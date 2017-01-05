# -​*- coding: utf-8 -*​-

from pathlib import Path
import scraper
import os
import logging
from estnltk import Text
import operator
import pandas
import math

# Selles failis toimub põhiline töö.


def tf(lemma, tekst):
    # Võtab sisse lemma ning teksti ja arvutab selle lemma sagedust
    return tekst.count(lemma) / len(tekst)


def n_containing(lemma, tekst_list):
    # Tagatsab, paljudes tekstides see lemma esineb
    return sum(1 for tekst in tekst_list if lemma in tekst)


def idf(lemma, tekst_list):
    # Arvutab, kui sagedasti lemma esineb sisu_tekstides ning annab selle pöördväärtuse
    return math.log(len(tekst_list)) / (1 + n_containing(lemma, tekst_list))


def tfidf(lemma, tekst, tekst_list):
    # Arvutab TF-IDF skoori
    # Tekst on siinkohal kasutaja sisend
    return tf(lemma, tekst) * idf(lemma, tekst_list)


def check_file_up_to_date():
    # Meetod kontrollib, kas seda faili peab uuendama
    # TODO
    return True


def check_data_exist():
    # See meetod kontrollib, kas "data.xlsx" fail asub kaustas
    my_file = Path("data.xlsx")
    return my_file.is_file()


def analyse_user_input(user_input):
    return Text(user_input).lemmas


def create_lemmas_counted_dict(data_lemmatised):
    # Loome dict kujul: {lemma: {lõigu_indeks:palju_neid_lõigus, lõigu_indeks jne...} lemma: {....}}
    counted_lemmas_dict = dict()
    for key in data_lemmatised.keys():
        for lemma in data_lemmatised[key]:
            if lemma in counted_lemmas_dict.keys():
                # Kui selline lemma on counted_lemmas_dictis
                if key in counted_lemmas_dict[lemma]:
                    counted_lemmas_dict[lemma][key] += 1
                else:
                    counted_lemmas_dict[lemma][key] = 1
            else:
                # Kui sellist lemmat pole counted_lemmas_dictis
                counted_loik = dict()
                counted_loik[key] = 1
                counted_lemmas_dict[lemma] = counted_loik
    return counted_lemmas_dict


def get_answer(user_input, counted_lemmas, data_lemmatised_dict, data_sisu_tekst_list):
    # Otsib võimalikku lõiku, mida vastuseks anda
    answer_indexes = list()
    for lemma in user_input:
        if lemma in counted_lemmas.keys():
            sorted_counted_lemmas = sorted(counted_lemmas[lemma].items(), key=operator.itemgetter(1), reverse=True)
            answer_indexes.append(sorted_counted_lemmas[0][0])
    lemma_scores = dict()
    for index in answer_indexes:
        lemma_scores = {lemma: tfidf(lemma, data_lemmatised_dict[index], data_sisu_tekst_list) for lemma in user_input}
    print(lemma_scores)
    return None


def main():
    # See meetod on programmi põhiline meetod ja tegeleb asjade jooksutamisega
    if not check_data_exist():
        # Kui seda faili ei eksisteeri
        scraper.scrape()
    # Kui fail eksisteerib, siis läheme siit edasi
    if not check_file_up_to_date():
        # Kui "data.xlsx" faili peab uuendama
        os.remove("data.xlsx")
        scraper.scrape()
    # Tsükkel, mis tegeleb sisendi saamisega
    while True:
        try:
            input_string = str(input("Sisestage otsing: "))
        except ValueError:
            print("Vigane sisend! Proovige uuesti.")
        else:
            break
    # Siit algab sisendi töötlemine ning vastuse väljamõtlemine
    user_input_lemmas = analyse_user_input(input_string)
    data_values = pandas.read_excel(open("data.xlsx", "rb"), sheetname="data")
    data_lemmatised_dict = dict()
    data_sisu_tekst_list = list()
    counter = 0
    for line in data_values.itertuples():
        # line[0] on indeks ja line[8] on sisu_tekst
        counter += 1
        logging.debug("Protsessitud lõike kokku: %s", counter)
        lemmatised = Text(str(line[8])).lemmas
        data_lemmatised_dict[line[0]] = lemmatised
        data_sisu_tekst_list.append(lemmatised)
    counted_lemmas_dict = create_lemmas_counted_dict(data_lemmatised_dict)
    answer = get_answer(user_input_lemmas, counted_lemmas_dict, data_lemmatised_dict, data_sisu_tekst_list)
    return None

if __name__ == "__main__":
    main()
