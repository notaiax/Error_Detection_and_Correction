#!/usr/bin/env python3
'''
Shebang
'''


import sys
import math


def main():
    '''
    Funció principal
    '''
    inputfile = sys.stdin
    outputfile = sys.stdout
    detection_code = 0
    location_code = ''
    module = 4

    original_text = inputfile.read()
    # S'eliminen salts de línia del final del text
    original_text = original_text.rstrip("\r\n")

    for char in original_text:
        detection_code += ord(char)

        # Es fa el mòdul del codi ascii del caràcter i es passa a binari
        # S'elimina el 0b que surt davant de binari al fer la conversió
        # El zfill ompla el nombre de manera que quedin dos dígits en cas de que sigui modul 4,
        #  tres en cas de que sigui modul 8, per a després llegir correctament el codi.
        location_code += ((bin(ord(char) % module))[2:]).zfill(int(math.log2(module)))

    num_separated_bits = len(location_code) % 4
    separated_bits = location_code[:num_separated_bits]
    location_code = location_code[num_separated_bits:]

    print(original_text, end=' ', file=outputfile)
    print(separated_bits, end=' ', file=outputfile)
    # S'imprimeix el codi de localització passat a hexadecimal i esborrant la 0x que
    # s'afegeix per defecte
    print(hex(int(location_code, 2))[2:].zfill(int(len(location_code)/4)), end=' ', file=outputfile)
    print((detection_code % 100), end='', file=outputfile)


if __name__ == "__main__":
    main()
