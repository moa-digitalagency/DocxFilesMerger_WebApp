/**
 * DocxFilesMerger - Application de traitement et fusion de documents.
 * Développé par MOA Digital Agency LLC (https://myoneart.com)
 * Email: moa@myoneart.com
 * Copyright © 2025 MOA Digital Agency LLC. Développé par Aisance Kalonji. Tous droits réservés.
 */

// Gestionnaire pour le tableau de bord d'administration
document.addEventListener('DOMContentLoaded', function() {
    // Récupérer les éléments DOM
    const refreshStatsBtn = document.getElementById('refresh-stats-btn');
    
    // Si le bouton existe, ajouter un événement de clic
    if (refreshStatsBtn) {
        refreshStatsBtn.addEventListener('click', function() {
            refreshStats();
        });
    }
    
    // Fonction pour actualiser les statistiques via AJAX
    function refreshStats() {
        // Afficher une indication visuelle que le rafraîchissement est en cours
        refreshStatsBtn.disabled = true;
        refreshStatsBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Actualisation...';
        
        // Effectuer une requête AJAX pour obtenir des statistiques mises à jour
        fetch('/admin/refresh_stats', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur réseau : ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            // Mettre à jour les statistiques globales
            updateGlobalStats(data.stats);
            
            // Mettre à jour la table des traitements récents
            updateRecentJobs(data.recent_jobs);
            
            // Mettre à jour les statistiques quotidiennes
            updateDailyStats(data.daily_stats);
            
            // Afficher une notification de succès
            showNotification('Statistiques actualisées avec succès', 'success');
        })
        .catch(error => {
            console.error('Erreur lors de l\'actualisation des statistiques:', error);
            showNotification('Erreur lors de l\'actualisation des statistiques : ' + error.message, 'danger');
        })
        .finally(() => {
            // Réactiver le bouton et restaurer son texte d'origine
            refreshStatsBtn.disabled = false;
            refreshStatsBtn.innerHTML = '<i class="fas fa-sync-alt me-2"></i> Actualiser les statistiques';
        });
    }
    
    // Fonction pour mettre à jour les statistiques globales
    function updateGlobalStats(stats) {
        const totalJobsEl = document.querySelector('.card:contains("Traitements totaux") h2');
        const totalFilesEl = document.querySelector('.card:contains("Fichiers traités") h2');
        const avgTimeEl = document.querySelector('.card:contains("Temps moyen") h2');
        
        if (totalJobsEl) totalJobsEl.textContent = stats.total_jobs;
        if (totalFilesEl) totalFilesEl.textContent = stats.total_files;
        if (avgTimeEl) totalJobsEl.textContent = stats.avg_time + 's';
    }
    
    // Fonction pour mettre à jour la table des traitements récents
    function updateRecentJobs(jobs) {
        const tableBody = document.getElementById('recent-jobs-table');
        const noJobsMessage = document.getElementById('no-jobs-message');
        
        if (!tableBody) return;
        
        // Vider le tableau
        tableBody.innerHTML = '';
        
        // Masquer/afficher le message "Aucun traitement récent"
        if (noJobsMessage) {
            noJobsMessage.style.display = jobs.length === 0 ? 'block' : 'none';
        }
        
        // Si aucun traitement, sortir
        if (jobs.length === 0) return;
        
        // Ajouter les nouvelles lignes
        jobs.forEach(job => {
            // Créer une ligne de tableau
            const tr = document.createElement('tr');
            
            // Formater la date
            const date = new Date(job.created_at);
            const formattedDate = `${date.getDate().toString().padStart(2, '0')}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getFullYear()} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
            
            // Déterminer la classe et le texte du badge en fonction du statut
            let badgeClass = 'bg-secondary';
            let statusText = job.status;
            
            if (job.status === 'completed') {
                badgeClass = 'bg-success';
                statusText = 'Terminé';
            } else if (job.status === 'error') {
                badgeClass = 'bg-danger';
                statusText = 'Erreur';
            } else if (job.status === 'processing') {
                badgeClass = 'bg-primary';
                statusText = 'En cours';
            }
            
            // Définir le contenu HTML de la ligne
            tr.innerHTML = `
                <td class="text-white">${job.id}</td>
                <td class="text-white text-truncate" style="max-width: 150px;">${job.original_filename || 'N/A'}</td>
                <td>
                    <span class="badge ${badgeClass}">${statusText}</span>
                </td>
                <td class="text-white">${job.file_count || 'N/A'}</td>
                <td class="text-white">${job.processing_time || 'N/A'}</td>
                <td class="text-white">${formattedDate}</td>
                <td class="text-center">
                    <div class="btn-group btn-group-sm">
                        <!-- Télécharger DOCX -->
                        ${job.status === 'completed' ? 
                            `<a href="/admin/download_job_file/${job.job_id}/docx" class="btn btn-outline-primary" title="Télécharger DOCX">
                                <i class="fas fa-file-word"></i>
                            </a>
                            <a href="/admin/download_job_file/${job.job_id}/pdf" class="btn btn-outline-danger" title="Télécharger PDF">
                                <i class="fas fa-file-pdf"></i>
                            </a>` :
                            `<button class="btn btn-outline-primary disabled" title="Fichier non disponible">
                                <i class="fas fa-file-word"></i>
                            </button>
                            <button class="btn btn-outline-danger disabled" title="Fichier non disponible">
                                <i class="fas fa-file-pdf"></i>
                            </button>`
                        }
                        <!-- Supprimer -->
                        <a href="/admin/delete_job/${job.id}" class="btn btn-outline-danger" 
                           onclick="return confirm('Êtes-vous sûr de vouloir supprimer ce traitement?');" title="Supprimer">
                            <i class="fas fa-trash-alt"></i>
                        </a>
                    </div>
                </td>
            `;
            
            // Ajouter la ligne au tableau
            tableBody.appendChild(tr);
        });
    }
    
    // Fonction pour mettre à jour les statistiques quotidiennes
    function updateDailyStats(stats) {
        // Implémenter si nécessaire
    }
    
    // Fonction pour afficher des notifications
    function showNotification(message, type = 'info') {
        // Créer l'élément de notification
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.top = '1rem';
        notification.style.right = '1rem';
        notification.style.zIndex = '1050';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        // Ajouter la notification au document
        document.body.appendChild(notification);
        
        // Supprimer automatiquement après 3 secondes
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    // Sélecteur JQuery personnalisé pour trouver un élément contenant un texte
    jQuery.expr[':'].contains = function(a, i, m) {
        return jQuery(a).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
    };
});