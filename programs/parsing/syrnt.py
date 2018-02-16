#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# now it works in python 2.6 and 3.x!
from __future__ import unicode_literals, print_function

import os.path
from collections import namedtuple
from constants import NT_BOOKS, SyrNT as c

# Read database location from config file
try: # allow for different module names in python 2 and 3
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

config = ConfigParser()
config.read('linksyr.conf')
datadir = config.get('syrnt','datadir')
filename = config.get('syrnt','filename')
dbpath = os.path.join(datadir, filename)
NT_OFFSET = 52  # starting id of NT books

# TODO check discrepancies between SEDRA and Syromorph NT.
# It seems that
# 521601715
# 550104214
# 562103016
# 562302606
# 580201122
# 781901718
# 782202101
# 782202102
# 782202103
# 782202104
# 782202105
# 782202106
# 782202107
# 782202108

# helper functions

def read_db_file():
    from io import open # This is for python 2.6
    with open(dbpath) as f:
        for line in f:
            yield line

def get_verse_labels():
    for book_id, (book_name, chapters) in enumerate(NT_BOOKS, NT_OFFSET):
        for chapter, versecount in enumerate(chapters, 1):
            for verse in range(1, versecount + 1):
                yield (book_name, book_id, chapter, verse)

def maketrans(s1, s2):
    '''Make a simple translation table'''
    # There are more sophisticated maketrans-functions (str.maketrans()
    # in python 3 and string.maketrans() in python 2, but they are not
    # compatible. The dictionary works in all versions from at least 2.6)
    return dict(zip([ord(a) for a in s1], [ord(a) for a in s2]))

# translation tables:
# source is always SEDRA transcription, so only need to specify 'to'.
towit = maketrans('AOKY;CEI/XW','>WXVJK<PYQC')
tosyr = maketrans('ABGDHOZKY;CLMNSEI/XRWT','ܐܒܓܕܗܘܙܚܛܝܟܠܡܢܣܥܦܨܩܪܫܬ')
notr = maketrans('','')

def postag(w):
    return w.postag

def supertag(w):
    return '+'.join([e for e in (w.prefix, w.postag, w.suffix) if e])


# class NTWord

class NTWord:

    Annotation = namedtuple('Annotation',
                    [f[0].replace(' ','_') for f in c.ANNOTATIONS])
    Location = namedtuple('Location',
                    ['book_name', 'book_id', 'chapter', 'verse', 'w_num'])

    def __init__(self, w_str, location, tr):
        if tr is not None:
            w_str = w_str.translate(tr)
        self.cons_str, a_str = w_str.split('|')
        self.location = NTWord.Location(*location)
        self.annotation = NTWord.Annotation(*[int(v) if v.isdigit() else v
                            for v in a_str.split('#')])
        self.ann_values = NTWord.Annotation(*[f[1][v] if f[1] else v
                            for f, v in zip(c.ANNOTATIONS, self.annotation)])
        # some shortcuts:
        self.stem   = self.ann_values.stem
        self.lexeme = self.ann_values.lexeme
        self.root   = self.ann_values.root
        self.prefix = self.ann_values.prefix
        self.suffix = self.ann_values.suffix
        self.seyame = self.ann_values.seyame
        self.postag = self.ann_values.grammatical_category

    def __repr__(self):
        return '<NTWord {0}: "{1}">'.format(self.get_loc_str(), self.cons_str)

    def __str__(self):
        return self.cons_str

    def get_loc_str(self):
        '''Combine location elements into fixed-length string'''
        return '{0:02}{1:02}{2:03}{3:02}'.format(*self.location[1:])
        # return get_loc_id(self.book_id, self.chapter, self.verse, self.w_num)


class SyrNT:

    def __init__(self, tr=towit):
        self._nt_verses = self._nt_verses(tr)
        self._nt_words = self._nt_words()
        self._idx = 0

    def __getitem__(self, key):
        return self._nt_words[key]

    def __len__(self):
        return len(self._nt_words)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            item = self._nt_words[self._idx]
        except IndexError:
            self._idx = 0
            raise StopIteration()
        self._idx += 1
        return item

    next = __next__ # Python 2

    def _nt_verses(self, tr):
        nt_verses = []
        for verse_label, line in zip(get_verse_labels(), read_db_file()):
            verse = [NTWord(w_str, verse_label + (w_num,), tr)
                     for w_num, w_str in enumerate(line.strip().split(), 1)]
            nt_verses.append((verse_label, verse))
        return nt_verses

    def _nt_words(self):
        return [w for l, v in self._nt_verses for w in v]

    def verses(self, label=False):
        for v in self._nt_verses:
            yield v if label else v[1]

    def words(self):
        for w in self._nt_words:
            yield w

    def tag_sentences(self, tag=postag):
        for s in self.verses():
            yield [(w.cons_str, tag(w)) for w in s]

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
    for line in SyrNT(tosyr).printlines():
        print(line)

def usage():
    print(__doc__)

if __name__ == "__main__":
        main()
