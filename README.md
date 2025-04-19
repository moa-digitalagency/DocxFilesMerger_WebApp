# 📋 DocxFilesMerger 🏥

*[English version available here](README.en.md)*

## 🌟 Présentation

Bienvenue dans l'application **DocxFilesMerger** ! 🎉
Cette application web permet de traiter efficacement et rapidement des archives ZIP contenant des milliers de dossiers médicaux au format .doc ou .docx.

![Badge Langage](https://img.shields.io/badge/Langage-Python-blue)
![Badge Framework](https://img.shields.io/badge/Framework-Flask-green)
![Badge Version](https://img.shields.io/badge/Version-1.0.0-orange)

### 📝 Développeur

**MOA Digital Agency LLC**  
Développé par Aisance Kalonji  
Site web: [https://myoneart.com](https://myoneart.com)  
Contact: [moa@myoneart.com](mailto:moa@myoneart.com)  
Copyright © 2025 MOA Digital Agency LLC. Développé par Aisance Kalonji. Tous droits réservés.

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

### 🌐 Déploiement sur cPanel (Méthode avancée)

#### ⚠️ Considérations importantes pour cPanel
cPanel ne prend pas nativement en charge les applications Python comme Flask. La méthode décrite ci-dessous utilise des techniques avancées pour contourner ces limitations:

#### Prérequis
- Hébergement avec cPanel permettant l'installation de Python (via les "Setup Python App" ou manuellement)
- Accès SSH (fortement recommandé)
- Domaine ou sous-domaine configuré
- Au moins un plan d'hébergement de niveau intermédiaire ou professionnel

#### Étape 1: Configuration de la base de données PostgreSQL
1. Connectez-vous à votre interface cPanel
2. Accédez à "Bases de données" → "PostgreSQL Databases"
3. Créez une nouvelle base de données (ex: `docxfilesmerger_db`)
4. Créez un nouvel utilisateur avec un mot de passe sécurisé
   - **IMPORTANT**: Notez soigneusement ces identifiants
5. Associez l'utilisateur à la base de données avec tous les privilèges

#### Étape 2: Installation de Python via cPanel (Méthode 1 - Préférée)
Si votre cPanel propose l'option "Setup Python App":
1. Accédez à cette section et créez une nouvelle application
2. Sélectionnez Python 3.9+ et configurez les chemins d'application
3. Notez le chemin de l'environnement virtuel créé

#### Étape 2 (Alternative): Installation manuelle de Python (Méthode 2)
Si "Setup Python App" n'est pas disponible:
1. Connectez-vous via SSH:
   ```bash
   ssh username@votrehébergement.com
   ```
2. Installez Python localement:
   ```bash
   cd ~
   mkdir -p python/pythonvenv
   curl -O https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz
   tar xzf Python-3.9.9.tgz
   cd Python-3.9.9
   ./configure --prefix=$HOME/python --enable-optimizations
   make
   make install
   cd ~/python
   ~/python/bin/python3 -m venv pythonvenv
   ```
3. Vérifiez l'installation:
   ```bash
   ~/python/pythonvenv/bin/python --version
   ```

#### Étape 3: Configuration du projet
1. Téléchargez les fichiers de l'application dans votre dossier public_html ou un sous-dossier:
   ```bash
   cd ~/public_html/sousdomaine  # Ou le dossier souhaité
   git clone https://github.com/votredepot/docxfilesmerger.git .  # Si Git est disponible
   # OU téléversez manuellement via le Gestionnaire de fichiers cPanel
   ```

2. Créez un fichier `.env` à la racine du projet:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/docxfilesmerger_db
   FLASK_SECRET_KEY=une_clé_secrète_très_longue_et_aléatoire
   ADMIN_USERNAME=choisissez_un_nom_admin
   ADMIN_PASSWORD=mot_de_passe_admin_sécurisé
   UPLOAD_FOLDER=/home/username/public_html/sousdomaine/uploads
   OUTPUT_FOLDER=/home/username/public_html/sousdomaine/outputs
   STATUS_FOLDER=/home/username/public_html/sousdomaine/status
   ```
   Remplacez `username`, `password`, etc. par vos valeurs réelles.

3. Créez les dossiers nécessaires:
   ```bash
   mkdir -p uploads outputs status
   chmod 755 uploads outputs status
   ```

#### Étape 4: Installation des dépendances
1. Activez l'environnement Python et installez les dépendances:
   ```bash
   # Pour l'installation via Setup Python App (Méthode 1)
   source ~/virtualenv/pythonX.X/bin/activate  # Le chemin exact dépend de votre configuration cPanel
   
   # OU pour l'installation manuelle (Méthode 2)
   source ~/python/pythonvenv/bin/activate
   
   # Ensuite, installez les dépendances
   pip install flask flask-sqlalchemy psycopg2-binary python-docx docx2pdf PyPDF2 reportlab gunicorn python-dotenv flask-login
   ```

#### Étape 5: Configuration du serveur WSGI
Depuis que cPanel n'a pas de support natif pour Python WSGI, nous utiliserons une approche hybride:

1. Créez un fichier `passenger_wsgi.py`:
   ```python
   import os
   import sys
   
   # Chemin vers votre environnement Python
   PYTHON_PATH = '/home/username/python/pythonvenv/bin/python'  # Méthode 2
   # OU
   # PYTHON_PATH = '/home/username/virtualenv/pythonX.X/bin/python'  # Méthode 1
   
   # Chemin vers le dossier de l'application
   APP_PATH = '/home/username/public_html/sousdomaine'
   
   # Ajoutez le chemin de l'application au système
   sys.path.insert(0, APP_PATH)
   
   # Définissez la variable d'environnement pour Python
   os.environ['PYTHONHOME'] = PYTHON_PATH.replace('/bin/python', '')
   
   # Fonction d'application pour Passenger
   def application(environ, start_response):
       # Exécutez l'application WSGI Flask
       from main import app as flask_app
       return flask_app(environ, start_response)
   ```
   Remplacez `username` et les chemins par vos valeurs réelles.

2. Créez un fichier `.htaccess`:
   ```apache
   PassengerEnabled On
   PassengerPython /home/username/python/pythonvenv/bin/python  # Méthode 2
   # OU
   # PassengerPython /home/username/virtualenv/pythonX.X/bin/python  # Méthode 1
   
   <Files ~ "\.(py|env)$">
       Order allow,deny
       Deny from all
   </Files>
   
   <Files passenger_wsgi.py>
       Order allow,deny
       Allow from all
   </Files>
   
   # Augmenter la taille maximale des téléversements
   php_value upload_max_filesize 300M
   php_value post_max_size 300M
   
   # Protection des dossiers sensibles
   <DirectoryMatch "^/.*/\.(git|env)/">
       Require all denied
   </DirectoryMatch>
   ```

#### Étape 6: Initialisation de la base de données
1. Via SSH, exécutez Python pour initialiser la base de données:
   ```bash
   cd ~/public_html/sousdomaine
   # Activez l'environnement virtuel approprié selon la méthode utilisée
   
   python -c "from app import app, db; with app.app_context(): db.create_all()"
   ```

#### Étape 7: Configuration du déploiement sans Passenger (alternative)
Si Passenger n'est pas disponible, utilisez un script CGI:

1. Créez un fichier `cgi-bin/app.cgi`:
   ```python
   #!/home/username/python/pythonvenv/bin/python
   import os
   import sys
   
   # Ajustez le chemin vers votre application
   sys.path.insert(0, '/home/username/public_html/sousdomaine')
   
   # Chargez les variables d'environnement
   from dotenv import load_dotenv
   load_dotenv('/home/username/public_html/sousdomaine/.env')
   
   # Exécutez l'application
   from wsgiref.handlers import CGIHandler
   from main import app
   
   CGIHandler().run(app)
   ```
   
2. Rendez le script exécutable:
   ```bash
   chmod +x cgi-bin/app.cgi
   ```

3. Créez un `.htaccess` spécial pour la redirection CGI:
   ```apache
   RewriteEngine On
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteRule ^(.*)$ /cgi-bin/app.cgi/$1 [QSA,L]
   ```

#### Étape 8: Tâche CRON pour maintenance
1. Dans cPanel, accédez à "Cron Jobs"
2. Créez une tâche quotidienne:
   ```
   0 3 * * * cd /home/username/public_html/sousdomaine && /home/username/python/pythonvenv/bin/python -c "from utils import cleanup_old_files; cleanup_old_files('uploads', 24); cleanup_old_files('outputs', 24); cleanup_old_files('status', 24)"
   ```

#### Résolution des problèmes courants
- **Erreur 500**: Vérifiez les logs d'erreur Apache dans cPanel → "Error Log"
- **Problèmes de chemin Python**: Vérifiez que tous les chemins dans `passenger_wsgi.py` et `.htaccess` correspondent à votre environnement
- **Dépendances manquantes**: Installez les bibliothèques système nécessaires (contactez le support d'hébergement)
- **Permissions**: Assurez-vous que les dossiers uploads/outputs/status ont les permissions 755
- **Base de données inaccessible**: Vérifiez la configuration PostgreSQL dans votre hébergement

#### Notes sur les limitations de cPanel
- cPanel n'est pas optimisé pour les applications Python; attendez-vous à quelques défis techniques
- Le déploiement peut nécessiter l'assistance du support d'hébergement pour certaines configurations
- Certains hébergeurs imposent des limites de ressources qui peuvent affecter les performances
- Pour une expérience optimale, envisagez des plateformes spécialisées pour Python (PythonAnywhere, Heroku, DigitalOcean, etc.)

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

Ce projet est développé par MOA Digital Agency LLC. Développé par Aisance Kalonji. Tous droits réservés © 2025.
