import requests
from bs4 import BeautifulSoup

# Selle on riigiteataja kodulehekülg. Siia lõppu lisan aktide lingid.
riigiteataja_link = "https://www.riigiteataja.ee/"

soup = BeautifulSoup(requests.get('https://www.riigiteataja.ee/tervikteksti_tulemused.html'
                                  '?kehtivusKuupaev=02.01.2017&nrOtsing=tapne&riigikoguOtsused=false'
                                  '&valislepingud=false&valitsuseKorraldused=false'
                                  '&valjDoli1=Rahvahääletusel+vastu+võetud+-+seadus'
                                  '&valjDoli2=Riigikogu+-+seadus&valjDoli3=Ülemnõukogu+-+seadus'
                                  '&sakk=kehtivad_kehtetuteta&leht=0'
                                  '&kuvaKoik=true&sorteeri=&kasvav=true').text, "lxml")
# print(soup.prettify())
aktide_lingid = list()
for link in soup.find_all('a'):
    if "akt/" in link.get('href'):
        aktide_lingid.append(link.get('href'))
    # print(link.get('href'))
# print(lingid)

