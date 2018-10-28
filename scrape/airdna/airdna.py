#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import time
import csv
import unittest
import sys
import datetime
import os.path
import pandas as pd
import datetime

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


class MyTestCase():
    def setUp(self):
        self.driver = webdriver.Chrome()
        #self.driver.error_handler = MyHandler()

    def main(self):
        now = datetime.now()
        f = csv.writer(open('Airdna_France.xls', 'a'))
        #f.writerow(['ID','Région','Insee','Ville','Last_scraped','Rental Demand','Average Daily Rate','Occupancy Rate','Revenue','Active Rentals',
        #'Entire Home','Private & shared Room','Rental Size','Rental Activity','Rental Growth','Active Hosts','Multi-listing Hosts','Single-listing Hosts'])
        REGION=[]
        INSEE=[] #la liste des départements
        CITIES=[]
        ID=1 # l'identifiant des données
        with open('3000Commun_France.csv') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader) # supression des entêtes
            for row in csv_reader:
                REGION.append(row[0])
                INSEE.append(row[1])
                CITIES.append(row[2])
        self.driver = webdriver.Chrome()
        driver=self.driver
        for region,insee,city in zip(REGION,INSEE,CITIES):
            print str(city) +" , "+str(insee)+" , "+str(ID)
            try:
                driver.get("https://www.airdna.co/")
                driver.implicitly_wait(20)
                driver.find_element_by_css_selector("#searchbox_home").send_keys(city)  # Enter city
                # Wait until autosuggestion come and click on first suggestion
                condition=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"ul.ui-menu.ui-widget.ui-widget-content.ui-autocomplete.ui-front>li>div"))).get_attribute("innerHTML")
                if condition=="No results found":
                    Rental_Demand="Aucun résultat"
                    Active_Hosts="Aucun résultat"
                    Active_Rentals="Aucun résultat"
                    Rental_Type="Aucun résultat"
                    Rental_Activity="Aucun résultat"
                    Rental_Size="Aucun résultat"
                    Rental_Growth="Aucun résultat"
                    Multi_listing_Hosts="Aucun résultat"
                    Single_listing_Hosts="Aucun résultat"
                    Average_Daily_Rate="Aucun résultat"
                    Occupancy_Rate="Aucun résultat"
                    Revenue="Aucun résultat"
                    Entire_Home="Aucun résultat"
                    Private_Shared_Room="Aucun résultat"
                else:
                    time.sleep(1)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"ul.ui-menu.ui-widget.ui-widget-content.ui-autocomplete.ui-front>li>div"))).click()
                    time.sleep(3)
                    page = driver.page_source
                    soup = BeautifulSoup(page, "lxml")
                    Rental_Demand=soup.find("p",class_="market-health-section__right-axis-text")
                    if Rental_Demand is None :
                        Rental_Demand="Aucun résultat"
                        Active_Hosts="Aucun résultat"
                        Active_Rentals="Aucun résultat"
                        Rental_Type="Aucun résultat"
                        Rental_Activity="Aucun résultat"
                        Rental_Size="Aucun résultat"
                        Rental_Growth="Aucun résultat"
                        Multi_listing_Hosts="Aucun résultat"
                        Single_listing_Hosts="Aucun résultat"
                        Average_Daily_Rate="Aucun résultat"
                        Occupancy_Rate="Aucun résultat"
                        Revenue="Aucun résultat"
                        Entire_Home="Aucun résultat"
                        Private_Shared_Room="Aucun résultat"
                    else :
                        Rental_Demand=Rental_Demand.string.encode('utf-8')
                        Average_Daily_Rate=soup.find_all("div", {"class" : "box-overall__value "})[0::2]
                        Occupancy_Rate=soup.find_all("div", {"class" : "box-overall__value"})[1::2]
                        Revenue=soup.find_all("div", {"class" : "box-overall__value"})[2::2]
                        for Data in list(zip(Average_Daily_Rate,Occupancy_Rate,Revenue)):
                            try:
                                Average_Daily_Rate, Occupancy_Rate,Revenue = Data
                                Average_Daily_Rate=Average_Daily_Rate.string.encode('utf-8') # Le nombre d’annonces dans la ville au 1er septembre 2017
                                Occupancy_Rate=Occupancy_Rate.string.encode('utf-8') # Le nombre de voyageurs accueillis entre septembre 2016 et septembre 2017
                                Revenue=Revenue.string.encode('utf-8') # Le nombre de pays dont sont originaires les voyageurs qui y ont séjourné
                                print ', '.join([Average_Daily_Rate, Occupancy_Rate,Revenue])
                            except NavigableString: 
                                pass
                        
                        values = soup.find_all("div", {"class" : "section__header"})
                        target_list = []
                        for value in values:
                            target_list.append(value.text)
                        Active_Rentals=target_list[0]
                        Active_Hosts=target_list[1]
                        print ','.join([Active_Rentals,Active_Hosts])
                        #print(output)

                        Rental_Type=soup.find_all("span",{"class" : "section__headline"})[0::3]
                        Rental_Size=soup.find_all("span",{"class" : "section__headline"})[1::3]
                        Rental_Activity=soup.find_all("span",{"class" : "section__headline"})[2::3]
                        Rental_Growth=soup.find_all("span",{"class" : "section__headline"})[3::3]
                        for Info in list(zip(Rental_Type,Rental_Size,Rental_Activity,Rental_Growth)):
                            try:
                                Rental_Type,Rental_Size,Rental_Activity,Rental_Growth=Info 
                                Rental_Type=Rental_Type.string.encode('utf-8')
                                Rental_Size=Rental_Size.string.encode('utf-8')
                                Rental_Activity=Rental_Activity.string.encode('utf-8')
                                Rental_Growth=Rental_Growth.string.encode('utf-8')
                                print ','.join([Rental_Type,Rental_Size,Rental_Activity,Rental_Growth])
                            except NavigableString: 
                                pass

                        Multi_listing_Hosts=soup.find_all("text",{"class" : "chart__legend-text"})[0::1]
                        Single_listing_Hosts=soup.find_all("text",{"class" : "chart__legend-text"})[1::1]
                        for Info in list(zip(Multi_listing_Hosts,Single_listing_Hosts)):
                            try:
                                Multi_listing_Hosts,Single_listing_Hosts=Info 
                                Multi_listing_Hosts=Multi_listing_Hosts.string.encode('utf-8')
                                Single_listing_Hosts=Single_listing_Hosts.string.encode('utf-8')
                                print ','.join([Multi_listing_Hosts,Single_listing_Hosts])
                            except NavigableString: 
                                pass
                        Entire_Home=Rental_Type
                        Private_Shared_Room="the rest"
                Date=now.strftime("%Y-%m-%d %H:%M")  
                f.writerow([ID,region,insee,city,Date,Rental_Demand,Average_Daily_Rate,Occupancy_Rate,Revenue,Active_Rentals,
                Entire_Home,Private_Shared_Room,Rental_Size,Rental_Activity,Rental_Growth,Active_Hosts,Multi_listing_Hosts,Single_listing_Hosts])
                ID+=1 
            except NavigableString: 
                    pass
if __name__ == "__main__":
    sys.tracebacklimit = 0
    MyTestCase().main()