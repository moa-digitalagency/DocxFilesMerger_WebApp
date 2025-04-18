# 📋 DocxFilesMerger 🏥

## 🌟 Présentation

Bienvenue dans l'application **DocxFilesMerger** ! 🎉
Cette application web permet de traiter efficacement et rapidement des archives ZIP contenant des milliers de dossiers médicaux au format .doc ou .docx.

![Badge Langage](https://img.shields.io/badge/Langage-Python-blue)
![Badge Framework](https://img.shields.io/badge/Framework-Flask-green)
![Badge Version](https://img.shields.io/badge/Version-1.0.0-orange)

### 📝 Développeur

**MOA Digital Agency LLC**  
Site web: [https://myoneart.com](https://myoneart.com)  
Contact: [moa@myoneart.com](mailto:moa@myoneart.com)

## 🚀 Fonctionnalités principales

- ✅ **Extraction de fichiers** : Extrait automatiquement tous les fichiers .doc et .docx d'une archive ZIP
- ✅ **Conversion de format** : Convertit les fichiers .doc en .docx si nécessaire
- ✅ **Fusion de documents** : Combine tous les fichiers en un seul document avec des séparateurs clairs
- ✅ **Conversion PDF** : Génère une version PDF du document fusionné
- ✅ **Interface utilisateur intuitive** : Interface web simple et réactive pour téléverser et télécharger des fichiers

## 🔍 Comment ça fonctionne

1. 📤 **Téléversez** une archive ZIP contenant des dossiers médicaux (.doc/.docx)
2. ⚙️ Le système **extrait** tous les fichiers pertinents
3. 🔄 Les fichiers sont **convertis** (si nécessaire) et **fusionnés** en un seul document
4. 📑 Une **séparation claire** est ajoutée avant chaque dossier : `<NOMFICHIER.extension>...`
5. 📊 Le système génère automatiquement des **versions DOCX et PDF** du document final
6. 📥 **Téléchargez** les documents finaux une fois le traitement terminé

## 💻 Technologies utilisées

- **Backend** : Python, Flask
- **Traitement de documents** : python-docx, docx2pdf
- **Frontend** : HTML5, CSS3, JavaScript, Bootstrap
- **Système de fichiers** : Gestion temporaire des fichiers zipfile
- **Base de données** : PostgreSQL (pour le suivi des traitements)

## 🚀 Déploiement

L'application peut être déployée sur différents types de serveurs :

### Configuration système minimale
- **CPU** : 2 cœurs (4 recommandés)  
- **RAM** : 2 Go minimum (4 Go recommandés)
- **Espace disque** : 20 Go minimum
- **OS** : Linux (Ubuntu 20.04 LTS ou plus récent recommandé)

### 🌐 Déploiement sur cPanel (Domaine ou Sous-domaine)

#### Prérequis
- Hébergement avec cPanel supportant Python 3.7+ et PostgreSQL
- Accès SSH (recommandé mais pas obligatoire)
- Domaine ou sous-domaine configuré

#### Étape 1: Configuration de la base de données PostgreSQL
1. Connectez-vous à votre interface cPanel
2. Allez dans la section "Bases de données" et cliquez sur "PostgreSQL Databases"
3. Créez une nouvelle base de données nommée `docxfilesmerger_db`
4. Créez un nouvel utilisateur avec un mot de passe sécurisé (ex: `docxuser`)
   - Utilisez un générateur de mot de passe pour créer un mot de passe fort
   - **IMPORTANT**: Notez ces identifiants, vous en aurez besoin plus tard
5. Associez l'utilisateur à la base de données avec tous les privilèges

#### Étape 2: Préparation de l'environnement Python
1. Dans cPanel, allez dans "Setup Python App"
2. Créez une nouvelle application avec les paramètres suivants:
   - **Python version**: 3.9 ou plus récent
   - **Application root**: `/docxfilesmerger` ou le chemin souhaité
   - **Application URL**: Votre domaine ou sous-domaine (ex: `docxfilesmerger.votredomaine.com`)
   - **Application startup file**: `main.py`
   - **Application Entry point**: `app`
3. Cliquez sur "Create" pour créer l'environnement Python

#### Étape 3: Téléchargement et configuration des fichiers
1. Téléchargez l'application via le Gestionnaire de fichiers de cPanel:
   - Accédez au dossier d'application créé à l'étape précédente
   - Téléversez tous les fichiers de l'application (.py, templates/, static/, etc.)

2. Créez un fichier `.env` à la racine du projet:
   ```
   DATABASE_URL=postgresql://docxuser:votre_mot_de_passe@localhost:5432/docxfilesmerger_db
   FLASK_SECRET_KEY=une_clé_secrète_très_longue_et_aléatoire
   UPLOAD_FOLDER=/home/username/docxfilesmerger/uploads
   OUTPUT_FOLDER=/home/username/docxfilesmerger/outputs
   STATUS_FOLDER=/home/username/docxfilesmerger/status
   ```
   Remplacez `username` par votre nom d'utilisateur cPanel et `votre_mot_de_passe` par le mot de passe PostgreSQL.

3. Créez un fichier `requirements.txt` contenant:
   ```
   flask==2.0.1
   flask-sqlalchemy==3.0.0
   psycopg2-binary==2.9.1
   python-docx==0.8.11
   docx2pdf==0.1.8
   PyPDF2==2.10.5
   reportlab==3.6.1
   gunicorn==20.1.0
   python-dotenv==0.19.0
   ```

4. Créez ou modifiez le fichier `.htaccess` à la racine de votre application:
   ```
   RewriteEngine On
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteRule ^(.*)$ /main.py [QSA,L]
   
   <Files ~ "\.(py|env)$">
       Order allow,deny
       Deny from all
   </Files>
   
   <Files main.py>
       SetHandler wsgi-script
       Options +ExecCGI
   </Files>
   
   # Augmenter la taille maximale des téléversements
   php_value upload_max_filesize 300M
   php_value post_max_size 300M
   ```

#### Étape 4: Installation des dépendances
1. Dans cPanel, retournez à "Setup Python App"
2. Sélectionnez votre application
3. Cliquez sur l'onglet "Installer des modules Python" ou "PIP Install"
4. Sélectionnez "From requirements.txt" et cliquez sur "Install Packages"

#### Étape 5: Configuration des dossiers d'upload
1. Via le Gestionnaire de fichiers cPanel, créez les dossiers suivants:
   - `uploads/` - Pour les fichiers ZIP téléversés
   - `outputs/` - Pour les fichiers traités
   - `status/`  - Pour les fichiers de statut
2. Définissez les permissions à 755 pour ces dossiers:
   ```bash
   chmod 755 uploads outputs status
   ```

#### Étape 6: Configuration de la base de données et premier démarrage
1. Accédez à votre application via SSH si disponible:
   ```bash
   cd ~/docxfilesmerger
   source venv/bin/activate  # Le chemin peut varier selon votre configuration cPanel
   python
   ```
2. Exécutez les commandes Python suivantes:
   ```python
   from app import app, db
   with app.app_context():
       db.create_all()
       exit()
   ```

3. Redémarrez l'application Python depuis cPanel

#### Étape 7: Configuration des tâches CRON pour le nettoyage
1. Dans cPanel, accédez à "Cron Jobs"
2. Créez une nouvelle tâche cron qui s'exécute quotidiennement:
   ```
   0 3 * * * cd ~/docxfilesmerger && /usr/local/bin/python3 -c "from utils import cleanup_old_files; cleanup_old_files('uploads', 24); cleanup_old_files('outputs', 24); cleanup_old_files('status', 24)"
   ```

#### Dépannage courant:
- **Erreur 500**: Vérifiez les logs d'erreur Apache dans cPanel
- **Problèmes de connexion à la base de données**: Vérifiez les informations de connexion dans `.env`
- **Fichiers non trouvés**: Vérifiez les permissions des dossiers `uploads`, `outputs` et `status`
- **Conversion PDF échoue**: Installez LibreOffice via SSH ou contactez votre hébergeur

### Documentation détaillée

Pour des instructions complètes sur le déploiement, voir notre documentation détaillée disponible à [moa@myoneart.com](mailto:moa@myoneart.com).

## 🛠️ Raccourcis clavier

| Raccourci | Action |
|-----------|--------|
| <kbd>Ctrl</kbd> + <kbd>O</kbd> | Ouvrir le sélecteur de fichiers |
| <kbd>Esc</kbd> | Annuler l'opération en cours |
| <kbd>Ctrl</kbd> + <kbd>D</kbd> | Télécharger le document DOCX |
| <kbd>Ctrl</kbd> + <kbd>P</kbd> | Télécharger le document PDF |
| <kbd>Ctrl</kbd> + <kbd>R</kbd> | Réinitialiser l'application |
| <kbd>Ctrl</kbd> + <kbd>H</kbd> | Afficher l'aide des raccourcis |

## 📋 Prérequis

- Python 3.7+
- Bibliothèques Python : flask, python-docx, docx2pdf, etc.
- Navigateur web moderne (Chrome, Firefox, Safari, Edge)

## ⚠️ Remarques importantes

- 🔒 **Confidentialité** : Cette application traite les fichiers localement et ne les envoie pas sur des serveurs externes
- 📦 **Taille maximale** : L'application a été testée avec des archives contenant plus de 5 000 fichiers
- ⏱️ **Temps de traitement** : Le traitement peut prendre plusieurs minutes pour les grandes archives
- 🧹 **Nettoyage automatique** : Les fichiers temporaires sont automatiquement supprimés après 24 heures

## 🔧 Dépannage

| Problème | Solution |
|----------|----------|
| L'archive ZIP n'est pas acceptée | Vérifiez que le fichier est bien au format ZIP (et non RAR ou 7z) |
| Erreur lors de l'extraction | Assurez-vous que l'archive n'est pas corrompue |
| Conversion PDF échoue | Installez LibreOffice pour améliorer la conversion PDF |
| Fichiers manquants | Seuls les fichiers .doc et .docx sont traités, les autres formats sont ignorés |

## 📞 Support

Pour toute question ou problème, n'hésitez pas à :
- 📧 Contacter le support : [moa@myoneart.com](mailto:moa@myoneart.com)
- 🌐 Visiter notre site web : [https://myoneart.com](https://myoneart.com)

## 📜 Licence

Ce projet est développé par MOA Digital Agency LLC. Tous droits réservés © 2025.
