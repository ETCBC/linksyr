import os, re

def get_lexicon(filename):
    l = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            entry = re.findall('^([^#\t ]+)\s+([0-9]+)([^#]*)', line)
            if entry:
                lexeme, l_id, ann = entry[0]
                ann_list = tuple(tuple(a.split('=', 1))
                                #  for a in ann.strip().split(':') if a)
                                # since apparently some dictionaries contain
                                # vc-fields with vocalization, containing
                                # the sequence '\:' (and hopefully only that)
                                # we need to split on non-escaped colons only.
                                #  https://stackoverflow.com/a/21107911
                                for a in re.split(r'(?<!\\):', ann.strip()) if a)
                l[lexeme] = (l_id, ann_list)
    return l

class Lexicon:

    def __init__(self, filename):
        self.lexicon = get_lexicon(filename)


#TODO filename as argument, make class
# /projects/lib/syriac/alphabet
# script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
# filename = '../data/syrlex'
# lexicon = get_lexicon(filename)
