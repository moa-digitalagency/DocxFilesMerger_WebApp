"""
DocxFilesMerger - Application de traitement et fusion de documents.
Développé par MOA Digital Agency LLC (https://myoneart.com)
Email: moa@myoneart.com
Copyright © 2025 MOA Digital Agency LLC. Tous droits réservés.
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Langue par défaut de l'application
DEFAULT_LANGUAGE = os.environ.get('DEFAULT_LANGUAGE', 'fr')

# Obtenir les langues disponibles à partir des variables d'environnement
available_languages_str = os.environ.get('AVAILABLE_LANGUAGES', 'fr:Français,en:English')
AVAILABLE_LANGUAGES = {}

# Convertir la chaîne en dictionnaire
for lang_pair in available_languages_str.split(','):
    if ':' in lang_pair:
        code, name = lang_pair.split(':')
        AVAILABLE_LANGUAGES[code] = name

# Traductions pour l'interface utilisateur
translations = {
    # Français
    'fr': {
        # Navigation et titres généraux
        'app_title': 'DocxFilesMerger',
        'home': 'Accueil',
        'admin': 'Administration',
        'help': 'Aide',
        'about': 'À propos',
        
        # Page d'accueil
        'medical_records_processing': 'Traitement de Dossiers Médicaux',
        'upload_title': 'Téléversement de Fichier',
        'upload_subtitle': 'Cet outil traite une archive ZIP contenant des dossiers médicaux (fichiers .doc ou .docx), les fusionne en un seul document et le convertit en PDF.',
        'how_it_works': 'Comment ça fonctionne :',
        'step_1': 'Téléversez un fichier ZIP contenant des dossiers médicaux (.doc ou .docx)',
        'step_2': 'Le système extraira et fusionnera tous les dossiers en un seul document',
        'step_3': 'Chaque dossier sera séparé par une ligne d\'en-tête avec le nom du fichier',
        'step_4': 'Téléchargez le document fusionné aux formats DOCX et PDF',
        
        # Zone de glisser-déposer
        'drop_zone_text': 'Glissez et déposez votre fichier ZIP ici',
        'drop_zone_or': 'ou',
        'browse_files': 'Parcourir les fichiers',
        
        # Boutons d'action
        'upload_and_process': 'Téléverser et Traiter',
        'cancel': 'Annuler',
        'reset': 'Réinitialiser',
        'download_docx': 'Télécharger le DOCX',
        'download_pdf': 'Télécharger le PDF',
        'process_another': 'Traiter un autre fichier',
        
        # Messages de progression
        'uploading': 'Téléversement en cours...',
        'processing': 'Traitement en cours...',
        'extracting': 'Extraction des fichiers...',
        'converting': 'Conversion des fichiers DOC en DOCX...',
        'merging': 'Fusion des documents...',
        'converting_to_pdf': 'Conversion du document fusionné en PDF...',
        'complete': 'Traitement terminé avec succès.',
        'error': 'Une erreur est survenue.',
        
        # Messages motivants
        'motivation_1': "C'est parti ! 🚀",
        'motivation_2': "Bonne progression ! ⭐",
        'motivation_3': "Vous êtes sur la bonne voie ! 👍",
        'motivation_4': "Plus que quelques minutes... 🙌",
        'motivation_5': "On y est presque ! 🎯",
        'motivation_6': "Mission accomplie ! 🏆",
        
        # Résultats
        'processing_complete': 'Traitement terminé avec succès',
        'processing_info': 'Informations de traitement :',
        'files_processed': 'Fichiers traités',
        'processing_time': 'Temps de traitement',
        'download_options': 'Vous pouvez maintenant télécharger le résultat dans les formats suivants :',
        
        # Instructions
        'instructions': 'Instructions',
        'zip_preparation': 'Préparation de votre fichier ZIP',
        'zip_content_info': 'Le fichier ZIP doit contenir des documents de dossiers médicaux au format .doc ou .docx. Le système va :',
        'extract_all': 'Extraire tous les fichiers .doc et .docx (en ignorant les autres types de fichiers)',
        'merge_content': 'Fusionner le contenu en un seul document',
        'add_separator': 'Ajouter une ligne de séparation avant le contenu de chaque document',
        'generate_versions': 'Générer les versions .docx et .pdf du document fusionné',
        'important_note': 'Important :',
        'large_archives_warning': 'Pour les grandes archives contenant de nombreux fichiers (5 000+), le traitement peut prendre plusieurs minutes.',
        'after_processing': 'Après le traitement',
        'after_processing_info': 'Une fois le traitement terminé, vous pourrez télécharger :',
        'merged_docx': 'Un fichier .docx fusionné contenant tous les dossiers',
        'pdf_version': 'Une version .pdf du document fusionné',
        
        # Erreurs
        'error_title': 'Erreur',
        'file_not_found': 'Fichier non trouvé',
        'system_error': 'Erreur système',
        'no_file_available': 'Aucun fichier disponible',
        'what_to_do': 'Que faire maintenant ?',
        'go_back': 'Retour à l\'accueil',
        'check_zip': 'Vérifiez que votre fichier ZIP contient bien des documents .doc ou .docx',
        'contact_support': 'Si le problème persiste, contactez le support technique',
        
        # Footer
        'copyright': 'Outil de DocxFilesMerger',
        'shortcuts_available': 'Raccourcis clavier disponibles. Voir la page d\'aide pour plus d\'informations.',
        
        # Raccourcis clavier
        'keyboard_shortcuts': 'Raccourcis Clavier',
        'shortcut': 'Raccourci',
        'action': 'Action',
        'open_file_selector': 'Ouvrir le sélecteur de fichiers',
        'cancel_operation': 'Annuler l\'opération en cours',
        'download_docx_shortcut': 'Télécharger le document DOCX',
        'download_pdf_shortcut': 'Télécharger le document PDF',
        'reset_app': 'Réinitialiser l\'application',
        'show_shortcuts': 'Afficher l\'aide des raccourcis',
        'close': 'Fermer',
    },
    
    # Anglais
    'en': {
        # Navigation and general titles
        'app_title': 'DocxFilesMerger',
        'home': 'Home',
        'admin': 'Admin',
        'help': 'Help',
        'about': 'About',
        
        # Home page
        'medical_records_processing': 'Medical Records Processing',
        'upload_title': 'File Upload',
        'upload_subtitle': 'This tool processes a ZIP archive containing medical records (.doc or .docx files), merges them into a single document and converts it to PDF.',
        'how_it_works': 'How it works:',
        'step_1': 'Upload a ZIP file containing medical records (.doc or .docx)',
        'step_2': 'The system will extract and merge all records into a single document',
        'step_3': 'Each record will be separated by a header line with the filename',
        'step_4': 'Download the merged document in DOCX and PDF formats',
        
        # Drop zone
        'drop_zone_text': 'Drag and drop your ZIP file here',
        'drop_zone_or': 'or',
        'browse_files': 'Browse files',
        
        # Action buttons
        'upload_and_process': 'Upload and Process',
        'cancel': 'Cancel',
        'reset': 'Reset',
        'download_docx': 'Download DOCX',
        'download_pdf': 'Download PDF',
        'process_another': 'Process another file',
        
        # Progress messages
        'uploading': 'Uploading...',
        'processing': 'Processing...',
        'extracting': 'Extracting files...',
        'converting': 'Converting DOC files to DOCX...',
        'merging': 'Merging documents...',
        'converting_to_pdf': 'Converting merged document to PDF...',
        'complete': 'Processing completed successfully.',
        'error': 'An error occurred.',
        
        # Motivational messages
        'motivation_1': "Let's go! 🚀",
        'motivation_2': "Good progress! ⭐",
        'motivation_3': "You're on the right track! 👍",
        'motivation_4': "Just a few more minutes... 🙌",
        'motivation_5': "Almost there! 🎯",
        'motivation_6': "Mission accomplished! 🏆",
        
        # Results
        'processing_complete': 'Processing completed successfully',
        'processing_info': 'Processing information:',
        'files_processed': 'Files processed',
        'processing_time': 'Processing time',
        'download_options': 'You can now download the result in the following formats:',
        
        # Instructions
        'instructions': 'Instructions',
        'zip_preparation': 'Preparing your ZIP file',
        'zip_content_info': 'The ZIP file must contain medical record documents in .doc or .docx format. The system will:',
        'extract_all': 'Extract all .doc and .docx files (ignoring other file types)',
        'merge_content': 'Merge the content into a single document',
        'add_separator': 'Add a separator line before the content of each document',
        'generate_versions': 'Generate .docx and .pdf versions of the merged document',
        'important_note': 'Important:',
        'large_archives_warning': 'For large archives containing many files (5,000+), processing can take several minutes.',
        'after_processing': 'After processing',
        'after_processing_info': 'Once processing is complete, you will be able to download:',
        'merged_docx': 'A merged .docx file containing all records',
        'pdf_version': 'A .pdf version of the merged document',
        
        # Errors
        'error_title': 'Error',
        'file_not_found': 'File not found',
        'system_error': 'System error',
        'no_file_available': 'No file available',
        'what_to_do': 'What to do now?',
        'go_back': 'Back to home',
        'check_zip': 'Check that your ZIP file contains .doc or .docx documents',
        'contact_support': 'If the problem persists, contact technical support',
        
        # Footer
        'copyright': 'DocxFilesMerger Tool',
        'shortcuts_available': 'Keyboard shortcuts available. See help page for more information.',
        
        # Keyboard shortcuts
        'keyboard_shortcuts': 'Keyboard Shortcuts',
        'shortcut': 'Shortcut',
        'action': 'Action',
        'open_file_selector': 'Open file selector',
        'cancel_operation': 'Cancel current operation',
        'download_docx_shortcut': 'Download DOCX document',
        'download_pdf_shortcut': 'Download PDF document',
        'reset_app': 'Reset application',
        'show_shortcuts': 'Show shortcuts help',
        'close': 'Close',
    }
}

def get_translation(lang_code, key):
    """
    Récupère une traduction basée sur le code de langue et la clé.
    Retourne la traduction dans la langue par défaut si la traduction demandée n'existe pas.
    """
    if lang_code not in translations:
        lang_code = DEFAULT_LANGUAGE
        
    if key not in translations[lang_code]:
        # Si la clé n'existe pas dans la langue choisie, essayer la langue par défaut
        if key in translations[DEFAULT_LANGUAGE]:
            return translations[DEFAULT_LANGUAGE][key]
        # Si elle n'existe pas non plus dans la langue par défaut, retourner la clé
        return key
        
    return translations[lang_code][key]

def get_available_languages():
    """
    Retourne un dictionnaire des langues disponibles.
    """
    return AVAILABLE_LANGUAGES