#  Projet Data Engineering  



## Introduction :
-------------

L'objectif de ce projet est de réaliser une application web à l'aide de Flask et de Mongo qui recense des annonces qu'on a au préalable scrapé avec scrapy, et de réaliser une analyse des donnés avec un dashoard interactif.

## USER GUIDE :
-------------

Pour pouvoir accéder au dashboard, vous devez : 

1. Cloner notre projet sur votre machine.

2. Allez dans le répertoire où se trouve le fichier cloné à l'aide du terminal, puis taper sur le terminal la commande : __docker-compose  up__.

3. Attendre quelques minutes le temps que ca finisse de scrapper.

4. Aller sur le lien : http://localhost:5001/ 


## Devopleur Guide :

-------------

Le fichier principal est le fichier __app.py__ . Le fichier __app.py__ permet de lancer le scrapping, de stocker les données du scrapping dans un fichier data. et contient tout le code relatif à mongo et à Flask.


## Scrapping :

-------------

Pour le scrapping on s'est servi de la librairie __scrapy__ pour scrapper le site 'https://www.autoeasy.fr/acheter', on a utilisé un seul spiders et on a du configurer le pipline afin de rendre le scrapping d'image plus facile.


## MONGO :

-------------

On s'est servi de la base de données no-SQL mongoDB à l'aide de pymongo.Tout ce qui est obtenue sur le site découle de requêtes sur notre base mongo. 

## Flask :

-------------

Pour la partie flask, il y a un fichier __app.py__ qui contient le code nécéssaire au déploiement de l'application web.
Il y deux dossier: un dossier templates qui contient tout les codes HTML,un dossier static qui contient la partie CSS et l'image de notre application web.



