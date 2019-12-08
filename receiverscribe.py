#!/usr/bin/env python3

"""Reads from stdin and outputs to stdout the same sequence of bytes and checks
the hash byte"""

import sys
import math


def location_algorithm(bin_location_code, noisy_text, module):
    '''
    Localitza la posició on hi ha l'error iterativament
    :param bin_location_code: Codi de localització obtingut de l'script senderscribe.py
    :param noisy_text: Text amb després de passar pel vitiet.py
    :return: Posició o -1 en cas de no trobar-la
    '''
    # char_length és el nombre de caràcters que llegirà cada cop del codi de localització
    char_length = int(math.log2(module))
    pos = 0

    while bin_location_code != '':
        checker = ord(noisy_text[pos]) % module
        # int(bin_location_code[:char_length], 2) llegeig els n primers caràcters del location code
        # i els passa a enter
        if checker != int(bin_location_code[:char_length], 2):
            return pos
        # Elimina els caràcters  llegits del codi
        bin_location_code = bin_location_code[char_length:]
        pos += 1

    return -1

#recursive location algorithm
def r_l_algorithm(bin_location_code, noisy_text, module, pos, char_length):
    '''
    Localitza la posició on hi ha l'error iterativament
    :param bin_location_code: Codi de localització obtingut de l'script senderscribe.py
    :param noisy_text: Text amb després de passar pel vitiet.py
    :param pos: Per defecte és 0
    :param char_length: És int(math.log2(module))
    :return: Posició o -1 en cas de no trobar-la
    '''
    if bin_location_code == '':
        return -1

    checker = ord(noisy_text[pos]) % module
    if checker != int(bin_location_code[:char_length], 2):
        return pos

    return r_l_algorithm(bin_location_code[char_length:], noisy_text, module, pos + 1, char_length)


def main():
    '''
    Funció principal
    '''
    inputfile = sys.stdin
    outputfile = sys.stdout
    module = 4

    checker = 0
    sent_text = inputfile.read()

    # Es separen els codis i el text i es guarden a les variables corresponents
    detection_code = int(sent_text.rsplit(' ', 3)[3])
    location_code = sent_text.rsplit(' ', 3)[2]
    # Aquests son els bits separats del location code
    separated_bits_lc = sent_text.rsplit(' ', 3)[1]
    noisy_text = sent_text.rsplit(' ', 3)[0]

    for char in noisy_text:
        checker += ord(char)

    checker = checker % 100

    if detection_code == checker:
        print("OK")
    else:
        # S'uneixen les parts del codi de localització, però esborrant el 0b que quedarà al
        #  passar la segona part del codi  a binari
        bin_location_code = bin(int(location_code, 16))[2:].zfill(len(location_code) * 4)
        bin_location_code = separated_bits_lc + str(bin_location_code)

        # Utilitzar la següent línia de codi si es fa servir l'algorisme iteratiu
        pos = location_algorithm(bin_location_code, noisy_text, module)

        # Utilitzar les tres següents línies de codi si es fa servir l'algorisme recursiu
        # pos = 0
        # char_length = int(math.log2(module))
        # pos = r_l_algorithm(bin_location_code, noisy_text, module, pos, char_length)


        if pos == -1:
            print("OK", file=outputfile)
        else:
            print("KO", file=outputfile)

            # Es fa modul 100 perque si la resta dona negativa, saltarà error al convertir-ho a char
            correct_char = chr((ord(noisy_text[pos]) + (detection_code - checker)) % 100)

            # La posició es printa pos+1 perquè l'editor de text comença a contar la posició
            # des de 1 i els strings en python ho fan des de 0
            print(str(pos + 1) + " " + correct_char, file=outputfile)


if __name__ == "__main__":
    main()
