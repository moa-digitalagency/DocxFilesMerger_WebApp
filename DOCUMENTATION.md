# 📚 DocxFilesMerger - Documentation Complète 🏥

## 📖 Guide Utilisateur

### 🚀 Installation et prérequis

Pour utiliser l'application DocxFilesMerger, vous avez besoin de :

1. **Un navigateur web moderne** 🌐
   - Google Chrome (v88+)
   - Mozilla Firefox (v86+)
   - Microsoft Edge (v88+)
   - Safari (v14+)

2. **Connexion Internet** 🔌
   - Une connexion stable est recommandée pour le téléversement de gros fichiers

### 📥 Préparation de vos fichiers

Pour une utilisation optimale de l'application :

1. **Format d'archive** : Utilisez uniquement des fichiers .ZIP (pas de RAR, 7z, etc.)
2. **Contenu de l'archive** : 
   - L'archive doit contenir des fichiers .doc ou .docx
   - Tous les autres types de fichiers seront ignorés
   - La structure des dossiers à l'intérieur de l'archive n'a pas d'importance
3. **Taille maximale** : 
   - L'application accepte des archives jusqu'à 300 Mo
   - Pour les fichiers plus volumineux, divisez-les en plusieurs archives

### 🔄 Utilisation de l'application

#### Étape 1 : Téléversement de l'archive

1. Accédez à l'application via votre navigateur
2. Sur la page d'accueil, cliquez sur le bouton "Parcourir les fichiers" ou glissez-déposez votre archive ZIP dans la zone indiquée
   ```
   💡 RACCOURCI : Utilisez Ctrl+O pour ouvrir le sélecteur de fichiers rapidement
   ```
3. Sélectionnez votre archive ZIP et confirmez

#### Étape 2 : Traitement des fichiers

1. Après le téléversement, l'application démarre automatiquement le traitement
2. Une barre de progression s'affiche avec des messages d'état
3. La durée de traitement dépend du nombre de fichiers dans l'archive :
   - Moins de 100 fichiers : quelques secondes
   - 100-1000 fichiers : 1-5 minutes
   - Plus de 1000 fichiers : 5-20 minutes
   ```
   💡 ASTUCE : Vous pouvez annuler le traitement à tout moment en appuyant sur la touche Échap
   ```

#### Étape 3 : Téléchargement des résultats

1. Une fois le traitement terminé, deux options de téléchargement s'affichent :
   - Document fusionné au format DOCX
   - Document fusionné au format PDF
2. Cliquez sur le bouton correspondant au format souhaité
   ```
   💡 RACCOURCIS : 
   - Ctrl+D pour télécharger la version DOCX
   - Ctrl+P pour télécharger la version PDF
   ```
3. Pour traiter un autre fichier, cliquez sur "Traiter un autre fichier" ou utilisez le raccourci Ctrl+R

### 🛠️ Raccourcis clavier

Pour une utilisation plus rapide, l'application propose plusieurs raccourcis clavier :

| Raccourci | Action |
|-----------|--------|
| <kbd>Ctrl</kbd> + <kbd>O</kbd> | Ouvrir le sélecteur de fichiers |
| <kbd>Esc</kbd> | Annuler l'opération en cours |
| <kbd>Ctrl</kbd> + <kbd>D</kbd> | Télécharger le document DOCX |
| <kbd>Ctrl</kbd> + <kbd>P</kbd> | Télécharger le document PDF |
| <kbd>Ctrl</kbd> + <kbd>R</kbd> | Réinitialiser l'application |
| <kbd>Ctrl</kbd> + <kbd>H</kbd> | Afficher l'aide des raccourcis |

```
💡 ASTUCE : Appuyez sur Ctrl+H à tout moment pour afficher la liste des raccourcis disponibles
```

### 🔍 Structure du document fusionné

Le document de sortie présente les caractéristiques suivantes :

1. **Organisation** :
   - Chaque document original est intégré dans l'ordre alphabétique
   - Une séparation claire est ajoutée avant chaque document

2. **Séparateurs** :
   - Format : `<NOMFICHIER.extension>....................................`
   - Police : Courier New, 12pt, Gras
   - Couleur : Bleu foncé

3. **Mise en page** :
   - Format : A4 (210 x 297 mm)
   - Marges : 2,5 cm sur tous les côtés
   - Orientation : Portrait

## 🚨 Dépannage

### Problèmes courants et solutions

| Problème | Cause possible | Solution |
|----------|----------------|----------|
| **Erreur lors du téléversement** | Archives trop volumineuses | Divisez votre archive en fichiers plus petits (<300 Mo) |
| **Message "Format non supporté"** | L'archive n'est pas au format ZIP | Convertissez votre archive au format ZIP |
| **Aucun document n'est extrait** | Les fichiers ne sont pas au format .doc/.docx | Vérifiez le contenu de votre archive |
| **Conversion PDF incomplète** | Problème avec la mise en forme complexe | Le format DOCX conserve mieux la mise en forme |
| **Tables ou images manquantes** | Problème de compatibilité des formats | Essayez d'utiliser des formats .docx plutôt que .doc |
| **Erreur "Application indisponible"** | Le serveur est surchargé | Réessayez ultérieurement ou contactez le support |

### Comment signaler un problème

Si vous rencontrez un problème non répertorié ci-dessus :

1. Notez l'étape précise à laquelle l'erreur s'est produite
2. Capturez l'écran affichant le message d'erreur (si possible)
3. Décrivez le problème avec le plus de détails possible
4. Envoyez ces informations par email à : moa@myoneart.com

## 💼 Cas d'utilisation avancés

### Traitement par lots

Pour traiter un très grand nombre de dossiers médicaux :

1. **Préparation** :
   - Divisez vos fichiers en plusieurs archives ZIP de taille raisonnable (100-300 Mo)
   - Nommez les archives de manière séquentielle (ex: dossiers_medicaux_part1.zip, dossiers_medicaux_part2.zip)

2. **Traitement** :
   - Traitez chaque archive séparément
   - Téléchargez et conservez les fichiers DOCX générés

3. **Fusion finale (optionnelle)** :
   - Utilisez un logiciel de traitement de texte comme Microsoft Word ou LibreOffice Writer
   - Ouvrez le premier document DOCX
   - Utilisez la fonction "Insérer" > "Texte d'un fichier" pour ajouter les autres documents

### Optimisation pour systèmes lents

Si vous utilisez l'application sur un système avec des ressources limitées :

1. Fermez les autres applications et onglets du navigateur
2. Traitez de plus petites archives à la fois (50-100 fichiers maximum)
3. Privilégiez les formats DOCX qui sont plus rapides à traiter que les DOC

## 📋 Respect de la confidentialité

L'application DocxFilesMerger a été conçue dans le respect de la confidentialité des données médicales :

1. **Traitement local** :
   - Tous les fichiers sont traités sur le serveur de l'application
   - Aucune donnée n'est envoyée à des services externes

2. **Suppression automatique** :
   - Les fichiers téléversés sont automatiquement supprimés après 24 heures
   - Vous pouvez demander la suppression immédiate en contactant le support

3. **Sécurité** :
   - Connexion HTTPS sécurisée
   - Aucune information personnelle n'est collectée ou stockée

## 🔗 Ressources supplémentaires

### Vidéos tutorielles

- [Guide de démarrage rapide](https://myoneart.com/docxfilesmerger/tutoriel-rapide) (2 minutes)
- [Traitement de grands volumes de données](https://myoneart.com/docxfilesmerger/tutoriel-avance) (5 minutes)
- [Dépannage des problèmes courants](https://myoneart.com/docxfilesmerger/depannage) (3 minutes)

### Documentation technique

Pour les administrateurs système et les développeurs, une documentation technique complète est disponible sur demande.

### Formation et support

Pour les grands établissements médicaux, nous proposons des sessions de formation personnalisées.
Contactez-nous à moa@myoneart.com pour plus d'informations.

## 📞 Contact et support

**MOA Digital Agency LLC**  
Site web : [https://myoneart.com](https://myoneart.com)  
Email : [moa@myoneart.com](mailto:moa@myoneart.com)

---

*© 2025 MOA Digital Agency LLC. Tous droits réservés.*