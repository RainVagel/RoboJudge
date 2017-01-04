# -​*- coding: utf-8 -*​-

from pathlib import Path
import scraper
import os

# Selles failis toimub põhiline töö.


def check_file_up_to_date():
    # Meetod kontrollib, kas seda faili peab uuendama
    # TODO
    return True


def check_data_exist():
    # See meetod kontrollib, kas "data.xlsx" fail asub kaustas
    my_file = Path("data.xlsx")
    return my_file.is_file()


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
            input_string = str(input("Sisenstage otsing: "))
        except ValueError:
            print("Vigane sisend! Prooviga uuesti.")
        else:
            break
    # Siit algab sisendi töötlemine ning vastuse väljamõtlemine
    return None

if __name__ == "__main__":
    main()
