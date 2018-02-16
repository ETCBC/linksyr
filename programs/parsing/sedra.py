#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Read the SEDRA database

The files of the SEDRA database have been are no longer
available from bethmardutho.org, but a copy is available
in the sedrajs project of Greg Borota on github.com/peshitta.
It contains the following files:
SEDRA3.DOC      - documentation of the database
ROOTS.TXT       - roots records
LEXEMES.TXT     - lexemes records
WORDS.TXT       - words records
ENGLISH.TXT     - english translations records
ETIMOLGY.TXT    - etymology records

BFBS.README.TXT - documentation of the NT text
BFBS.TXT        - the NT text

The BFBS files contain, according to the README file,
   BFBSREC.TXT  - The text of the Syriac New Testament according to the
                  British and Foreign Bible Society's Edition
   FEATURRE.TXT - A list of all the words in BFBSREC.TXT with morphological
                  information.

Although the filenames differ, besides other minor inconsistencies,
the description seems to apply roughly to BFBS.TXT.
"""
# The SEDRA III database is read into the variable db,
# the New Testament text is read into the variable nt.
# TODO
# Not all attributes and features are clearly explained
# in the documentation, so some research may improve
# their usefulness.
# TODO
# Add values for prefix-attribute in constants.py, and
# find a way to reconstruct suffixes, and add relevant
# attributes/methods to Word class.
# TODO
# With the prefixes and suffixes, make a supertag-method
# for the NTWord-class.
# TODO
# Add documentation to classes/methods.

# now it works in python 2.[67] and 3.x!
from __future__ import unicode_literals, print_function
import os
from collections import namedtuple
from constants import NT_BOOKS, SedraIII as c

CFG_FILENAME = 'linksyr.conf'
CFG_SECTION = 'sedra'
CFG_FIELDS = ('datadir',
              'roots',
              'lexemes',
              'words',
              'english',
              'etymology',
              'nt')

# Read database location from config file
try: # allow for different module names in python 2 and 3
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
cfg = ConfigParser()
cfg.read(CFG_FILENAME)
CFG_ITEMS = dict(cfg.items(CFG_SECTION))

DB_DIR = CFG_ITEMS[CFG_FIELDS[0]]
# DB_FILES = tuple(CFG_ITEMS[s] for s in CFG_FIELDS[1:6])
NT_FILE = CFG_ITEMS[CFG_FIELDS[6]]
NT_OFFSET = 52  # starting id of NT books


# helper functions
def read_db_file(db_dir, filename):
    from csv import reader
    with open(os.path.join(db_dir, filename), 'r') as f:
        for line in reader(f):
            try:        # csv.reader in python 2 does not support Unicode
                line = [e.decode('utf-8') for e in line]
            except AttributeError:
                pass    # for Python 3, no decoding is possible/necessary
            yield line

def get_identifier(o):
    return '<{0}.{1} {2}: "{3}">'.format(
        o.__module__, o.__class__.__name__, o.id, o.__str__())

def get_address(a):
    return tuple(int(e) for e in a.split(':')) if a != 'NULL' else None

def get_values(n, fields):
    # TODO calculating bit groups for every record may be inefficient,
    # maybe it could be done once in a class variable?
    bit_groups = [f_bits for (f_name, f_bits, f_values) in fields]
    bits = 32 if sum(bit_groups) > 16 else 16
    values = split_bits(n, bit_groups, bits)
    return [(l[2][n] if l[2] else n) for l, n in zip(fields, values)]

def split_bits(n, groups, bits=16):
    if n<0: n+=(1<<bits) # shift bits https://stackoverflow.com/a/20768199
    b = '{0:0{1}b}'.format(n, bits) # convert to binary
    result = []
    start = None
    for size in groups:
        end = start-size if start is not None else -size
        result.append(int(b[end:start], 2)) # convert slice back to int
        start = end
    return tuple(result)

def maketrans(s1, s2):
    '''Make a simple translation table'''
    # There are more sophisticated maketrans-functions (str.maketrans()
    # in python 3 and string.maketrans() in python 2, but they are not
    # compatible. The dictionary works in all versions from at least 2.6)
    return dict(zip([ord(a) for a in s1], [ord(a) for a in s2]))

# translation tables:
# source is always SEDRA transcription, so only need to specify 'to'.
towit = maketrans("AOKY;CEI/XW*,'oaeiu",'>WXVJK<PYQC"#^A@EIU')
tosyr = maketrans("ABGDHOZKY;CLMNSEI/XRWT*,'_oaeiu",'ܐܒܓܕܗܘܙܚܛܝܟܠܡܢܣܥܦܨܩܪܫܬ̣̱̈̇ܳܰܶܺܽ')
notr = maketrans('','')


# classes

class Root:
    # example input line: 0:1,"AAR","aat          |0",0

    Attributes = namedtuple('Attributes',
                    [f[0].strip('<>').replace(' ','_') for f in c.ROOTS_ATTR])

    def __init__(self, line, file_no, name, db):
        tr = db._tr
        self.file_no = file_no
        self.name = name
        self.db = db
        self.id = int(line[0].split(':')[1])
        self.rt_str = line[1] if tr is None else line[1].translate(tr)
        self.sort_str = line[2]
        self.attr = int(line[3])
        attr_values = get_values(self.attr, c.ROOTS_ATTR)
        self.attributes = Root.Attributes(*attr_values)
        # empty slot for lexemes
        self._lexemes = None

    def __repr__(self):
        return get_identifier(self)

    def __str__(self):
        return self.rt_str

    @property
    def lexemes(self):
        if self._lexemes is None:
            self._lexemes = self.db.filter('lexemes', 'root_addr', self.id)
        return self._lexemes


class Lexeme:
    # example input line: 1:2,0:2,"ABA",41960448,16

    Attributes = namedtuple('Attributes',
                    [f[0].strip('<>').replace(' ','_') for f in c.LEXEMES_ATTR])
    Features = namedtuple('Features',
                    [f[0].strip('<>').replace(' ','_') for f in c.LEXEMES_FEAT])

    def __init__(self, line, file_no, name, db):
        tr = db._tr
        self.file_no = file_no
        self.name = name
        self.db = db
        self.id = int(line[0].split(':')[1])
        self.root_addr = get_address(line[1])
        self.lex_str = line[2] if tr is None else line[2].translate(tr)
        self.feat = int(line[3])
        feat_values = get_values(self.feat, c.LEXEMES_FEAT)
        self.features = Lexeme.Features(*feat_values)
        self.attr = int(line[4])
        attr_values = get_values(self.attr, c.LEXEMES_ATTR)
        self.attributes = Lexeme.Attributes(*attr_values)
        # shortcut to root
        self.root = db.get(self.root_addr)
        # empty slots for other properties, accessed with @property decorator
        self._english = None # not yet available, initialized on first request
        self._words = None
        self._etymology = None


    def __repr__(self):
        return get_identifier(self)

    def __str__(self):
        return self.lex_str

    @property
    def english(self):
        if self._english is None:
            self._english = self.db.filter('english', 'lex_addr', self.id)
        return self._english

    @property
    def words(self):
        if self._words is None:
            self._words = self.db.filter('words', 'lex_addr', self.id)
        return self._words

    @property
    def etymology(self):
        if self._etymology is None:
            self._etymology = self.db.filter('etymology', 'lex_addr', self.id)
        return self._etymology[0] if self._etymology else None


class Word:
    # example input line: 2:3,1:1,"DAAR","D'oAAaR",558080,128

    Attributes = namedtuple('Attributes',
                    [f[0].strip('<>').replace(' ','_') for f in c.WORDS_ATTR])
    Features = namedtuple('Features',
                    [f[0].strip('<>').replace(' ','_').replace('/','_') for f in c.WORDS_FEAT])

    def __init__(self, line, file_no, name, db):
        tr = db._tr
        self.file_no = file_no
        self.name = name
        self.db = db
        self.id = int(line[0].split(':')[1])
        self.lex_addr = get_address(line[1])
        self.cons_str = line[2] if tr is None else line[2].translate(tr)
        self.voc_str = line[3] if tr is None else line[3].translate(tr)
        # correct transcription of digraph #_ in WIT transcription
        if tr == towit and '_' in self.voc_str:
            self.voc_str = self.voc_str.replace('_', '#_')
        self.feat = int(line[4])
        feat_values = get_values(self.feat, c.WORDS_FEAT)
        self.features = Word.Features(*feat_values)
        self.attr = int(line[5])
        attr_values = get_values(self.attr, c.WORDS_ATTR)
        self.attributes = Word.Attributes(*attr_values)
        # shortcuts to lexeme and root objects
        self.lexeme = db.get(self.lex_addr)
        self.root = self.lexeme.root if self.lexeme else None

    def __repr__(self):
        return get_identifier(self)

    def __str__(self):
        return self.cons_str


class English:
    # example input line: 3:36,1:22,"land","parcel of","","",0,0

    Attributes = namedtuple('Attributes',
                    [f[0].strip('<>').replace(' ','_') for f in c.ENGLISH_ATTR])

    def __init__(self, line, file_no, name, db):
        self.file_no = file_no
        self.name = name
        self.db = db
        self.id = int(line[0].split(':')[1])
        self.lex_addr = get_address(line[1])
        self.meaning = line[2]
        self.before = line[3]
        self.after = line[4]
        self.comment = line[5]
        self.attr = int(line[6])
        attr_values = get_values(self.attr, c.ENGLISH_ATTR)
        self.attributes = English.Attributes(*attr_values)
        self.ignore = int(line[7])
        self._words = None
        # shortcut to lexeme
        self.lexeme = db.get(self.lex_addr)

    def __repr__(self):
        return get_identifier(self)

    def __str__(self):
        return self.meaning


class Etymology:
    # example input line: 4:5,1:46,"eu\255jaristi\256a",5

    Attributes = namedtuple('Attributes',
                    [f[0].strip('<>').replace(' ','_') for f in c.ETYMOLOGY_ATTR])

    def __init__(self, line, file_no, name, db):
        self.file_no = file_no
        self.name = name
        self.db = db
        self.id = int(line[0].split(':')[1])    # Record address, e.g. 4:1
        self.lex_addr = get_address(line[1])    # Lexeme address (in LEXEMES.TXT), e.g. 1:1
        self.word_origin = line[2]              # Word Origin, e.g. "a\255h\256r"
        self.attr = int(line[3])
        attr_values = get_values(self.attr, c.ETYMOLOGY_ATTR)
        self.attributes = Etymology.Attributes(*attr_values)
        # shortcut to lexeme
        self.lexeme = db.get(self.lex_addr)

    def __repr__(self):
        return get_identifier(self)

    def __str__(self):
        # return self.attributes[0] # ['LANGUAGE']
        return '{0} from {1}: {2}'.format(
            self.lexeme, self.attributes[0], self.word_origin)


class SedraIII:

    files = 'roots', 'lexemes', 'words', 'english', 'etymology'
    classes = Root, Lexeme, Word, English, Etymology
    db_classes = (('roots',     Root),
                  ('lexemes',   Lexeme),
                  ('words',     Word),
                  ('english',   English),
                  ('etymology', Etymology))

    def __init__(self, tr=towit):
        self._tr = tr
        self._dicts = {}
        for file_no, (name, db_class) in enumerate(SedraIII.db_classes): # zip(SedraIII.files, SedraIII.classes):
            addr_dict, db = self._import_db(file_no, name, db_class)
            self._dicts[file_no] = addr_dict
            setattr(self, name, db)

    def get(self, address):
        '''Get record by address tuple'''
        if address is None:
            return None
        else:
            f, r = address # file, record
            return self._dicts[f][r]

    def filter(self, db_file, key, search_id):
        '''Get list of all records in db_file where key == search_id'''
        return [e for e in getattr(self, db_file)
                if getattr(e, key) is not None
                and getattr(e, key)[1] == search_id]


    def _import_db(self, file_no, name, db_class):
        addr_dict = {}
        db = []
        for line in read_db_file(DB_DIR, CFG_ITEMS[name]):
            e = db_class(line, file_no, name, self)
            addr_dict[e.id] = e
            db.append(e)
        return (addr_dict, tuple(db))


class NTWord:
    # example input line: 0:6,520100106,33558659,24

    Location = namedtuple('Location',
                    ['book_name', 'book_id', 'chapter', 'verse', 'w_num'])

    def __init__(self, line, db):
        self.db = db
        # self.rec_addr = line[0]  # rec_addr is not unique, so useless as id
        self.id = int(line[1]) # use location id as identifier instead
        self.location = NTWord.Location(*self._get_location(line[1]))
        self.word_addr = self._get_word_addr(line[2]) # tuple, e.g. (2,1)
        self.attr = int(line[3])
        self.attributes = self.attr # TODO find attribute description
        self.attr_bits = '{0:016b}'.format(self.attr) # for easier inspection
        # shortcuts to db object attributes
        self.word = db.get(self.word_addr)
        self.lexeme = self.word.lexeme
        self.root = self.word.root
        self.cons_str = self.word.cons_str

    def __repr__(self):
        return get_identifier(self)

    def __str__(self):
        return self.word.__str__()

    def _get_word_addr(self, a):
        # word_addr is a crazy encoded decimal value of two combined
        # hexadecimal values, the first of which is always '02'
        # (the number of the WORDS.TXT file). So to retrieve
        # the word_id, we must convert word_addr to a hex string
        # of eight positions, and convert the rightmost six back
        # to decimal. The leftmost two will always be '02'.
        h = '{0:08x}'.format(int(a))
        return (int(h[:2], 16), int(h[2:], 16))

    def _get_location(self, s):
        loc_id = tuple(int(e) for e in (s[:2], s[2:4], s[4:7], s[7:]))
        book_name = NT_BOOKS[loc_id[0]-NT_OFFSET][0]
        return (book_name,) + loc_id


class BFBS:

    def __init__(self, tr = towit, db = None):
        if db == None:
            db = SedraIII(tr=tr)
        self.db = db
        self.nt = self._read_nt_file()

    def __getitem__(self, key):
        return self.nt[key]

    def _read_nt_file(self):
        nt = []
        for line in read_db_file(DB_DIR, NT_FILE):
            nt.append(NTWord(line, self.db))
        # since source file is not sorted properly, need to sort list first
        nt.sort(key=lambda w: w.id)
        return tuple(nt)

    def verses(self, label = False):
        verse = []
        verse_label = self.nt[0].location[:4]
        for word in self.nt:
            if word.location[:4] != verse_label:
                yield (verse_label, verse) if label else verse
                verse = []
                verse_label = word.location[:4]
            verse.append(word)
        yield (verse_label, verse) if label else verse

    def words(self):
        for w in self.nt:
            yield w

    def printlines(self):
        pl = None # pl: previous label
        for l, v in self.verses(label=True):
            if pl is None or pl[1] != l[1] or pl[2] != l[2]:
                if pl is not None:  # no newline before first chapter
                    yield ''
                yield '{0} chapter {1}'.format(l[0], l[2])
            pl = l
            yield '{0:2} {1}'.format(l[3], ' '.join([w.cons_str for w in v]))


def main():
    for line in BFBS(tosyr).printlines():
        print(line)

def usage():
    print(__doc__)

if __name__ == "__main__":
        main()
