#!/usr/bin/env python

"""A simple python script template.
"""

import random

def main():
    correct_files_list = ["regulaminy/avans", "regulaminy/cortland", "regulaminy/euro", "regulaminy/neonet", "regulaminy/saturn", "regulaminy/xkom", "ustawy/ustawa_o_ochronie_konkurencji_i_konsumentow", "ustawy/ustawa_o_swiadczeniu_uslug_droga_elektroniczna_jednolity"]
    incorrect_files_list = ["klauzule/dostawa_energii_wody_gazu_i_ciepła", "klauzule/edukacja", "klauzule/handel_elektroniczny", 
        "klauzule/inne_uslugi", "klauzule/internet", "klauzule/nieruchomosci", "klauzule/sprzedaz_konsumencka", "klauzule/system_argentynski",
        "klauzule/telewizja_kablowa_i_satelitarna", "klauzule/turystyka", "klauzule/uslugi_bankowe", "klauzule/uslugi_finansowe", "klauzule/uslugi_internetowe", 
        "klauzule/uslugi_telekomunikacyjne", "klauzule/uslugi_ubezpieczeniowe"]

    correct_sentences_set = set()
    incorrect_sentences_set = set()

    for file_name in correct_files_list:
        with open(file_name) as file:
            correct_sentences_set |=  set(map(lambda line: line.rstrip(), file.readlines()))

    for file_name in incorrect_files_list:
        with open(file_name) as file:
            incorrect_sentences_set |=  set(map(lambda line: line.rstrip(), file.readlines()))

    shuffled_correct_sentences_list = list(correct_sentences_set)
    random.shuffle(shuffled_correct_sentences_list)
    shuffled_correct_sentences_list_pivot = int(len(shuffled_correct_sentences_list) * 0.8)

    shuffled_incorrect_sentences_list = list(incorrect_sentences_set)
    random.shuffle(shuffled_incorrect_sentences_list)
    shuffled_incorrect_sentences_list_pivot = int(len(shuffled_incorrect_sentences_list) * 0.8)

    with open("train_set.txt", 'w') as train_set:
        for sentence in shuffled_correct_sentences_list[:shuffled_correct_sentences_list_pivot]:
            train_set.write("correct\t"+sentence+"\n")

        for sentence in shuffled_incorrect_sentences_list[:shuffled_incorrect_sentences_list_pivot]:
            train_set.write("incorrect\t"+sentence+"\n")

    with open("test_set_correct.txt", 'w') as test_set_correct:
        for sentence in shuffled_correct_sentences_list[shuffled_correct_sentences_list_pivot:]:
            test_set_correct.write("correct\t"+sentence+"\n")

    with open("test_set_incorrect.txt", 'w') as test_set_incorrect:
        for sentence in shuffled_incorrect_sentences_list[shuffled_incorrect_sentences_list_pivot:]:
            test_set_incorrect.write("incorrect\t"+sentence+"\n")

if __name__ == '__main__':
    main()