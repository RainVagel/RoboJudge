# -​*- coding: utf-8 -*​-

import requests
import logging
import urllib2
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s %(levelname)s:  %(message)s', level=logging.DEBUG)

# Selle on riigiteataja kodulehekülg. Siia lõppu lisan aktide lingid.
riigiteataja_link = "https://www.riigiteataja.ee/"

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
sisu = list()

logging.info("Laen seaduseid ... %s dokumenti kokku", len(aktide_lingid))

for link in aktide_lingid[:2]:
    sisu.append(urllib2.urlopen("https://www.riigiteataja.ee/" + str(link) + ".xml").read())
    logging.debug("Protsessin järgmist seadust: %s", link)
    protsessitud_lehti += 1
    logging.debug("Protsessitud lehti kokku: %s", protsessitud_lehti)

print(sisu)
