// UI Elements
let dropZone = document.getElementById('drop-zone');
let fileInput = document.getElementById('file-input');
let uploadForm = document.getElementById('upload-form');
let uploadButton = document.getElementById('upload-button');
let progressContainer = document.querySelector('.progress-container');
let progressBar = document.getElementById('progress-bar');
let progressText = document.getElementById('progress-status');
let progressPercent = document.getElementById('progress-percentage');
let alertContainer = document.getElementById('alert-container');
let resultsContainer = document.getElementById('result-container');
let resetButton = document.getElementById('reset-button');

// Éléments de téléchargement qui seront créés dynamiquement
let docxDownloadBtn = null;
let pdfDownloadBtn = null;

// Variables for tracking state
let uploadStatus = 'idle'; // 'idle', 'uploading', 'processing', 'complete', 'error'
let statusCheckInterval = null;

// Initialize the upload interface
function setupDropZone() {
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    
    // Handle drag enter and leave
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });
    
    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);
    
    // Handle manual file selection
    fileInput.addEventListener('change', () => {
        handleFiles(fileInput.files);
    });
    
    // Reset button functionality
    if (resetButton) {
        resetButton.addEventListener('click', resetApplication);
    }
}

function setupForm() {
    uploadForm.addEventListener('submit', (e) => {
        e.preventDefault();
        if (fileInput.files.length > 0) {
            handleFiles(fileInput.files);
        } else {
            showAlert('Veuillez sélectionner un fichier ZIP à téléverser.', 'warning');
        }
    });
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight() {
    dropZone.classList.add('active');
}

function unhighlight() {
    dropZone.classList.remove('active');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

function handleFiles(files) {
    if (files.length > 0) {
        const file = files[0];
        
        // Check if it's a ZIP file
        if (file.type === 'application/zip' || file.name.toLowerCase().endsWith('.zip')) {
            uploadFile(file);
        } else {
            showAlert('Veuillez téléverser un fichier ZIP valide.', 'danger');
        }
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Octets';
    
    const k = 1024;
    const sizes = ['Octets', 'Ko', 'Mo', 'Go'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showAlert(message, type = 'info') {
    // Clear previous alerts
    alertContainer.innerHTML = '';
    
    // Create the alert
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.role = 'alert';
    
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Add to the container
    alertContainer.appendChild(alert);
    alertContainer.scrollIntoView({ behavior: 'smooth' });
}

function uploadFile(file) {
    if (uploadStatus === 'uploading' || uploadStatus === 'processing') {
        showAlert('Un fichier est déjà en cours de traitement. Veuillez patienter.', 'warning');
        return;
    }
    
    // Update status
    uploadStatus = 'uploading';
    updateProgressUI(5, 'Téléversement du fichier...', 'upload');
    
    // Create form data
    const formData = new FormData();
    formData.append('file', file);
    
    // Send the file to the server
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Échec du téléversement');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            updateProgressUI(20, 'Téléversement terminé. Démarrage du traitement...', 'upload_complete');
            startProcessing(data.zip_path, data.file_count);
        } else {
            throw new Error(data.error || 'Échec du téléversement');
        }
    })
    .catch(error => {
        uploadStatus = 'error';
        updateProgressUI(0, 'Erreur lors du téléversement : ' + error.message, 'error');
        console.error('Upload error:', error);
    });
}

function startProcessing(zipPath, fileCount) {
    // Update status
    uploadStatus = 'processing';
    
    // Send request to start processing
    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            zip_path: zipPath
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Échec du démarrage du traitement');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Start checking status
            startStatusCheck(fileCount);
        } else {
            throw new Error(data.error || 'Échec du démarrage du traitement');
        }
    })
    .catch(error => {
        uploadStatus = 'error';
        updateProgressUI(0, 'Erreur lors du démarrage du traitement : ' + error.message, 'error');
        console.error('Processing error:', error);
    });
}

function startStatusCheck(fileCount) {
    // Clear any existing interval
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }
    
    // Set up status checking
    statusCheckInterval = setInterval(() => {
        checkProcessingStatus(fileCount);
    }, 2000); // Check every 2 seconds
}

function checkProcessingStatus(fileCount) {
    fetch('/status')
        .then(response => {
            if (!response.ok) {
                if (response.status === 404) {
                    // Status file not found, keep waiting
                    console.log("Fichier de statut introuvable");
                    return null;
                }
                return response.json().then(data => {
                    throw new Error(data.error || 'Échec de la vérification du statut');
                });
            }
            return response.json();
        })
        .then(data => {
            if (!data) return; // Status file not ready yet
            
            console.log("Réponse du statut:", data);
            
            // Vérifier si le traitement est terminé ou en erreur
            if (data.complete === true) {
                uploadStatus = 'complete';
                updateProgressUI(100, 'Traitement terminé !', 'complete');
                
                // Stop the interval
                if (statusCheckInterval) {
                    clearInterval(statusCheckInterval);
                    statusCheckInterval = null;
                }
                
                // Display stats
                showResults(data);
                return;
            }
            
            if (data.current_step === 'error') {
                uploadStatus = 'error';
                updateProgressUI(0, `Erreur lors du traitement : ${data.error || 'Erreur inconnue'}`, 'error');
                
                // Stop the interval
                if (statusCheckInterval) {
                    clearInterval(statusCheckInterval);
                    statusCheckInterval = null;
                }
                return;
            }
            
            // Mettre à jour l'UI en fonction de l'étape actuelle
            if (data.percent !== undefined && data.status_text) {
                updateProgressUI(data.percent, data.status_text, data.current_step);
                return;
            }
            
            // Format legacy - pour rétrocompatibilité
            switch (data.current_step) {
                case 'extract':
                    updateProgressUI(10, 'Extraction des fichiers de l\'archive ZIP...', 'process');
                    break;
                    
                case 'convert':
                    updateProgressUI(30, 'Conversion des fichiers...', 'process');
                    break;
                    
                case 'merge':
                    updateProgressUI(50, 'Fusion des documents...', 'process');
                    break;
                    
                case 'pdf':
                    updateProgressUI(80, 'Conversion du document en PDF...', 'process');
                    break;
                    
                case 'complete':
                    uploadStatus = 'complete';
                    updateProgressUI(100, 'Traitement terminé !', 'complete');
                    
                    // Stop the interval
                    if (statusCheckInterval) {
                        clearInterval(statusCheckInterval);
                        statusCheckInterval = null;
                    }
                    
                    // Display stats
                    showResults(data);
                    break;
                    
                case 'error':
                    uploadStatus = 'error';
                    updateProgressUI(0, `Erreur lors du traitement : ${data.error || 'Erreur inconnue'}`, 'error');
                    
                    // Stop the interval
                    if (statusCheckInterval) {
                        clearInterval(statusCheckInterval);
                        statusCheckInterval = null;
                    }
                    break;
                    
                default:
                    // Unknown status, log it
                    console.log("Statut inconnu :", data.current_step);
            }
        })
        .catch(error => {
            console.error('Erreur lors de la vérification du statut:', error);
            // On error, don't stop checking - might be a temporary issue
        });
}

// Messages motivants selon le pourcentage d'avancement
const motivationalMessages = [
    { min: 0, max: 20, message: "C'est parti ! 🚀" },
    { min: 20, max: 40, message: "Bonne progression ! ⭐" },
    { min: 40, max: 60, message: "Vous êtes sur la bonne voie ! 👍" },
    { min: 60, max: 80, message: "Plus que quelques minutes... 🙌" },
    { min: 80, max: 95, message: "On y est presque ! 🎯" },
    { min: 95, max: 100, message: "Mission accomplie ! 🏆" }
];

// Obtenir un message motivant en fonction du pourcentage
function getMotivationalMessage(percent) {
    for (const item of motivationalMessages) {
        if (percent >= item.min && percent <= item.max) {
            return item.message;
        }
    }
    return "";
}

function updateProgressUI(percent, statusText, step) {
    // Show progress container
    progressContainer.style.display = 'block';
    
    // Update progress bar
    progressBar.style.width = `${percent}%`;
    progressBar.setAttribute('aria-valuenow', percent);
    
    // Update text
    progressText.textContent = statusText;
    
    // Ajouter le pourcentage
    if (progressPercent) {
        progressPercent.textContent = `${Math.round(percent)}%`;
    }
    
    // Ajouter un message motivant
    const motivationMsg = getMotivationalMessage(percent);
    if (motivationMsg && document.getElementById('motivation-message')) {
        document.getElementById('motivation-message').textContent = motivationMsg;
        document.getElementById('motivation-message').style.display = 'block';
    }
    
    // Animer la mascotte en fonction du pourcentage
    const mascot = document.getElementById('upload-mascot');
    if (mascot) {
        // Ajuster l'état de la mascotte en fonction de l'étape
        if (step === 'error') {
            mascot.src = '/static/img/mascot-sad.svg';
            mascot.alt = "Mascotte triste";
            mascot.classList.remove('jumping', 'dancing');
            mascot.classList.add('shaking');
        } else if (step === 'complete') {
            mascot.src = '/static/img/mascot-happy.svg';
            mascot.alt = "Mascotte heureuse";
            mascot.classList.remove('shaking', 'jumping');
            mascot.classList.add('dancing');
        } else {
            mascot.src = '/static/img/mascot-working.svg';
            mascot.alt = "Mascotte au travail";
            mascot.classList.remove('shaking', 'dancing');
            mascot.classList.add('jumping');
            
            // Faire varier l'animation selon le pourcentage
            const animationDuration = Math.max(0.5, 2 - (percent / 100) * 1.5); // Plus rapide quand on approche de 100%
            mascot.style.animationDuration = `${animationDuration}s`;
        }
        
        // Assurez-vous que la mascotte est visible
        mascot.style.display = 'block';
    }
    
    // Set appropriate classes based on step
    progressBar.className = 'progress-bar';
    
    if (step === 'error') {
        progressBar.classList.add('bg-danger');
    } else if (step === 'complete') {
        progressBar.classList.add('bg-success');
        // Show the results section
        resultsContainer.style.display = 'block';
    } else {
        progressBar.classList.add('bg-primary', 'progress-bar-striped', 'progress-bar-animated');
    }
}

function showResults(data) {
    // Créer les boutons de téléchargement s'ils n'existent pas déjà
    if (!docxDownloadBtn || !pdfDownloadBtn) {
        // Vider le conteneur de résultats
        resultsContainer.innerHTML = '';
        
        // Créer une carte pour les résultats
        const resultCard = document.createElement('div');
        resultCard.className = 'card mb-4';
        
        // Contenu de la carte
        resultCard.innerHTML = `
            <div class="card-header bg-success text-white">
                <h5 class="card-title mb-0"><i class="fas fa-check-circle me-2"></i>Traitement terminé avec succès</h5>
            </div>
            <div class="card-body">
                <div class="alert alert-info">
                    <h5>Informations de traitement :</h5>
                    <ul>
                        <li>Fichiers traités : ${data.file_count || (data.stats ? data.stats.file_count : 'N/A')}</li>
                        <li>Temps de traitement : ${data.processing_time || (data.stats ? data.stats.processing_time : 'N/A')} secondes</li>
                    </ul>
                </div>
                
                <p>Vous pouvez maintenant télécharger le résultat dans les formats suivants :</p>
                
                <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                    <a href="/download/docx" class="btn btn-primary me-md-2" id="docx-download-btn">
                        <i class="fas fa-file-word me-2"></i>Télécharger le DOCX
                    </a>
                    <a href="/download/pdf" class="btn btn-danger" id="pdf-download-btn">
                        <i class="fas fa-file-pdf me-2"></i>Télécharger le PDF
                    </a>
                </div>
                
                <div class="d-grid gap-2 mt-3">
                    <button class="btn btn-outline-secondary" onclick="resetApplication()">
                        <i class="fas fa-redo me-2"></i>Traiter un autre fichier
                    </button>
                </div>
            </div>
        `;
        
        // Ajouter la carte au conteneur
        resultsContainer.appendChild(resultCard);
        
        // Mettre à jour les références des boutons
        docxDownloadBtn = document.getElementById('docx-download-btn');
        pdfDownloadBtn = document.getElementById('pdf-download-btn');
    }
}

function resetApplication() {
    // Reset UI state
    uploadStatus = 'idle';
    
    // Clear any ongoing status check
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
        statusCheckInterval = null;
    }
    
    // Reset file input
    if (fileInput) {
        fileInput.value = '';
    }
    
    // Hide progress and results
    progressContainer.style.display = 'none';
    resultsContainer.style.display = 'none';
    
    // Clear alerts
    alertContainer.innerHTML = '';
    
    // Reset progress bar
    progressBar.style.width = '0%';
    progressBar.setAttribute('aria-valuenow', 0);
    progressBar.className = 'progress-bar';
    
    // Disable download buttons
    if (docxDownloadBtn && pdfDownloadBtn) {
        docxDownloadBtn.classList.add('disabled');
        pdfDownloadBtn.classList.add('disabled');
    }
    
    // Reset results container content (but keep the download buttons)
    const downloadButtons = resultsContainer.querySelector('.btn-group');
    if (downloadButtons) {
        resultsContainer.innerHTML = '';
        resultsContainer.appendChild(downloadButtons);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupDropZone();
    setupForm();
});
