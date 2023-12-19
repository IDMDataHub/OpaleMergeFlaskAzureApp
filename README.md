OpaleMergeFlaskAzureApp
Description Brève

OpaleMergeFlaskAzureApp est une application web polyvalente conçue pour fusionner des fichiers CSV en utilisant Flask, optimisée pour un déploiement sur Azure. Cet outil facilite la manipulation de données en permettant aux utilisateurs de télécharger, traiter et fusionner divers fichiers CSV en un format unifié, le rendant idéal pour les analystes de données et toute personne gérant de grands ensembles de données.
Fonctionnalités

    Téléchargement de Fichiers CSV : Permet aux utilisateurs de télécharger plusieurs fichiers CSV pour traitement.
    Gestion des Colonnes : Détecte et gère automatiquement différentes structures de colonnes telles que 'initiales_nom' et 'numero_patient'.
    Préfixage des Colonnes : Ajoute automatiquement des préfixes aux noms des colonnes en fonction de l'ordre des fichiers, facilitant l'identification après la fusion.
    Fusion de Fichiers CSV : Fusionne plusieurs fichiers CSV téléchargés en un seul fichier consolidé.
    Téléchargement du Fichier Fusionné : Les utilisateurs peuvent télécharger le fichier CSV fusionné directement depuis l'interface web.

Installation

Pour installer ce projet localement, suivez ces étapes :

    Clonez le dépôt :

    bash

git clone [url-du-dépôt]

Installez les dépendances requises :

bash

    pip install -r requirements.txt

Utilisation

Pour exécuter l'application Flask :

bash

python app.py

Accédez à l'application web via localhost:5000 dans votre navigateur web.
Points d'Accès

    Accueil (/) : Page de destination pour le téléchargement de fichiers.
    Téléchargement (/upload) : Point d'accès pour le téléchargement et le traitement des fichiers CSV.
    Téléchargement (/download) : Point d'accès pour télécharger le fichier CSV fusionné.

Bibliothèques Utilisées

    pandas : Pour la manipulation de DataFrame.
    Flask : Framework web pour gérer les requêtes HTTP et le rendu des templates.
    os, io : Utilitaires pour les opérations de fichiers et d'entrée/sortie.

Contribution

Les contributions sont les bienvenues ! Pour les changements majeurs, veuillez ouvrir un problème d'abord pour discuter de ce que vous souhaitez changer.
Licence

Ce projet est sous licence MIT.
Auteur

Maxime Jacoupy