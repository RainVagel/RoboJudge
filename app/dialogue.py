import re
from estnltk import Text
import lemmatise
import scraper

# Tegeleb kasutajale vastuse leidmisega

freim = {"akti_nimi": None, "peatukk_nr": None, "paragrahv_nr": None, "loik_nr": None,
         "asked_which_law": False, "asked_peatukk_nr": False}


def arabic_to_roman(arabic_number):
    conv = [[1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'],
            [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'],
            [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'],
            [1, 'I']]
    roman = ""
    i = 0
    while arabic_number > 0:
        while conv[i][0] > arabic_number:
            i += 1
        roman += conv[i][1]
        arabic_number -= conv[i][0]
    return roman


def is_loik_numeration(user_message):
    # Tagastab, kas tegu on lõigu numbritega
    m = re.search("(\d+\.)+", user_message)
    if m is None:
        return ""
    numeric_array = m.group(0).split(".")
    answer = list()
    for el in numeric_array:
        if el != '':
            answer.append(el)
    if len(answer) > 3:
        return None
    else:
        return numeric_array


def search_pandas():
    df = lemmatise.return_dataframe()
    # print(df)
    df = df.loc[df['akti_nimi'] == freim["akti_nimi"]]
    if freim["peatukk_nr"] != '':
        df = df.loc[df["peatukk_nr"] == freim["peatukk_nr"]]
        if df.empty:
            empty_freim_number_values()
            return "Vabandust, sellist peatükki ei leidu selles aktis. Palun proovi uuesti!"
    if freim["paragrahv_nr"] != '':
        df = df.loc[df["paragrahv_nr"] == freim["paragrahv_nr"]]
        if df.empty:
            empty_freim_number_values()
            return "Vabandust, sellist paragraahvi ei leidu selles peatükis. Palun proovi uuesti!"
    if freim["loik_nr"] != '':
        df = df.loc[df["loige_nr"] == freim["loik_nr"]]
        if df.empty:
            empty_freim_number_values()
            return "Vabandust, sellist lõiku ei leidu selles paragraahvis. Palun proovi uuesti!"
    sisu_tekst = ""
    for word in df["sisu_tekst"]:
        sisu_tekst += word + " "
    answer = "Seadus: " + str(freim["akti_nimi"]) + "\n" + "Peatükk: " + str(freim["peatukk_nr"]) + \
        ". Paragrahv nr. " + str(freim["paragrahv_nr"]) + ". \n" + sisu_tekst
    return answer


def finding_laws_with_lemmas(user_lemmas, akti_nimed_list):
    akti_nimed_dict_lemmas = dict()
    akti_nimed_dict = dict()
    user_lemmas.remove("seadus")
    index = 0
    for element in akti_nimed_list:
        akti_nimed_dict[index] = element
        akti_nimed_dict_lemmas[index] = Text(element).lemmas
        index += 1
    possible_laws = list()
    for lemma in user_lemmas:
        index = 0
        while index < len(akti_nimed_dict_lemmas):
            if lemma in akti_nimed_dict_lemmas[index]:
                if akti_nimed_dict[index] not in possible_laws:
                    possible_laws.append(akti_nimed_dict[index])
            index += 1
    return possible_laws


def format_possible_laws(possible_laws):
    # Vormistab võimalikud seadused, et need kasutajale esitada
    answer = ""
    for law in possible_laws:
        answer += law + "\n"
    return answer


def lower_akti_nimed():
    akti_nimed_list = lemmatise.collect_akti_nimi()
    akti_nimed_list_lower = list()
    for element in akti_nimed_list:
        if element.lower not in akti_nimed_list_lower:
            akti_nimed_list_lower.append(element.lower())
    return akti_nimed_list_lower


def empty_freim_number_values():
    freim["paragrahv_nr"] = ""
    freim["peatukk_nr"] = ""
    freim["loik_nr"] = ""


def get_number_removed_value(user_message):
    numbers_removed = re.sub("(\d+\.)+", "", user_message).replace("punkt", "").lower().strip()
    numbers_removed = re.sub("(jah|JAH|Jah)(!|.|,)", "", numbers_removed).strip()
    return numbers_removed


def if_law_in_name(numeric_array):
    for index in range(len(numeric_array)):
        if index == 0:
            freim["peatukk_nr"] = arabic_to_roman(int(numeric_array[index]))
        elif index == 1:
            freim["paragrahv_nr"] = numeric_array[index]
        elif index == 2:
            freim["loik_nr"] = numeric_array[index]
    return search_pandas()


def format_seadus():
    # tagastab terve seaduse
    df = lemmatise.return_dataframe()
    df = df.loc[df['akti_nimi'] == freim["akti_nimi"]]
    answer = ""
    last_paragraph_nr = ""
    last_peatukk_nr = ""
    last_loik_nr = ""
    start_index = df.index.values[0]
    end_index = df.index.values[-1]
    while start_index < end_index:
        paragraph_nr = str(df.at[start_index, "paragrahv_nr"])
        peatukk_nr = str(df.at[start_index, "peatukk_nr"])
        loige_nr = str(df.at[start_index, "loige_nr"])
        if paragraph_nr == last_paragraph_nr and peatukk_nr == last_peatukk_nr and loige_nr == last_loik_nr:
            answer += df.at[start_index, "sisu_tekst"] + "\n"
        elif paragraph_nr == last_paragraph_nr and peatukk_nr == last_peatukk_nr and loige_nr != last_loik_nr:
            answer += loige_nr + " " + str(df.at[start_index, "sisu_tekst"]) + "\n"
            last_loik_nr = loige_nr
        elif peatukk_nr == last_peatukk_nr and paragraph_nr != last_paragraph_nr:
            answer += paragraph_nr + "\n" + loige_nr + " " + str(df.at[start_index, "sisu_tekst"]) + "\n"
            last_paragraph_nr = paragraph_nr
            last_loik_nr = loige_nr
        elif peatukk_nr != last_peatukk_nr:
            answer += peatukk_nr + "\n" + paragraph_nr + "\n" + loige_nr + " " + str(df.at[start_index, "sisu_tekst"]) + "\n"
            last_loik_nr = loige_nr
            last_peatukk_nr = peatukk_nr
            last_paragraph_nr = paragraph_nr
        start_index += 1
    return answer


def get_ai_response(user_message):
    # Dialoogisüsteemi põhimeetod
    if user_message == "abi":
        return "Kui tahad küsida seaduse kohta täpselt, siis <seadus> <punkt>. Kui midagi jääb arusaamatuks," \
               " siis üritan sind suunata. Hüvasti jätmiseks, kirjuta 'Tšau'"
    # elif freim["asked_which_law"] is False and freim["akti_nimi"] != "":
    #     # Kui viimati sain seaduse kätte, aga punkte mitte
    elif freim["asked_which_law"] is True:
        if is_loik_numeration(user_message) != "":
            # Kui on punktid ka
            numeric_array = is_loik_numeration(user_message)
            numbers_removed = get_number_removed_value(user_message)
            akti_nimed_list_lower = lower_akti_nimed()
            if numbers_removed.lower() in akti_nimed_list_lower:
                freim["akti_nimi"] = numbers_removed
                freim["asked_which_law"] = False
                return if_law_in_name(numeric_array)
        else:
            # Kui punkte pole
            numbers_removed = get_number_removed_value(user_message)
            akti_nimed_list_lower = lower_akti_nimed()
            if numbers_removed.lower() in akti_nimed_list_lower:
                freim["akti_nimi"] = numbers_removed
                freim["asked_which_law"] = False
            return format_seadus()
    elif is_loik_numeration(user_message) != "":
        numeric_array = is_loik_numeration(user_message)
        numbers_removed = re.sub("(\d+\.)+", "", user_message).replace("punkt", "").lower().strip()
        akti_nimed_list_lower = lower_akti_nimed()
        akti_nimed_list = lemmatise.collect_akti_nimi()
        if numbers_removed in akti_nimed_list_lower:
            # Kui tekstis on kohe seaduse nimi olemas
            akti_nimi = numbers_removed
            freim["akti_nimi"] = akti_nimi
            # print(numeric_array)
            return if_law_in_name(numeric_array)
        else:
            empty_freim_number_values()
            numbers_removed_lemmas = Text(numbers_removed).lemmas
            possible_answers = finding_laws_with_lemmas(numbers_removed_lemmas, akti_nimed_list)
            if len(possible_answers) == 0:
                return "Vabandust, ma ei leidnud ühtegi seadust, mis sobiks. Palun proovi uuesti"
            else:
                freim["asked_which_law"] = True
                return "Kas sa otsid mõnda nendest seadustest: \n" + format_possible_laws(possible_answers)
    return "Vabandust, ma ei saanud aru."


def main():
    # Terminali puhul on see programmi põhimeetod
    if not lemmatise.check_data_exist():
        scraper.scrape()
    print("Tere! Ma olen juura robot. Aitan sul leida vajalikke asju Eesti Vabariigi seadustest. "
          "Võid minult seaduste kohta täpsemalt küsida näiteks väljendiga, '<seaduse nimi> <otsitav punkt>. "
          "Üritan sind vajaduse puhul ka suunata õigesse suunda. Kui vajad abi, "
          "siis kirjuta 'abi'. Kui ei soovi minuga enam rääkida, siis kirjuta 'Tšau'.")
    while True:
        human = str(input(">>"))
        if "Tšau" in human:
            print("Tšau!")
            break
        else:
            print(get_ai_response(human))
    return None


if __name__ == "__main__":
    main()
