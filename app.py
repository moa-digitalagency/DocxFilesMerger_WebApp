"""
DocxFilesMerger - Application de traitement et fusion de documents.
Développé par MOA Digital Agency LLC (https://myoneart.com)
Email: moa@myoneart.com
Copyright © 2025 MOA Digital Agency LLC. Tous droits réservés.
"""

import os
import time
import json
import shutil
import threading
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, abort
from utils import process_zip_file, cleanup_old_files
from models import db, ProcessingJob, UsageStat, Config
from datetime import datetime

# Configuration de l'application
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_key_for_docxfilesmerger")
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 500  # 500 MB
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(os.getcwd(), 'outputs')
app.config['STATUS_FOLDER'] = os.path.join(os.getcwd(), 'status')
app.config['ALLOWED_EXTENSIONS'] = {'zip'}

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser la base de données avec des options de reconnexion
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "pool_size": 10,
    "max_overflow": 15,
    "connect_args": {
        "connect_timeout": 10,
        "application_name": "DocxFilesMerger"
    }
}
db.init_app(app)

# Créer les dossiers nécessaires s'ils n'existent pas
for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'], app.config['STATUS_FOLDER']]:
    os.makedirs(folder, exist_ok=True)
    
# Création des tables de la base de données si elles n'existent pas
with app.app_context():
    # Vérifier la connexion à la base de données
    try:
        # Test simple pour vérifier que la base est accessible
        db.session.execute(db.text('SELECT 1'))
        print("Database connection successful!")
        
        # Créer les tables
        db.create_all()
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        print("The application will continue, but database operations may fail.")

# Vérification des extensions de fichiers autorisées
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route principale
@app.route('/')
def index():
    # Nettoyer les anciens fichiers à chaque rechargement de la page principale
    cleanup_thread = threading.Thread(target=cleanup_old_files, args=(app.config['UPLOAD_FOLDER'],))
    cleanup_thread.daemon = True
    cleanup_thread.start()
    
    cleanup_thread = threading.Thread(target=cleanup_old_files, args=(app.config['OUTPUT_FOLDER'],))
    cleanup_thread.daemon = True
    cleanup_thread.start()
    
    cleanup_thread = threading.Thread(target=cleanup_old_files, args=(app.config['STATUS_FOLDER'],))
    cleanup_thread.daemon = True
    cleanup_thread.start()
    
    return render_template('index.html')

# Route pour le téléversement du fichier
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'Aucun fichier n\'a été téléversé.'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Aucun fichier n\'a été sélectionné.'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Seuls les fichiers ZIP sont autorisés.'}), 400
    
    try:
        # Sécuriser le nom du fichier et créer un identifiant unique
        filename = secure_filename(file.filename)
        timestamp = int(time.time())
        unique_id = f"{timestamp}_{os.urandom(4).hex()}"
        
        # Créer un dossier spécifique pour cette session
        session_folder = os.path.join(app.config['UPLOAD_FOLDER'], unique_id)
        output_folder = os.path.join(app.config['OUTPUT_FOLDER'], unique_id)
        status_folder = os.path.join(app.config['STATUS_FOLDER'], unique_id)
        
        os.makedirs(session_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)
        os.makedirs(status_folder, exist_ok=True)
        
        # Sauvegarder le fichier
        zip_path = os.path.join(session_folder, filename)
        file.save(zip_path)
        
        # Initialiser le statut
        status_file = os.path.join(status_folder, 'status.json')
        with open(status_file, 'w') as f:
            json.dump({
                'percent': 0,
                'status_text': 'Fichier téléversé avec succès.',
                'current_step': 'extract',
                'complete': False,
                'error': None,
                'start_time': timestamp
            }, f)
        
        # Estimer le nombre de fichiers (pour l'interface utilisateur)
        file_count = 20  # Valeur par défaut
        
        # Créer un enregistrement dans la base de données
        with app.app_context():
            job = ProcessingJob(
                job_id=unique_id,
                status='uploaded',
                file_count=file_count,
                original_filename=filename
            )
            db.session.add(job)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'zip_path': zip_path,
            'output_dir': output_folder,
            'status_dir': status_folder,
            'file_count': file_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Route pour traiter le fichier téléversé
@app.route('/process', methods=['POST'])
def process_file():
    data = request.json
    
    if not data or 'zip_path' not in data:
        return jsonify({'success': False, 'error': 'Données invalides.'}), 400
    
    zip_path = data['zip_path']
    
    if not os.path.exists(zip_path):
        return jsonify({'success': False, 'error': 'Le fichier ZIP n\'existe pas.'}), 404
    
    # Obtenir le dossier unique
    unique_id = os.path.dirname(zip_path).split(os.path.sep)[-1]
    output_folder = os.path.join(app.config['OUTPUT_FOLDER'], unique_id)
    status_folder = os.path.join(app.config['STATUS_FOLDER'], unique_id)
    
    try:
        # Mettre à jour l'état du job dans la base de données
        job = ProcessingJob.query.filter_by(job_id=unique_id).first()
        if job:
            job.status = 'processing'
            db.session.commit()
        
        # Lancer le traitement dans un thread séparé
        process_thread = threading.Thread(
            target=process_zip_file,
            args=(zip_path, output_folder),
            kwargs={'status_dir': status_folder, 'job_id': unique_id}
        )
        process_thread.daemon = True
        process_thread.start()
        
        return jsonify({'success': True})
        
    except Exception as e:
        # Enregistrer l'erreur dans le fichier de statut
        status_file = os.path.join(status_folder, 'status.json')
        with open(status_file, 'w') as f:
            json.dump({
                'percent': 0,
                'status_text': 'Une erreur s\'est produite.',
                'current_step': 'error',
                'complete': False,
                'error': str(e)
            }, f)
        
        # Mettre à jour le statut d'erreur dans la base de données
        try:
            job = ProcessingJob.query.filter_by(job_id=unique_id).first()
            if job:
                job.status = 'error'
                db.session.commit()
        except Exception as db_err:
            print(f"Erreur lors de la mise à jour du statut dans la base de données: {str(db_err)}")
        
        return jsonify({'success': False, 'error': str(e)}), 500

# Route pour télécharger les fichiers traités
@app.route('/download/<file_type>')
def download_file(file_type):
    """Télécharger le fichier fusionné (docx ou pdf)"""
    # Récupérer tous les dossiers dans le répertoire output
    output_dirs = []
    
    try:
        # Parcourir le répertoire de sortie de manière récursive
        for root, dirs, files in os.walk(app.config['OUTPUT_FOLDER']):
            # Chercher les fichiers merged.docx ou merged.pdf
            if 'merged.docx' in files or 'merged.pdf' in files:
                output_dirs.append(root)
    except Exception as e:
        print(f"Erreur lors de la recherche des dossiers de sortie: {str(e)}")
        return render_template('error.html', error="Erreur système", 
                              message="Impossible d'accéder aux fichiers de sortie.")
    
    if not output_dirs:
        print("Aucun fichier fusionné trouvé")
        return render_template('error.html', error="Aucun fichier disponible", 
                              message="Aucun fichier fusionné n'a été trouvé. Veuillez d'abord traiter un fichier ZIP.")
    
    # Trouver le dossier le plus récent
    try:
        latest_dir = max(output_dirs, key=os.path.getmtime)
        print(f"Dossier le plus récent trouvé: {latest_dir}")
    except Exception as e:
        print(f"Erreur lors de la recherche du dossier le plus récent: {str(e)}")
        return render_template('error.html', error="Erreur système", 
                              message="Impossible de déterminer le dossier de sortie le plus récent.")
    
    # Déterminer le chemin du fichier à télécharger
    if file_type == 'docx':
        file_path = os.path.join(latest_dir, 'merged.docx')
        filename = 'documents_fusionnes.docx'
    elif file_type == 'pdf':
        file_path = os.path.join(latest_dir, 'merged.pdf')
        filename = 'documents_fusionnes.pdf'
    else:
        print(f"Type de fichier non reconnu: {file_type}")
        abort(404)
    
    print(f"Tentative de téléchargement du fichier: {file_path}")
    
    # Vérifier si le fichier existe
    if not os.path.exists(file_path):
        print(f"Fichier non trouvé: {file_path}")
        return render_template('error.html', error="Fichier non trouvé", 
                              message=f"Le fichier {file_type} demandé n'est pas disponible.")
    
    # Envoyer le fichier
    try:
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        print(f"Erreur lors de l'envoi du fichier: {str(e)}")
        return render_template('error.html', error="Erreur de téléchargement", 
                              message=f"Une erreur s'est produite lors du téléchargement: {str(e)}")

# Route pour vérifier le statut du traitement
@app.route('/status')
def processing_status():
    # Trouver le dossier de statut le plus récent
    try:
        status_folders = [os.path.join(app.config['STATUS_FOLDER'], f) for f in os.listdir(app.config['STATUS_FOLDER'])]
        if not status_folders:
            return jsonify({'error': 'Aucun traitement en cours.'})
        
        latest_folder = max(status_folders, key=os.path.getmtime)
        status_file = os.path.join(latest_folder, 'status.json')
        
        if not os.path.exists(status_file):
            return jsonify({'error': 'Fichier de statut introuvable.'})
        
        try:
            with open(status_file, 'r') as f:
                status_data = json.load(f)
            
            # Ajouter des statistiques si le traitement est terminé
            if status_data.get('complete', False):
                start_time = status_data.get('start_time', 0)
                end_time = status_data.get('end_time', int(time.time()))
                processing_time = end_time - start_time
                
                status_data['stats'] = {
                    'processing_time': processing_time,
                    'file_count': status_data.get('file_count', 0)
                }
            
            # Pour les journaux de débogage
            print(f"Status file content: {json.dumps(status_data, indent=2)}")
            
            # Si un état d'erreur est détecté, ajoutez plus de détails pour faciliter le débogage
            if status_data.get('current_step') == 'error':
                error_msg = status_data.get('error', 'Erreur inconnue')
                traceback_info = status_data.get('traceback', '')
                print(f"Erreur détectée: {error_msg}")
                if traceback_info:
                    print(f"Traceback: {traceback_info}")
            
            return jsonify(status_data)
            
        except Exception as e:
            return jsonify({'error': f'Erreur lors de la lecture du statut: {str(e)}'})
    except Exception as outer_e:
        return jsonify({'error': f'Erreur lors de la récupération du statut: {str(outer_e)}'})

# Afficher le README
@app.route('/readme')
def show_readme():
    with open('README.md', 'r') as f:
        readme_content = f.read()
    
    # Ici, on pourrait convertir le Markdown en HTML pour un affichage plus élégant
    # Pour l'instant, on redirige simplement vers la page d'accueil
    return redirect(url_for('index'))

# Interface d'administration
@app.route('/admin')
def admin_dashboard():
    """Page d'administration avec statistiques et configuration"""
    # Récupérer les statistiques globales
    total_jobs = ProcessingJob.query.count()
    total_files = db.session.query(db.func.sum(ProcessingJob.file_count)).scalar() or 0
    avg_time = db.session.query(db.func.avg(ProcessingJob.processing_time)).scalar() or 0
    
    # Préparer les statistiques pour le template
    stats = {
        'total_jobs': total_jobs,
        'total_files': total_files,
        'avg_time': int(avg_time)
    }
    
    # Récupérer les jobs récents
    recent_jobs = ProcessingJob.query.order_by(ProcessingJob.created_at.desc()).limit(10).all()
    
    # Récupérer les statistiques par jour
    daily_stats = UsageStat.query.order_by(UsageStat.date.desc()).limit(7).all()
    
    # Récupérer les configurations
    configs = Config.query.all()
    
    return render_template('admin.html', 
                          stats=stats, 
                          recent_jobs=recent_jobs, 
                          daily_stats=daily_stats,
                          configs=configs)

# Mise à jour de la configuration
@app.route('/admin/config', methods=['POST'])
def update_config():
    """Mettre à jour les paramètres de configuration"""
    try:
        for key, value in request.form.items():
            config = Config.query.filter_by(key=key).first()
            if config:
                config.value = value
                db.session.commit()
        
        return redirect(url_for('admin_dashboard'))
    except Exception as e:
        return render_template('error.html', error_code=500, 
                              error_message=f"Erreur lors de la mise à jour de la configuration: {str(e)}"), 500

# Gestionnaire d'erreur 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page introuvable"), 404

# Gestionnaire d'erreur 500
@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error_code=500, error_message="Erreur interne du serveur"), 500

# Exécution de l'application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
