import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import csv
import random



# définition de la classe Notaire (nom, email, adresse, telephone, url)
class Notaire:
    def __init__(self, nom, email, adresse, telephone, url):
        self.nom = nom
        self.adresse = adresse
        self.email = email
        self.url = url
        self.telephone = telephone

    def __repr__(self):
        return f"{self.nom}, {self.adresse}, {self.email}, {self.telephone}, {self.url}"



#Fonctions pour parcourir toutes les pages
def get_pages_url(nb_pages):
    urls_pages = ["https://www.notaires.fr/fr/directory/notaries?location=toulouse&lat=43.604082&lon=1.433805&locality=Toulouse&postal_code=31000&search_id=MXWMHT7reKwzkXKL_YR7aJlHas42yo66EYecN14-kA8"]
    for i in range(1, nb_pages):
        url = f"{urls_pages[0]}&page={i}"
        urls_pages.append(url)
    return urls_pages
#ok fonction pour récupérer l'url de chaque notaire d'une page de liste des notaires
def get_notaire_url(url_page):
    try:
        # Récupérer le contenu HTML de la page
        response = requests.get(url_page)
        response.raise_for_status()  # Vérifie si la requête a réussi (code 200)

        # Analyser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Récupère tous les liens <a> avec la classe "arrow-link" et le texte "Plus d'infos"
        links = soup.find_all('a', class_='arrow-link', string="Plus d'infos")

        # Extraire les Urls de links dans une liste
        urls = []
        for link in links:
            urls.append(f"https://www.notaires.fr{link["href"]}")

        return list(set(urls))  # Retirer les doublons en utilisant set() puis convertit en liste

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de l'URL de page : {url} - {e}")
        return []

def get_notaire_info(url):
    try:

        # Utiliser un User-Agent pour éviter d'être bloqué par le serveur
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        #Récupérer le contenu HTML de la page
        response=requests.get(url,headers=headers)

        # Vérifie si la requête a réussi (code 200)
        response.raise_for_status()  

        # Vérifie si le serveur a renvoyé une erreur 429 (Trop de requêtes)
        # Si le serveur renvoie une erreur 429, on attend avant de réessayer
        if response.status_code == 429:
            print("Trop de requêtes, pause de 5 minutes...")
            time.sleep(30) 

        #analyser le contenu avec beautifulSoup
        soup=BeautifulSoup(response.text,'html.parser')

        #trouver l'email 
        email=soup.find("a",class_="btn-sheet btn-size--size-m btn-sheet--mail")['href'].replace("mailto:","").strip() if soup.find("a",class_="btn-sheet btn-size--size-m btn-sheet--mail") else None

        #trouver le numéro de téléphone
        telephone=soup.find("div",class_="office-sheet__phone field--telephone").find("a")['href'].replace("tel:","").strip() if soup.find("div",class_="office-sheet__phone field--telephone") else None
  
        # Trouver le nom du notaire
        nom=soup.find("div",class_="notary-card__line").find_all("p")[1].text.strip() if soup.find("div",class_="notary-card__line") else None

        # Trouver l'adresse du notaire
        adresse=soup.find("p",class_="address") if soup.find("p",class_="address") else None

        adresse_line1=adresse.find("span",class_="address-line1").text.strip() if adresse and adresse.find("span",class_="address-line1") else ""
        postal_code=adresse.find("span",class_="postal-code").text.strip() if adresse and adresse.find("span",class_="postal-code") else ""
        locality=adresse.find("span",class_="locality").text.strip() if adresse and adresse.find("span",class_="locality") else ""
        country=adresse.find("span",class_="country").text.strip() if adresse and adresse.find("span",class_="country") else ""
        adresse=adresse_line1 + ", " + postal_code +" "+ locality + ", " + country

        # Créer une instance de la classe Notaire
        notaire=Notaire(nom,email,adresse,telephone,url)
        return notaire
    
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de l'URL : {url} - {e}")
        return None

# Fonction pour extraire les urls des pages de tous les notaires
def get_all_urls():


    # liste d'URLs à scraper
    urls = []

    for url in get_pages_url(30):
        urls.extend(get_notaire_url(url))
        sleep(0.5)  # Pause de 0.5 secondes entre les requêtes pour éviter de surcharger le serveur
    
    # Enregistrer les urls de chaque page sur un fichier annexe
    with open("urls.txt","w") as file:
        for url in urls:
            file.write(url + "\n")
    return urls

# Enregistrer les informations du notaire dans un fichier CSV
def write_notaire_info(notaire,fichier="notaire.csv"):
    
    with open(fichier, "a", newline='',encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([notaire.nom,  notaire.email ,notaire.adresse, notaire.telephone, notaire.url])

#Enregistrer les informations de tous les notaires dans un fichier CSV
def save_all_notaire_info(fichier_urls,fichier_notaire="notaire.csv"):

    #créer le fichier CSV et écrire l'en-tête
    with open(fichier_notaire, "w", newline='',encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Nom", "Email", "Adresse", "Téléphone", "URL"])

    # Récupérer les urls des notaires depuis urls.txt
    with open("urls.txt",'r') as file:
        urls=file.readlines()
        urls=[url.strip() for url in urls]

    # Ajouter les infos de chaque notaire dans le fichier CSV
    i=0
    for url in urls :
        i+=1
        notaire=get_notaire_info(url)

        if notaire:
            with open(fichier_notaire, "a", newline='',encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([notaire.nom,  notaire.email ,notaire.adresse, notaire.telephone, notaire.url])
        else:
            print(f"Erreur lors de la récupération des informations pour l'URL : {url}")
    
        sleep(4) if i%10==0 else sleep(random.uniform(0.1,1))  # Pause de 4 secondes après chaque 10 notaires pour éviter de surcharger le serveur, sinon 0.5 secondes entre les requêtes

csv_notaire="notaire.csv"
save_all_notaire_info("urls.txt",csv_notaire)

