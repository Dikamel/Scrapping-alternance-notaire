**Objectif** : Scrapper les infos publiques de notaires, puis d'envoyer de manière automatique des emails de prospection pour trouver une alternance.

**Fichiers** : Je ne maîtrise pas parfaitement le versionning git, mais en résumé : 

Version 0 :

  urls.txt : fichier contenant l'url de chaque page web du site notaires.fr de chaque notaire de Toulouse (fichier crée  à partir d'un bout de code de main.py)
  main.py : fichier principal qui utilise chaque url de urls.txt pour venir récupérer les infos de base (et publiques) des notaires, puis l'inscrire dans le fichier notaires.csv
  notaires.csv : tableau des infos de tous les notaires de urls.txt sous le format [Nom,	Email,	Adresse,	Téléphone,	URL]

Version 1 : 

  scrapping.py : version légèrement modifiée pour la visibilité de main.py
  emailing.py : programme qui permet d'envoyer un email unique individuellement à chaque adresse écrite dans un fichier csv 
  
