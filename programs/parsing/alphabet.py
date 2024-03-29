import os, re

def get_alphabet(filename):
    ab = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line.strip() and line.strip()[0] != '#':
                entry = re.findall('([a-zA-Z_]*)\s+"(\\.|[^"])*"', line)
                if entry:
                    a, b = entry[0]
                    ab[c][b] = a
                else:
                    category = re.findall('([a-zA-Z_ ]*):', line)
                    if category:
                        c = category[0]
                        ab[c] = {}
    return ab

class Alphabet:

    def __init__(self, filename):
        self.alphabet = get_alphabet(filename)
        self.letters = self.alphabet['letters']
        self.diacritics = self.alphabet['diacritics']
        self.punctuation = self.alphabet['punctuation marks']


#TODO filename as argument, make class
# /projects/lib/syriac/alphabet
# script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
# filename = '../data/alphabet'
# alphabet = get_alphabet(filename)
#
# letters = alphabet['letters']
# diacritics = alphabet['diacritics']
# punctuation = alphabet['punctuation marks']
