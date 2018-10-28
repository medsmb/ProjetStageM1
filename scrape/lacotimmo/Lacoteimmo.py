#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import time
import csv
import unittest
import sys
import datetime
import os.path
import pandas as pd


from datetime import datetime
from selenium import webdriver
from bs4 import NavigableString
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.errorhandler import ErrorHandler
from unidecode import unidecode

import unicodecsv
import codecs
reload(sys)
streamWriter = codecs.lookup('utf-8')[-1]
sys.stdout = streamWriter(sys.stdout)
sys.setdefaultencoding("utf-8")
class MyTestCase():
	
    def setUp(self):
        self.driver = webdriver.Chrome()
        #self.driver.error_handler = MyHandler()

    def main(self):
        REGION=[]
        INSEE=[] #la liste des départements
        CITIES=[]
        with open('3000Commun_France.csv') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader) # supression des entêtes
            for row in csv_reader:
                REGION.append(row[0])
                INSEE.append(row[1])
                CITIES.append(row[2])
        self.driver = webdriver.Chrome()
        driver=self.driver
        ID=1
        f = csv.writer(open('Lacoteimmo_Nouvelle_Aquitaine.csv', 'w'))
        f.writerow(['ID','Région','INSEE','Ville','Ville','Prix m²','Loyer le plus recherché','Nb de pièces le plus recherché','Superficie la plus recherchée','Type de bien le plus recherché','EPM 3mois','EPM 12mois',
        'EPM 3ans','EPM 5 ans','EPA 3mois','EPA 12mois','EPA 3ans','EPA 5ans','Prix minimal au m² (maison - appartement)','Prix moyen au m² (maison - appartement)','Prix maximal au m² (maison - appartement)','Répartition des prix moyen au m²',
        'Répartition des Surfaces','Part de résidences principales','Part de propriétaires','Répartition homme / femme','Population','Densité de population au km²','Habitants','Revenue'])
        for region,insee,city in zip(REGION,INSEE,CITIES):
            print str(city) +" , "+str(insee)+" , "+str(ID)
            try:
                driver.get("http://www.lacoteimmo.com/prix-de-l-immo/location/pays/france.htm#/")
                driver.implicitly_wait(20)
                driver.find_element_by_css_selector("#mapAutosuggest").send_keys(city)  # Enter city
                # Wait until autosuggestion come and click on first suggestion
                time.sleep(3)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.slam-aui-results>span.slam-aui-results-line.focus"))).click()
                time.sleep(5)
                page = driver.page_source
                soup = BeautifulSoup(page, "lxml")
                Prix=soup.find("div",{"class":"price"})
                Prix=Prix.text
                print Prix
                Loyer=soup.find_all("div", {"class" : "value"})[0::3]
                Nb_piece=soup.find_all("div", {"class" : "value"})[1::3]
                surface=soup.find_all("div", {"class" : "value"})[2::3]
                Type_bien=soup.find_all("div", {"class" : "value"})[3::3]
                for Data in list(zip(Loyer,Nb_piece,surface,Type_bien)):
                    try:
                        Loyer,Nb_piece,surface,Type_bien = Data
                        Loyer=Loyer.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        Nb_piece=Nb_piece.string.encode('utf-8') # Le nombre de voyageurs accueillis entre septembre 2016 et septembre 2017
                        surface=surface.string.encode('utf-8') # Le nombre de pays dont sont originaires les voyageurs qui y ont séjourné
                        Type_bien=Type_bien.string.encode('utf-8')
                        print ', '.join([Loyer,Nb_piece,surface,Type_bien])
                    except NavigableString: 
                            pass
                Ville=soup.find("div",{"class":"place"})
                Ville=Ville.string.encode('utf-8')
                print Ville
                Habitans=soup.find_all("div", {"class" : "bold"})[0::2]
                Population=soup.find_all("div", {"class" : "bold"})[1::2]
                Revenue=soup.find_all("div", {"class" : "bold"})[2::2]
                for Data in list(zip(Habitans,Population,Revenue)):
                    try:
                        Habitans,Population,Revenue = Data
                        Habitans=Habitans.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        Population=Population.string.encode('utf-8') # Le nombre de voyageurs accueillis entre septembre 2016 et septembre 2017
                        Revenue=Revenue.string.encode('utf-8') # Le nombre de pays dont sont originaires les voyageurs qui y ont séjourné
                        print ', '.join([Habitans,Population,Revenue])
                    except NavigableString: 
                            pass
                Residence=soup.find_all("text", {"class" : "p10_title"})
                Propriete=soup.find_all("text", {"class" : "p11_title"})
                for Data in list(zip(Residence,Propriete)):
                    try:
                        Residence,Propriete = Data
                        Residence=Residence.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        Propriete=Propriete.string.encode('utf-8') # Le nombre de voyageurs accueillis entre septembre 2016 et septembre 2017
                        print ', '.join([Residence,Propriete])
                    except NavigableString: 
                            pass
                
                Evo_maison_3m=soup.find_all("div", {"class" : "valeur orange ng-binding"})[0::7]
                Evo_maison_12m=soup.find_all("div", {"class" : "valeur orange ng-binding"})[1::7]
                Evo_maison_3a=soup.find_all("div", {"class" : "valeur orange ng-binding"})[2::7]
                Evo_maison_5a=soup.find_all("div", {"class" : "valeur orange ng-binding"})[3::7]
                Evo_appt_3m=soup.find_all("div", {"class" : "valeur orange ng-binding"})[4::7]
                Evo_appt_12m=soup.find_all("div", {"class" : "valeur orange ng-binding"})[5::7]
                Evo_appt_3a=soup.find_all("div", {"class" : "valeur orange ng-binding"})[6::7]               
                Evo_appt_5a=soup.find_all("div", {"class" : "valeur orange ng-binding"})[7::7]
                for Data in list(zip(Evo_maison_3m,Evo_maison_12m,Evo_maison_3a,Evo_maison_5a,Evo_appt_3m,Evo_appt_12m,Evo_appt_3a,Evo_appt_5a)):
                    try:
                        Evo_maison_3m,Evo_maison_12m,Evo_maison_3a,Evo_maison_5a,Evo_appt_3m,Evo_appt_12m,Evo_appt_3a,Evo_appt_5a= Data
                        Evo_maison_3m= Evo_maison_3m.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        Evo_maison_12m= Evo_maison_12m.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        Evo_maison_3a= Evo_maison_3a.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        Evo_maison_5a= Evo_maison_5a.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        Evo_appt_3m= Evo_appt_3m.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        Evo_appt_12m= Evo_appt_12m.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        Evo_appt_3a= Evo_appt_3a.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        Evo_appt_5a= Evo_appt_5a.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        print ', '.join([Evo_maison_3m,Evo_maison_12m,Evo_maison_3a,Evo_maison_5a,Evo_appt_3m,Evo_appt_12m,Evo_appt_3a,Evo_appt_5a])
                    except NavigableString: 
                            pass
                nb_femme=soup.find_all("text", {"class" : "p8_segmentMainLabel-outer"})
                nb_homme=soup.find_all("text", {"class" : "p8_segmentValue-outer"})
                Homme_Femme=[]
                for Data in list(zip(nb_femme,nb_homme)):
                    try:
                        nb_femme,nb_homme = Data
                        nb_femme=nb_femme.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        nb_homme=nb_homme.string.encode('utf-8') # Le nombre de voyageurs accueillis entre septembre 2016 et septembre 2017
                        #print ' = '.join([nb_femme,nb_homme])
                        Data1=' = '.join([nb_femme,nb_homme])
                        print Data1
                        Homme_Femme.append(Data1)
                    except NavigableString: 
                            pass
                #Population
                Populationbis=[]
                nb_celeb=soup.find_all("text", {"class" : "p9_segmentMainLabel-outer"})
                nb_en_couple=soup.find_all("text", {"class" : "p9_segmentValue-outer"})
                for Data in list(zip(nb_celeb,nb_en_couple)):
                    try:
                        nb_celeb,nb_en_couple = Data
                        nb_celeb=nb_celeb.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        nb_en_couple=nb_en_couple.string.encode('utf-8') # Le nombre de voyageurs accueillis entre septembre 2016 et septembre 2017
                        Data4=' = '.join([nb_celeb,nb_en_couple])
                        Populationbis.append(Data4)
                        print ' = '.join([nb_celeb,nb_en_couple])
                    except NavigableString: 
                            pass
                #Répartition des prix moyen au m²
                Repartition=[]          
                Inferieur=soup.find_all("text", {"class" : "p6_segmentMainLabel-outer"})
                Superieur=soup.find_all("text", {"class" : "p6_segmentValue-outer"})
                for Data in list(zip(Inferieur,Superieur)):
                    try:
                        Inferieur,Superieur = Data
                        Inferieur=Inferieur.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        Superieur=Superieur.string.encode('utf-8') # Le nombre de voyageurs accueillis entre septembre 2016 et septembre 2017
                        Data2=' = '.join([Inferieur,Superieur])
                        print Data2
                        Repartition.append(Data2)
                    except NavigableString: 
                            pass
                #Répartition des Surfaces
                SurfaceBis=[]
                Surface=soup.find_all("text", {"class" : "p7_segmentMainLabel-outer"})
                Surface_Val=soup.find_all("text", {"class" : "p7_segmentValue-outer"})
                for Data in list(zip(Surface,Surface_Val)):
                    try:
                        Surface,Surface_Val = Data
                        Surface=Surface.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                        Surface_Val=Surface_Val.string.encode('utf-8') # Le nombre de voyageurs accueillis entre septembre 2016 et septembre 2017
                        Data3=' = '.join([Surface,Surface_Val])
                        SurfaceBis.append(Data3)
                    except NavigableString: 
                            pass
                Minim=[]
                Moyen=[]
                Maxim=[]
                minim=soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['min'])
                moyen=soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['moy'])
                maxim=soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['max'])
                for Data in list(zip(minim,moyen,maxim)):
                        minim,moyen,maxim=Data
                        minim=minim.string.encode('utf-8')
                        moyen=moyen.string.encode('utf-8')
                        maxim=maxim.string.encode('utf-8')
                        Minim.append(minim)
                        Moyen.append(moyen)
                        Maxim.append(maxim)
                        print ' , '.join([minim,moyen,maxim])

                f.writerow([ID,region,insee,city,Ville,Prix.encode('utf-8'),Loyer,Nb_piece,surface,Type_bien,Evo_maison_3m,Evo_maison_12m,Evo_appt_3a,Evo_maison_5a,Evo_appt_3m,Evo_appt_12m,
                            Evo_appt_3a,Evo_appt_5a,Minim,Moyen,Maxim,Repartition,SurfaceBis,Residence,Propriete,Homme_Femme,
                            Populationbis,Habitans,Population,Revenue]) 
                ID+=1
                driver.refresh()
            except NoSuchElementException:  #spelling error making this code not work as expected
                pass
        self.driver.quit()

    def tearDown(self):
        self.driver.quit()
        
    
if __name__ == "__main__":
    sys.tracebacklimit = 0
    MyTestCase().main()

