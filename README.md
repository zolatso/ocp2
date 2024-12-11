# Comment utiliser les scripts pour extraire des données et des images

## Installation de l'environnement virtuel

Pour créer un environnement virtuel, utilisez le module Python `venv`. Une fois le dépôt Git cloné sur votre machine locale, ouvrez un terminal pour procéder à la création de l'environnement.

Dans le répertoire contenant le projet, exécutez la commande suivante (cest possible qui vous devez utilisez python3 s'il y a aussi une version de Python 2 installé sur votre machine):
```bash
python -m venv env
```

### Activation de l'environnement virtuel :
- **Mac/Linux** : 
  ```bash
  source env/bin/activate
  ```
- **Windows** :
  ```bash
  .\env\Scripts\activate
  ```

Une fois l'environnement activé, installez les dépendances du projet en exécutant la commande suivante :
```bash
pip install -r requirements.txt
```

Cela téléchargera et installera tous les modules spécifiés dans le fichier `requirements.txt`.

**Remarque :** Si vous utilisez Visual Studio Code, ce processus peut être encore plus simple. L'éditeur vous proposera automatiquement de créer un environnement virtuel et d’installer les modules listés dans `requirements.txt`.

## phase1.py
Ce script permet de créer un fichier CSV contenant les données d'un seul livre.

Configuration :
Spécifiez l'URL du livre dans la variable url.
Exécution :
Lorsque vous exécutez le script, un fichier CSV nommé example.csv sera généré dans le répertoire du projet.

## phase2.py
Ce script permet d'extraire les données de tous les livres d'une catégorie.

Configuration :
Fournissez l'URL d'une catégorie de livres à la fonction get_books_from_category.
Cette fonction initialise la variable get_urls.
Exécution :
Comme pour phase1.py, un fichier CSV nommé example.csv sera créé dans le répertoire du projet.
Cette fois, le CSV contiendra les données de tous les livres appartenant à la catégorie spécifiée.


## phase3.py
Ce script permet d'extraire les données de toutes les catégories de livres disponibles sur le site.

Configuration :
Spécifiez l'URL de la page d'accueil du site dans la variable list_of_cats, utilisée par la fonction get_category_url_and_name.
Exécution :
Le script génère un dossier pour chaque catégorie.
Chaque dossier contient un fichier CSV regroupant les données de tous les livres de cette catégorie.
Un sous-dossier images est également créé dans chaque dossier de catégorie, mais il restera vide à cette étape.


## phase4.py
Ce script fonctionne de manière similaire à phase3.py, avec une fonctionnalité supplémentaire : le téléchargement des images des livres.

Configuration et exécution :
Les dossiers et fichiers CSV sont générés comme dans phase3.py.
Les images des livres sont téléchargées dans le dossier images de chaque catégorie.
Les fichiers images sont nommés à l'aide du Universal Product Code (UPC).
Astuce :
Vous pouvez facilement associer les images aux données des fichiers CSV en recherchant le UPC correspondant.