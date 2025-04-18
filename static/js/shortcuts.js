/**
 * DocxFilesMerger - Application de traitement et fusion de documents.
 * Développé par MOA Digital Agency LLC (https://myoneart.com)
 * Email: moa@myoneart.com
 * Copyright © 2025 MOA Digital Agency LLC. Tous droits réservés.
 */
// Gestion des raccourcis clavier
document.addEventListener('DOMContentLoaded', function() {
    setupKeyboardShortcuts();
});

// Liste des raccourcis disponibles pour l'aide
const availableShortcuts = [
    { keys: 'Ctrl+O', description: 'Ouvrir le sélecteur de fichiers' },
    { keys: 'Ctrl+D', description: 'Télécharger le document fusionné (DOCX)' },
    { keys: 'Ctrl+P', description: 'Télécharger le document fusionné (PDF)' },
    { keys: 'Ctrl+R', description: 'Réinitialiser l\'application après traitement' },
    { keys: 'Ctrl+H', description: 'Afficher l\'aide des raccourcis' },
    { keys: 'Escape', description: 'Annuler l\'opération en cours' }
];

function setupKeyboardShortcuts() {
    // Créer un élément modal pour l'aide des raccourcis
    createShortcutsHelpModal();
    
    document.addEventListener('keydown', function(e) {
        // Globallement disponible : uploadStatus peut être undefined dans certains contextes
        const currentUploadStatus = window.uploadStatus || 'idle';
        
        // Ctrl+O : Ouvrir le sélecteur de fichiers
        if (e.ctrlKey && e.key === 'o') {
            e.preventDefault();
            const fileInput = document.getElementById('file-input');
            if (fileInput) fileInput.click();
        }
        
        // Escape : Annuler l'opération en cours
        if (e.key === 'Escape') {
            if (currentUploadStatus === 'uploading' || currentUploadStatus === 'processing') {
                if (confirm('Voulez-vous vraiment annuler l\'opération en cours ?')) {
                    if (typeof resetApplication === 'function') {
                        resetApplication();
                    }
                }
            }
        }
        
        // Ctrl+D : Télécharger DOCX (si disponible)
        if (e.ctrlKey && e.key === 'd') {
            e.preventDefault();
            const docxLink = document.querySelector('a[href="/download/docx"]');
            if (docxLink && !docxLink.classList.contains('disabled')) {
                docxLink.click();
            } else {
                showShortcutToast('Le fichier DOCX n\'est pas encore disponible');
            }
        }
        
        // Ctrl+P : Télécharger PDF (si disponible)
        if (e.ctrlKey && e.key === 'p') {
            e.preventDefault();
            const pdfLink = document.querySelector('a[href="/download/pdf"]');
            if (pdfLink && !pdfLink.classList.contains('disabled')) {
                pdfLink.click();
            } else {
                showShortcutToast('Le fichier PDF n\'est pas encore disponible');
                // Si l'impression native est activée, ne pas l'empêcher
                return true;
            }
        }
        
        // Ctrl+R : Réinitialiser l'application (seulement si terminé)
        if (e.ctrlKey && e.key === 'r') {
            if (currentUploadStatus === 'complete' || currentUploadStatus === 'error') {
                e.preventDefault(); // Empêcher le rechargement de la page
                if (typeof resetApplication === 'function') {
                    resetApplication();
                }
            }
        }
        
        // Ctrl+H : Afficher l'aide des raccourcis
        if (e.ctrlKey && e.key === 'h') {
            e.preventDefault();
            const shortcutsModal = document.getElementById('shortcuts-help-modal');
            if (shortcutsModal) {
                const bsModal = new bootstrap.Modal(shortcutsModal);
                bsModal.show();
            }
        }
    });
}

// Fonction pour créer le modal d'aide des raccourcis
function createShortcutsHelpModal() {
    if (document.getElementById('shortcuts-help-modal')) return;
    
    const modalDiv = document.createElement('div');
    modalDiv.className = 'modal fade';
    modalDiv.id = 'shortcuts-help-modal';
    modalDiv.tabIndex = '-1';
    modalDiv.setAttribute('aria-labelledby', 'shortcutsModalLabel');
    modalDiv.setAttribute('aria-hidden', 'true');
    
    // Créer le contenu du modal
    let shortcutsRows = '';
    availableShortcuts.forEach(shortcut => {
        shortcutsRows += `
            <tr>
                <td><kbd>${shortcut.keys}</kbd></td>
                <td>${shortcut.description}</td>
            </tr>
        `;
    });
    
    modalDiv.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="shortcutsModalLabel">
                        <i class="fas fa-keyboard me-2"></i>Raccourcis Clavier
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>Voici les raccourcis clavier disponibles dans l'application :</p>
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Raccourci</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${shortcutsRows}
                        </tbody>
                    </table>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fermer</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modalDiv);
}

// Afficher un toast pour les raccourcis non disponibles
function showShortcutToast(message) {
    // Créer un élément toast s'il n'existe pas déjà
    let toastContainer = document.getElementById('shortcut-toast-container');
    
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'shortcut-toast-container';
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    const toastId = 'shortcut-toast-' + Date.now();
    const toastEl = document.createElement('div');
    toastEl.id = toastId;
    toastEl.className = 'toast';
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    
    toastEl.innerHTML = `
        <div class="toast-header bg-warning text-dark">
            <i class="fas fa-keyboard me-2"></i>
            <strong class="me-auto">Raccourci Clavier</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    toastContainer.appendChild(toastEl);
    
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();
    
    // Retirer le toast après qu'il soit caché
    toastEl.addEventListener('hidden.bs.toast', function() {
        toastEl.remove();
    });
}
