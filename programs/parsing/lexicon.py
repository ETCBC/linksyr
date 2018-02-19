import os, re

def get_lexicon(filename):
    l = {}
    with open(os.path.join(script_dir, filename), 'r') as f:
        for line in f.readlines():
            if line.strip() and line.strip()[0] != '#':
                entry = re.findall('^([^\t ]+)\s+([0-9]+):([^#]*)', line)
                if entry:
                    lexeme, l_id, ann = entry[0]
                    ann_list = [tuple(a.split('=')) for a in ann.strip().split(':')]
                    l[lexeme] = (l_id, ann_list)
    return l

#TODO filename as argument, make class
# /projects/lib/syriac/alphabet
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
filename = '../data/syrlex'
lexicon = get_lexicon(filename)
