# -​*- coding: utf-8 -*​-

import requests
import logging
import re
from xml.etree.ElementTree import XML
from bs4 import BeautifulSoup
from pandas import DataFrame

# Selle on riigiteataja kodulehekülg. Siia lõppu lisan aktide lingid.
riigiteataja_link = "https://www.riigiteataja.ee/"


class Scraper:

    logging.basicConfig(format='%(asctime)s %(levelname)s:  %(message)s', level=logging.DEBUG)

    def __init__(self):
        self.kehtivuse_algus = None
        self.kehtivuse_lopp = None
        self.akti_nimi = None
        self.peatukk_nr = None
        self.paragrahv_nr = None
        self.paragrahv_pealkiri = None
        self.alampunkt_nr = None
        self.loige_nr = None
        self.ylaindeks = None
        self.sisu_tekst = None
        self.kehtivuse_algus_column = list()
        self.kehtivuse_lopp_column = list()
        self.akti_nimi_column = list()
        self.peatukk_nr_column = list()
        self.paragrahv_nr_column = list()
        self.paragrahv_pealkiri_column = list()
        self.loige_nr_column = list()
        self.ylaindeks_column = list()
        self.sisu_tekst_column = list()

    def xml_parser(self, element):
        #     Rekurssiivne funktsioon. insert_law_to_excel abifunktsioon.

        if element.tag == "metaandmed":
            for child in element:
                # print("Made it to meta")
                # print(child.tag)
                self.xml_parser(child)
        elif element.tag == "kehtivus":
            kehtivuse_lopp_boolean = False
            for child in element:
                if child.tag == "kehtivuseAlgus":
                    self.kehtivuse_algus = child.text
                elif child.tag == "kehtivuseLopp":
                    kehtivuse_lopp_boolean = True
                    self.kehtivuse_lopp = child.text
            if kehtivuse_lopp_boolean is False:
                self.kehtivuse_lopp = None
        elif element.tag == "aktinimi":
            for child in element:
                for grand_child in child:
                    if grand_child.tag == "pealkiri":
                        self.akti_nimi = grand_child.text
        elif element.tag == "sisu":
            # print("Made it to sisu!")
            for child in element:
                self.xml_parser(child)
        elif element.tag == "peatykk":
            for child in element:
                self.xml_parser(child)
        elif element.tag == "peatykkNr":
            self.peatukk_nr = element.text
        elif element.tag == "paragrahv":
            # print("Made it to paragrahv")
            for child in element:
                self.xml_parser(child)
        elif element.tag == "paragrahvNr":
            # print("Made it to paragrahvNr")
            self.paragrahv_nr = element.text
            # print(self.paragrahv_nr)
        elif element.tag == "paragrahvPealkiri":
            self.paragrahv_pealkiri = element.text
        elif element.tag == "loige":
            # print("Made it to loige")
            for child in element:
                # print(child.tag)
                if child.tag == "loigeNr":
                    if "ylaindeks" in child.attrib:
                        self.ylaindeks = child.attrib.get("ylaindeks")
                    self.loige_nr = child.text
                    # print(self.loige_nr)
                if child.tag == "sisuTekst":
                    # print("Made it to sisutekst1")
                    for grand_child in child:
                        if grand_child.tag == "tavatekst":
                            # print("Made it to tavatekst")
                            self.sisu_tekst = grand_child.text
                if child.tag == "alampunkt":
                    i = 0
                    while child[i].tag != "alampunktNr":
                        i += 1
                    self.alampunkt_nr = child[i].text
                    # print(self.alampunkt_nr)
                    for grand_child in child:
                        # print(self.alampunkt_nr)
                        if grand_child.tag == "sisuTekst":
                            for great_grand_child in grand_child:
                                if great_grand_child.tag == "tavatekst":
                                    # print(great_grand_child.text)
                                    self.sisu_tekst += "" if self.alampunkt_nr is None else \
                                        self.alampunkt_nr + " " + great_grand_child.text
            self.kehtivuse_algus_column.append(self.kehtivuse_algus)
            self.kehtivuse_lopp_column.append(self.kehtivuse_lopp)
            self.akti_nimi_column.append(self.akti_nimi)
            self.peatukk_nr_column.append(self.peatukk_nr)
            self.paragrahv_nr_column.append(self.paragrahv_nr)
            self.paragrahv_pealkiri_column.append(self.paragrahv_pealkiri)
            self.loige_nr_column.append(self.loige_nr)
            self.ylaindeks_column.append(self.ylaindeks)
            self.sisu_tekst_column.append(self.sisu_tekst)
            self.alampunkt_nr = None
            self.ylaindeks = None
            self.sisu_tekst = None

    def insert_laws_to_excel(self, xml_files):
        # Võtab xml_files listi ja sisestab andmed exceli formaati. xlsx formaati
        for file in xml_files:
            xml_string = re.sub('xmlns="[^"]+"', '', file, count=1)
            tree = XML(xml_string)
            for elem in tree:
                self.xml_parser(elem)
        # print("kehtivuse algus: " + str(self.kehtivuse_algus_column))
        # print("kehtivuse lõpp: " + str(self.kehtivuse_lopp_column))
        # print("aktiNimi: " + str(self.akti_nimi_column))
        # print("peatukkNr: " + str(self.peatukk_nr_column))
        # print("paragrahbNr: " + str(self.paragrahv_nr_column))
        # print("paragrahvNimi: " + str(self.paragrahv_pealkiri_column))
        # print("lõigeNr: " + str(self.loige_nr_column))
        # print("ylaindeksNr: " + str(self.ylaindeks_column))
        # print("sisuTekst: " + str(self.sisu_tekst_column))
        df = DataFrame({"kehtivuse_algus" : self.kehtivuse_algus_column, "kehtivuse_lopp" : self.kehtivuse_lopp_column,
                        "akti_nimi" : self.akti_nimi_column, "peatukk_nr" : self.peatukk_nr_column,
                        "paragrahv_nr" : self.paragrahv_nr_column, "paragrahv_nimi" : self.paragrahv_pealkiri_column,
                        "loige_nr" : self.loige_nr_column, "ylaindeks_nr" : self.ylaindeks_column,
                        "sisu_tekst" : self.sisu_tekst_column})
        df.to_excel("data.xlsx", sheet_name="data", index=True)


def get_laws():
    # Kogub kokku seaduste xml failid

    soup = BeautifulSoup(requests.get('https://www.riigiteataja.ee/tervikteksti_tulemused.html'
                                      '?kehtivusKuupaev=02.01.2017&nrOtsing=tapne&riigikoguOtsused=false'
                                      '&valislepingud=false&valitsuseKorraldused=false'
                                      '&valjDoli1=Rahvahääletusel+vastu+võetud+-+seadus'
                                      '&valjDoli2=Riigikogu+-+seadus&valjDoli3=Ülemnõukogu+-+seadus'
                                      '&sakk=kehtivad_kehtetuteta&leht=0'
                                      '&kuvaKoik=true&sorteeri=&kasvav=true').text, "lxml")
    aktide_lingid = list()
    for link in soup.find_all('a'):
        if "akt/" in link.get('href'):
            aktide_lingid.append(link.get('href'))

    protsessitud_lehti = 0
    xml_files = list()

    logging.info("Laen seaduseid ... %s dokumenti kokku", len(aktide_lingid))

    for link in aktide_lingid:
        xml_files.append(requests.get(riigiteataja_link + str(link) + ".xml").text)
        logging.debug("Protsessin järgmist seadust: %s", link)
        protsessitud_lehti += 1
        logging.debug("Protsessitud lehti kokku: %s", protsessitud_lehti)

    return xml_files


def scrape():
    # Mooduli põhimeetod, mida väljaspool moodulit kutsutakse välja
    scraper = Scraper()
    scraper.insert_laws_to_excel(get_laws())
