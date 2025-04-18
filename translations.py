"""
DocxFilesMerger - Application de traitement et fusion de documents.
Développé par MOA Digital Agency LLC (https://myoneart.com)
Email: moa@myoneart.com
Copyright © 2025 MOA Digital Agency LLC. Tous droits réservés.
"""

import os
from flask import session
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Dictionnaire de traduction
translations = {
    'fr': {
        # Interface utilisateur générale
        'title': 'DocxFilesMerger - Fusion de documents médicaux',
        'home': 'Accueil',
        'admin': 'Administration',
        'help': 'Aide',
        'upload_title': 'Téléversez votre fichier ZIP',
        'upload_subtitle': 'Glissez-déposez votre fichier ZIP contenant des documents .doc ou .docx',
        'or_text': 'ou',
        'browse_files': 'Parcourir les fichiers',
        'processing': 'Traitement en cours...',
        'download_docx': 'Télécharger DOCX',
        'download_pdf': 'Télécharger PDF',
        'restart': 'Recommencer',
        
        # Messages d'information et d'erreur
        'upload_success': 'Fichier téléversé avec succès.',
        'processing_started': 'Traitement démarré. Veuillez patienter...',
        'processing_complete': 'Traitement terminé avec succès.',
        'error_occurred': 'Une erreur s\'est produite.',
        'no_file_selected': 'Aucun fichier sélectionné.',
        'only_zip_allowed': 'Seuls les fichiers ZIP sont autorisés.',
        'file_too_large': 'Le fichier est trop volumineux.',
        
        # Étapes de traitement
        'step_extract': 'Extraction des fichiers...',
        'step_convert': 'Conversion des fichiers...',
        'step_merge': 'Fusion des documents...',
        'step_pdf': 'Génération du PDF...',
        
        # Administration
        'admin_login': 'Connexion Administrateur',
        'admin_dashboard': 'Tableau de bord d\'administration',
        'username': 'Nom d\'utilisateur',
        'password': 'Mot de passe',
        'login': 'Se connecter',
        'logout': 'Déconnexion',
        'global_stats': 'Statistiques globales',
        'total_jobs': 'Traitements totaux',
        'total_files': 'Fichiers traités',
        'avg_time': 'Temps moyen de traitement',
        'recent_jobs': 'Traitements récents',
        'daily_stats': 'Statistiques par jour',
        'config': 'Configuration',
        'save': 'Enregistrer',
        'refresh_stats': 'Actualiser les statistiques',
        'clear_history': 'Supprimer l\'historique',
        'confirm_clear': 'Êtes-vous sûr de vouloir supprimer tout l\'historique des traitements?',
        'warning_irreversible': 'Attention : Cette action est irréversible.',
        'cancel': 'Annuler',
        'confirm_delete': 'Supprimer définitivement',
        
        # Statuts des traitements
        'status_uploaded': 'Téléversé',
        'status_processing': 'En cours',
        'status_completed': 'Terminé',
        'status_error': 'Erreur',
        
        # Messages motivants
        'motivation_0': 'Préparation des documents...',
        'motivation_20': 'Traitement des fichiers en cours...',
        'motivation_40': 'Bientôt terminé, continuez à patienter...',
        'motivation_60': 'Les documents sont en train d\'être combinés...',
        'motivation_80': 'Finalisation de la fusion, c\'est presque fini !',
        'motivation_100': 'Traitement terminé avec succès !',
        
        # Footer
        'footer_text': 'Outil de DocxFilesMerger © 2025',
        'shortcuts_info': 'Raccourcis clavier disponibles. Voir la page d\'aide pour plus d\'informations.',
        
        # Erreurs
        'error_404': 'Page introuvable',
        'error_500': 'Erreur interne du serveur',
        'back_home': 'Retour à l\'accueil'
    },
    'en': {
        # General user interface
        'title': 'DocxFilesMerger - Medical Document Merging',
        'home': 'Home',
        'admin': 'Administration',
        'help': 'Help',
        'upload_title': 'Upload your ZIP file',
        'upload_subtitle': 'Drag and drop your ZIP file containing .doc or .docx documents',
        'or_text': 'or',
        'browse_files': 'Browse files',
        'processing': 'Processing...',
        'download_docx': 'Download DOCX',
        'download_pdf': 'Download PDF',
        'restart': 'Start over',
        
        # Information and error messages
        'upload_success': 'File uploaded successfully.',
        'processing_started': 'Processing started. Please wait...',
        'processing_complete': 'Processing completed successfully.',
        'error_occurred': 'An error occurred.',
        'no_file_selected': 'No file selected.',
        'only_zip_allowed': 'Only ZIP files are allowed.',
        'file_too_large': 'File is too large.',
        
        # Processing steps
        'step_extract': 'Extracting files...',
        'step_convert': 'Converting files...',
        'step_merge': 'Merging documents...',
        'step_pdf': 'Generating PDF...',
        
        # Administration
        'admin_login': 'Administrator Login',
        'admin_dashboard': 'Administration Dashboard',
        'username': 'Username',
        'password': 'Password',
        'login': 'Log in',
        'logout': 'Log out',
        'global_stats': 'Global Statistics',
        'total_jobs': 'Total Jobs',
        'total_files': 'Files Processed',
        'avg_time': 'Average Processing Time',
        'recent_jobs': 'Recent Jobs',
        'daily_stats': 'Daily Statistics',
        'config': 'Configuration',
        'save': 'Save',
        'refresh_stats': 'Refresh Statistics',
        'clear_history': 'Clear History',
        'confirm_clear': 'Are you sure you want to delete all processing history?',
        'warning_irreversible': 'Warning: This action is irreversible.',
        'cancel': 'Cancel',
        'confirm_delete': 'Delete Permanently',
        
        # Processing statuses
        'status_uploaded': 'Uploaded',
        'status_processing': 'Processing',
        'status_completed': 'Completed',
        'status_error': 'Error',
        
        # Motivational messages
        'motivation_0': 'Preparing documents...',
        'motivation_20': 'Processing files in progress...',
        'motivation_40': 'Almost done, please continue to wait...',
        'motivation_60': 'Documents are being combined...',
        'motivation_80': 'Finalizing the merge, almost there!',
        'motivation_100': 'Processing completed successfully!',
        
        # Footer
        'footer_text': 'DocxFilesMerger Tool © 2025',
        'shortcuts_info': 'Keyboard shortcuts available. See Help page for more information.',
        
        # Errors
        'error_404': 'Page not found',
        'error_500': 'Internal server error',
        'back_home': 'Back to home'
    }
}

def get_translation(lang_code, key):
    """
    Récupère une traduction basée sur le code de langue et la clé.
    Retourne la traduction dans la langue par défaut si la traduction demandée n'existe pas.
    """
    # Par défaut, utiliser la langue française
    if not lang_code or lang_code not in translations:
        lang_code = 'fr'
    
    # Récupérer la traduction ou utiliser la clé elle-même si non trouvée
    if key in translations[lang_code]:
        return translations[lang_code][key]
    elif 'fr' in translations and key in translations['fr']:
        # Fallback à la langue par défaut
        return translations['fr'][key]
    else:
        # Si la clé n'existe pas, retourner la clé elle-même
        return key

def get_available_languages():
    """
    Retourne un dictionnaire des langues disponibles.
    """
    languages = {
        'fr': 'Français',
        'en': 'English'
    }
    return languages