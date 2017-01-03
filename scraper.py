# -​*- coding: utf-8 -*​-

import requests
import logging
import re
from xml.etree.ElementTree import XML
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s %(levelname)s:  %(message)s', level=logging.DEBUG)

# Selle on riigiteataja kodulehekülg. Siia lõppu lisan aktide lingid.
riigiteataja_link = "https://www.riigiteataja.ee/"


def get_laws():
    # Kogub kokku seaduste xml failid

    soup = BeautifulSoup(requests.get('https://www.riigiteataja.ee/tervikteksti_tulemused.html'
                                      '?kehtivusKuupaev=02.01.2017&nrOtsing=tapne&riigikoguOtsused=false'
                                      '&valislepingud=false&valitsuseKorraldused=false'
                                      '&valjDoli1=Rahvahääletusel+vastu+võetud+-+seadus'
                                      '&valjDoli2=Riigikogu+-+seadus&valjDoli3=Ülemnõukogu+-+seadus'
                                      '&sakk=kehtivad_kehtetuteta&leht=0'
                                      '&kuvaKoik=true&sorteeri=&kasvav=true').text, "lxml")
    #print(soup.prettify())
    aktide_lingid = list()
    for link in soup.find_all('a'):
        if "akt/" in link.get('href'):
            aktide_lingid.append(link.get('href'))

    #print(aktide_lingid)

    protsessitud_lehti = 0
    xml_files = list()

    logging.info("Laen seaduseid ... %s dokumenti kokku", len(aktide_lingid))

    for link in aktide_lingid[:2]:
        xml_files.append(requests.get(riigiteataja_link + str(link) + ".xml").text)
        logging.debug("Protsessin järgmist seadust: %s", link)
        protsessitud_lehti += 1
        logging.debug("Protsessitud lehti kokku: %s", protsessitud_lehti)

    # print("Sisu: " + str(xml_files))

    return xml_files


def insert_laws_to_excel(xml_files):
    # Võtab xml_files listi ja sisestab andmed exceli formaati. xlsx formaati
    for file in xml_files[:1]:
        xml_string = re.sub('xmlns="[^"]+"', '', file, count=1)
        tree = XML(xml_string)
        # with open(file, "rt") as f:
        # tree = XML(file)
        # print(tree)
        for elem in tree:
            # Kirjutan ümber rekurssiivseks - Vagel
            if elem.tag == "metaandmed":
                print(elem.tag)
                for child in elem:
                    if child.tag == "vastuvoetud":
                        print(child.tag)
                        for i in child:
                            aktikuupaev = i.text
    #                         Sain kätte kuupäeva, millal akt võeti vastu

    # TODO
    return None


insert_laws_to_excel(get_laws())

def scrape():
    # Mooduli põhimeetod, mida väljaspool moodulit kutsutakse välja
    insert_laws_to_excel(get_laws())
    # TODO
    return None
