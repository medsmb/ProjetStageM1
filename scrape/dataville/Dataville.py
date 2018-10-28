#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
© 2018 Mohammed BENAOU & Mohammed RASFA ALL RIGHTS RESERVED
Sous l'encadrement de Mr.Sylvian dejean

"""
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
import os, os.path, csv
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')


#Création du fichier DataVille.csv oû on va stoker les informations
#note fichier contient :
"""
1_L'identifiant des données
2_La Ville concernée
3_La pérdiode
4_Le nombre d’annonces dans la ville au 1er septembre 2017
5_Le nombre de voyageurs accueillis entre septembre 2016 et septembre 2017
6_Le nombre de pays dont sont originaires les voyageurs qui y ont séjourné
7_Le revenu annuel médian d’un hôte dans la commune
8_Le lien qui mène vers la page

"""
# DÉBUT DE PROGRAMME
class MyTestCase():

    def main(self):
        start_time = time.time()
        f = csv.writer(open('DataVille_France.xls', 'w'))
        f.writerow(['ID','Région','INSEE','Ville','Période','Nombre annonces','Nombre voyageur','Nationalité voyageur','Revenue Annuel','Lien vers la page'])

        REGION=[]
        VILLE=[] # la lise des villes récupérée à partir le fichier CommunesNA.csv fournie par 
        URLS=[] #la liste des urls
        INSEE=[] #la liste des départements
        ID=1 # l'identifiant des données
        """
        Ps : pour ajouter des nouvelles communes il suffie juste de les ajouter 
            dans le fichiers CommunesNA.csv (Communes de la Nouvelle-Aquitaine) 
        """
        #Lécture de fichier pour récupérer toutes les communes de la Nouvelle-Aquitaine
        with open('communes_france.csv','rb') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader) # supression des entêtes
            for row in csv_reader:
                REGION.append(row[0])
                INSEE.append(row[1]+row[2]) #l'ajout des département à la liste convenable
                # ce test nous permet de savoir si le nom de la ville s'écrit en deux parties (ex: La Rochelle) 
                if row[4] in (None, ""): 
                    city=row[3]
                else:
                    #la définition des expressions réqulières permettant d'adapter le lien de recherche
                    city=row[4]+row[3]
                    city = city.replace("(", "")
                    city = city.replace(")", "-")
                    city = city.replace("'", "-")
                    city=city.encode('utf-8')
                VILLE.append(city.lower())#l'ajout des ville à la liste convenable
                #Parcourire la liste de villes et l'envoie des urls à la liste dédiée 
            for ville in VILLE:
                
                URLS.append('https://dataville.byairbnb.com/city/'+str(ville[0:1])+'/'+str(ville)+'-city.html')
        #Parcourir la liste des URLS
        for region,insee,ville,url in zip(REGION,INSEE,VILLE,URLS):
            try:
                url = url.decode('utf8')
                response = requests.get(url) 
                #encodedText = response.text.encode("latin-1")
                soup = BeautifulSoup(response.text, "html.parser") #l'extraction des données a l'aide de la bibiothèque BeautifulSoup
                #Ce test permet de vérifier l'éxistance de url
                if response.status_code == 200: #si l'url existe
                    for item in list(zip(soup.find_all("dd")[0::3],soup.find_all("dd")[1::3],soup.find_all("dd")[2::3],soup.find_all("dd")[3::3])):
                        try:
                            rentals, travlers,national,revenue = item
                            rentals=rentals.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                            travlers=travlers.string.encode('utf-8') # Le nombre de voyageurs accueillis entre septembre 2016 et septembre 2017
                            national=national.string.encode('utf-8') # Le nombre de pays dont sont originaires les voyageurs qui y ont séjourné
                            revenue=revenue.string.encode('utf-8') # Le revenu annuel médian d’un hôte dans la commune
                            #print ', '.join([rentals, travlers,national,revenue])
                        except NavigableString: 
                            pass
            # si l'url n'existe pas donc il n'y pas de données concenant cette ville
                else :
                    rentals="Aucun résultat"
                    travlers="Aucun résultat"
                    national="Aucun résultat"
                    revenue="Aucun résultat"
                    #print 'le site n\'existe pas'
                # récupération du nom de la ville à partir le url
                #start,end=url.find('/city/'), url.find('-city')
                #City=url[start+8:end]
                print str(ville) +" , "+str(insee)+" , "+str(ID)
                Date='01/09/2016 au 01/09/2017' # ces données sont valides juste pour cette période 
                #l'écreture de résultat dans le fichier DataVille.csv
                f.writerow([ID,region,insee,ville,Date,rentals,travlers,national,revenue,url.encode('utf-8')])
                ID+=1 # l'incémentation de l'identifiant de page
                #f.close() #fermeture de fichier
            except NavigableString: 
                    pass
        print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    MyTestCase().main()