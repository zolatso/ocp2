# Comment utiliser les scripts pour extraire des données et des images

## phase1.py
Ce script vous permet de creer un seul fichier csv qui contient les données d'un seul livre.
Il faut preciser le URL d'un livre dans la variable 'url'
Quand vous executez le code, un fichier csv au nom de example.csv sera crée dans le dossier du projet.

## phase2.p2
Pour faire marcher ce script, il faut passer le URL d'une categorie de livres du site-web à la fonctionne get_books_from_category.
Cette fonction sera initialise dans la variable get_urls.
Quand vous executez le code, comme dans phase1.py, un fichier csv au nom de example.csv sera crée dans le dossier du projet.
La difference c'est que cette fois ce csv contiendra les données de tous les livres de la categorie selectionée.

## phase3.py
Avec ce script, il faut preciser le URL du homepage du site dans la variable list_of_cats, qui appelle la fonction get_category_url_and_name.
Quand vous executez le code, le script va créer un fichier pour chaque categorie, dans lequel se trouvera un fichier csv. 
Ce ficher contiendra les données de tous les livres d'une seule categorie.
Notez que il y aura un dossier "images" dans chaque dossier de categorie, mais ça reste vide pour l'instant.

## phase4.py
Ce script fonctionne dans la meme maniere que le precedent.
La seule difference c'est que cette fois les images vont etre telecharger et stocker dans le dossier "images" de chaque categorie.
Les fichiers images sont nommées avec le "universal product code." 
Ca veut dire que vous pouvez facilement matcher les images avec les données dans les csv en utiliant le upc comme terme de recherche.