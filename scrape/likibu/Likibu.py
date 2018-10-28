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
import unicodecsv as csv

from time import sleep
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



class MyHandler(ErrorHandler):
    def check_response(self, response):
        try:
            super(MyHandler, self).check_response(response)
        except NoSuchElementException as e:
            e.stacktrace = None
            raise

class MyTestCase():
    def setUp(self):
        self.driver = webdriver.Chrome()
        #self.driver.error_handler = MyHandler()

    def main(self):
        if not os.path.exists('likibu_Nouvelle_Aquitaine.csv'):
                f = csv.writer(open('likibu_Nouvelle_Aquitaine.csv', 'w'))
                f.writerow(['INSEE','Ville','Titre','Prix','Surface','Nombre de personne','La note du logement','Nombre de commentaire','Collaborateur','Longitude','Latitude'])
        else :
                f = csv.writer(open('likibu_Nouvelle_Aquitaine.csv', 'a'))
                global file_size_stored
                file_size_stored = os.stat('likibu_Nouvelle_Aquitaine.csv').st_size
        CITIES = []
        INSEE=[]
        with open('New_aquitaine_cities.csv') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader) # supression des entêtes
            for row in csv_reader:
                INSEE.append(row[0]+row[1])
                CITIES.append(row[2])
        self.driver = webdriver.Chrome()
        driver=self.driver
        driver.set_window_size(1920, 1080)
        driver.implicitly_wait(20)
        global city
        ID=1
        for insee,city in zip(INSEE,CITIES):
            print str(city) +" , "+str(ID)
            ID+=1
            try:      
                driver.get("https://www.likibu.com/")   #Lancer le site web 
                driver.implicitly_wait(20) 
                driver.find_element_by_css_selector("#where").send_keys(city+",fr")  # Entrer le nom de la ville
                # Wait until autosuggestion come and click on first suggestion
                condition = EC.visibility_of_element_located((By.CSS_SELECTOR, '#where + ul > li:nth-child(1)'))
                time.sleep(3)
                WebDriverWait(driver, 5).until(condition).click()
                driver.find_element_by_id("show_exit_units").click() # Décocher le compare avec Airbnb 
                #Cliquer sur le bouton chercher
                driver.find_element_by_css_selector('div.form-group.col-md-5.col-sm-3.col-xs-12').click()
                #Cliquer sur le button filtre
                driver.find_element_by_css_selector("div.col-xs-12.col-sm-11.col-sm-push-1").click()
                #Choisir l'option Entre particuliers
                if not driver.find_element_by_id("is_p2p"):
                    pass
                else :
                    driver.find_element_by_id("is_p2p").click()
                #Cliquer sur le bouton chercher pour valider les nouveaux paramètre 
                    driver.find_element_by_css_selector('div.form-group.col-md-5.col-sm-3.col-xs-12').click()
                    while 1:
                        page = driver.page_source
                        soup = BeautifulSoup(page, "lxml")  # Use BeautifulSoup For scraping of data since selenium is slow
                        #le tag global de l'annoce
                        Annonces = soup.find_all("div", {"class":"lkb-offer-card col-lg-4 col-md-6 col-sm-6 col-xs-12"}) 
                        #le prix de l'annonce
                        Prix=soup.find_all("span",{"itemprop":"priceRange"})
                        #le site collaborateur ex(booking,hotels...)   
                        Collaborateur=soup.find_all("div",{"class":"compare"})
                        #Latitude & longitude de l'annonce
                        Latitude=soup.find_all("meta",{"itemprop":"latitude"}) 
                        Longitude=soup.find_all("meta", {"itemprop":"longitude"}) 
                        #nombre de "guets"  
                        nb_personne=soup.find_all("span",{"class":"lkb-icon lkb-icon-guest"})
                        for Annonce,prix,site,lat,lon,pers in list(zip(Annonces,Prix,Collaborateur,Latitude,Longitude,nb_personne)):
                                #titre de l'annonce
                                Titre = Annonce.find("div",{"class":"title col-xs-12"}).string.encode('utf-8')
                                #la note de l'annonce 
                                avg_comment=Annonce.find("span",{"class":"average"}).string.encode('utf-8')
                                #le nombre de commentaire
                                nb_comment=Annonce.find("span",{"class":"count"}).string.encode('utf-8')
                                lat=lat['content']
                                lon=lon['content']
                                #surfece de l'annonce
                                Surface=Annonce.find("span",class_="units grey")
                                if Surface is None:
                                    Surface=" None "
                                else:
                                    Surface=Surface.text.encode('utf-8')
                                if pers is None:
                                    pers=" None "
                                else:
                                    pers=pers.text.encode('utf-8')
                                prix=prix.text.encode('utf-8')
                                site=site.text.encode('utf-8')
                
                                #Date=now.strftime("%Y-%m-%d %H:%M")
                                #l'écreture de résultat dans le fichier Likibu.csv                    
                                f.writerow([insee,city,Titre,prix,Surface,pers,avg_comment,nb_comment,site,lon,lat])                       
                        next_page_link=driver.find_element_by_link_text('»').get_attribute('href')
                        href=len(next_page_link)
                        if not driver.find_element_by_link_text('»'): #si la page suivante n'existe pas
                            break #sort
                        elif next_page_link[href-1:]=="#": # s'il reste plus de page à suivre
                            break
                                # Open next page
                        try :
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='pagination']//li/a[@rel='nofollow' and contains(.,'»')]"))).click()
                        except :
                            break 
                        time.sleep(10)
                        driver.implicitly_wait(30) 
            except NoSuchElementException:  #spelling error making this code not work as expected
                pass
        self.driver.quit()

    def csv_traitement(self):
        now = datetime.now()
        Date=now.strftime("%Y-%m-%d %H:%M")
        df = pd.read_csv('likibu_Nouvelle_Aquitaine.csv')
        df.drop_duplicates(inplace=True)
        df.to_csv('likibu_likibu_Nouvelle_Aquitaine.csv', index=False)
        file_size_current = os.stat('likibu_Nouvelle_Aquitaine.csv').st_size
        text_file = open("Détails.txt", "a")
        if file_size_stored != file_size_current:
            text_file.write("Le fichier likibu_Nouvelle_Aquitaine.csv a été modifié à : %s \n " % Date)
            text_file.close()

    def tearDown(self):
        self.driver.quit()
        
    
if __name__ == "__main__":
    sys.tracebacklimit = 0
    MyTestCase().main()
    #MyTestCase().csv_traitement()

