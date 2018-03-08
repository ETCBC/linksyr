import wgr, alphabet, lexicon
from collections import namedtuple


########################################################################
#   Class WordGrammar:                                                 #
#   Word grammar                                                       #
########################################################################
class WordGrammar:
    '''Word grammar thingy

    Class with attributes and methods used by wgr.py
    to create word grammar tables, and methods to
    apply the word grammar tables to
    '''

    _morpheme_type = namedtuple('MORPHEME_TYPE',
        ['ident', 'mclass', 'pos', 'markers'])
    _meta_keys = namedtuple('META_KEYS',
        ['addition', 'elision', 'root_sep', 'homography'])

    def __init__(self, word_grammar_file, lexicon_file): # , alphabet_file):
        """Set initial values"""

        # export current word grammar object to wgr module
        wgr.W = self

        # set lexicon and alphabet
        self.lexicon = lexicon.Lexicon(lexicon_file).lexicon
        # self.alphabet = alphabet.Alphabet(alphabet_file).letters # not used

        self._ds = {}       # descriptive strings
        self._mclass = None # morpheme class: mc_inflection or mc_derivation
        self._mtypes = []   # list of morpheme types and markers
        self._mvalues = {}  # lists of possible values per mtype
        self._fvalues = {}  # lists of possible values per function
        self._metas = None  # meta symbols
        self._rules = []    # word grammar rules

        with open(word_grammar_file, 'r') as f:
            text = f.read()

        # The wgr functions will set the attributes of wgr.W,
        # which is this WordGrammar object (set above: wgr.W = self)
        wgr.parse('grammar', text)

    def analyze(self, word):
        '''Return Word object with word analyses'''
        return Word(word, self)

    def desc(self, name):
        '''Return descriptive string for name'''
        return self._ds[name]

    #### FUNCTIONS USED BY wgr.py ####

    def reset(self):
        # TODO remove call to this function from wgr.[py|g]
        pass

    def setmclass(self, mclass):
        """Set morpheme class: mc_inflection or mc_derivation"""
        self._mclass = mclass

    def getmclass(self):
        """Get morpheme class: mc_inflection or mc_derivation"""
        return self._mclass

    def addmt(self, mtid, p, m, ds):
        """Add new morpheme type"""
        self._mtypes.append(
            self._morpheme_type(mtid, self._mclass, p, m))
        self._ds[mtid] = ds
        # self._values[mtid] = None

    def addmvenum(self, mtid, mvenum):
        """Add new list of morpheme values"""
        self._mvalues[mtid] = mvenum

    def addwf(self, wfid, ds):
        """Add new word function"""
        self._ds[wfid] = ds
        # self._values[wfid] = None

    def addfv(self, fvid, ds):
        """Add new word function value descriptive string"""
        self._ds[fvid] = ds

    def addfvenum(self, wfid, fvenum):
        """Add new list of word function values"""
        self._fvalues[wfid] = fvenum

    def getds(self, ident):
        """Return description string for identifier"""
        return self._ds[ident]

    def setmetas(self, metas):
        """Add meta symbols"""
        if self._metas:
            raise Exception('Meta symbols already set')
        self._metas = self._meta_keys._make(metas)

    def getmetas(self, s=None):
        """Return meta symbols"""
        if not self._metas:
            raise Exception('Meta symbols not set')
        return self._metas

    def addrule(self, rule, mclass=0):
        """Add word grammar rule"""
        self._rules.append(rule)


########################################################################
#   Class Word:                                                        #
#   Analyzed word                                                      #
########################################################################
class Word:
    '''Word grammar thingy

    Class with attributes and methods used by wgr.py
    to create word grammar tables, and methods to
    apply the word grammar tables to
    '''

    def __init__(self, word, word_grammar):
        """Init"""
        self.wgr = word_grammar

        # word_elements is a tuple with all word elements in the order they
        # were found in the annotated string. It is needed to reconstruct
        # the surface form, since the location of e.g. infixes in lexemes
        # cannot be determined from the morphemes list.
        word_elements = split_word(word, self.wgr._mtypes)

        # meta_form with meta characters, without patterns (mt.pos 4)
        a = ''.join(e for mt, e in word_elements if mt.pos != 4)
        p, s = an_decode(a, self.wgr._metas)

        self.word = word            # fully annotated form
        self.meta_form = a          # word annotated with meta characters
        self.paradigmatic_form = p  # paradigmatic form
        self.surface_form = s       # surface form

        self.morphemes = get_morphemes(word_elements, self.wgr._metas)
        self.lexeme = next(m.p for m in self.morphemes if m.mt.pos == 1)
        self.lex = self.wgr.lexicon[self.lexeme]
        self.functions = self.analyze_word()

    def dmp_str(self, title, verse):
        heading = f'{title} {verse}'
        func_str = get_func_str(self.functions)
        affix_str = get_affix_str(self.morphemes)
        return '\t'.join((heading, self.word, self.surface_form, self.lexeme, affix_str, func_str))

    ####################################################################
    # Morpheme operations
    ####################################################################

    def analyze_word(self):
        """Returns analyzed word functions"""
        self._jump = None   # may contain label to jump to
        self._m = {}        # contains morphemes
        self._f = {}        # contains functions

        # make dict with paradigmatic form, or None, for all morpheme types
        for mt in self.wgr._mtypes:
            self._m[mt.ident] = None
        for m in self.morphemes:
            self._m[m.mt.ident] = m.p

        # apply all rules from the grammar
        for rule in self.wgr._rules:
            self.apply_rule(rule)
            if self._jump == False: # TODO dirty hack
                break

        # If self._f is None, no paradigmatic form was found. That should
        # probably be indicated in a more elegant way such as an Exception
        if self._f is None:     # TODO dirty hack
            raise ValueError('No paradigmatic form found.')
        else:
            # update functions with values from lexicon
            for f, v in self.lex[1]: # loop through descriptions in lexicon
                if f in self.wgr._fvalues: # check if function name is valid
                    # Values from lexicon always take precedence,
                    # also if the value was already set, even to False.
                    self._f[f] = v

        return tuple(self._f.items())

    ####################################################################
    # Rules
    ####################################################################
    def apply_rule(self, r):
        k, v = r # key, value = rule
        if self._jump is not None:
            if k == 'label':
                label, rule = v
                if label == self._jump:
                    self.apply_rule(rule)
        elif k == 'simple_rule':
            expr, actions = v
            if self.evaluate(expr):
                for action in actions:
                    self.perform_action(action)
        elif k == 'block':
            (expr, actions), rules = v
            if self.evaluate(expr):
                for action in actions if actions else []:
                    self.perform_action(action)
                for rule in rules:
                    self.apply_rule(rule)

    ####################################################################
    # Actions
    ####################################################################
    def perform_action(self, action):
        k, v = action
        # attribution
        if k == 'assignment':
            function, value = v
            self._f[function] = value # assign value to function
        elif k == 'exclusion':
            self._f[v] = False # exclude function v from self._f
        elif k == 'inclusion':
            self._f[v] = None # include function v in self._f
        # shift
        elif k == 'jump':
            self._jump = v
        elif k == 'accept':
            self._jump = False  # TODO looks like dirty hack to stop processing
        elif k == 'reject':
            self._jump = False  # TODO looks like dirty hack to stop processing
            self._f = None      # TODO another dirty hack?

    ####################################################################
    # Expression evaluation
    ####################################################################
    def evaluate(self, expr):
        """Evaluate expression, return boolean"""
        # TODO values not in self._values but separate object
        k, v = expr
        if k == 'exist':
            return self._m[v] != None
        elif k == 'not':
            return self.evaluate(v) == False
        elif k == 'cmp':            # equals is True for '=='
            ident, val, equals = v  #       or False for '!='
            return (self._m[ident] in val) == equals
        elif k == 'and':
            for t in v:
                if not self.evaluate(t):
                    return False
            return True
        elif k == 'or':
            for e in v:
                if self.evaluate(e):
                    return True
            return False

# helper functions for Word class
def split_word(s, mtypes, mclass=0):
    """Splits morphologically analyzed word into morphemes.

    Returns a list of tuples with as first member the
    morpheme type identifier, and as second member the
    found morpheme, or None if it was not found.
    """
    # Message strings
    emptymarkers = '{}: Empty left marker after empty right marker.'
    leftnotright = '{}: Found left marker but not right marker.'

    result = []

    p = 0           # position in string
    prevmt = None   # previous morpheme type - set when right marker
                    # is not set, so end cannot yet be determined
    for mt in (mt for mt in mtypes if mt.mclass == mclass):
        m = mt.markers
        l = s.find(m[0], p) if m[0] else None
        if l is None:
            if prevmt is not None:
                raise Exception(emptymarkers.format(mt.ident))
        elif l >= p and prevmt is not None:
            result.append((prevmt, s[p:l]))
            p = l + len(m[0])
            if mt.pos != 2:
                prevmt = None
        elif l == p:
            p += len(m[0])
        elif l == -1 or l > p: # not found at current position
            # result.append((mt, None))
            continue
        r = s.find(m[1], p) if m[1] else None
        if r is None:
            prevmt = mt
        elif r == -1 and l is None: # not found
            # result.append((mt, None))
            continue
        elif r == -1:   # r not found, while l was found
            raise Exception(leftnotright.format(mt.ident))
        elif r >= p:
            result.append((mt, s[p:r]))
            p = r + len(m[1])
    if prevmt is not None:
        result.append((prevmt, s[p:]))
    return tuple(result)

def get_morphemes(word_elements, metas):
    '''Returns tuples with morphemes: (mtype, (p, s, a))

    Where mtype is a string with the morpheme type,
    and p, s and a are the different realizations of the morpheme:
    p=paradigmatic form, s=surface form, a=annotated metastring
    '''
    mtypes = []
    a_strs = []
    morphemes = []

    for mt, a in word_elements:
        if mt in mtypes:
            a_strs[mtypes.index(mt)] += a
        else:
            mtypes.append(mt)
            a_strs.append(a)

    # p=paradigmatic form, s=surface form, a=annotated metastring
    for mt, a in zip(mtypes, a_strs):
        p, s = an_decode(a, metas)
        morphemes.append(Morpheme(mt, p, s, a))

    return tuple(morphemes)

def an_decode(a, metas):
    """Return paradigmatic and surface forms of annotated string"""

    meta = None
    p, s = [], []  # p: paradigmatic form, s: surface form

    for c in a:
        if c in (metas.addition, metas.elision):
            meta = c
        else:
            if meta is None or meta == metas.addition:
                p.append(c)
            if c != metas.homography and (meta is None
                    or meta == metas.elision):
                s.append(c)
            meta = None

    return (''.join(p), ''.join(s))

# helper functions for Word.get_dmp_str()
def get_affix_str(morphemes):
    affixes = []
    for m in (m for m in morphemes if m.mt.pos != 1):  # ignore lexemes
            affixes.append(f'{m.mt.ident}="{m.p}"' if m.mt.pos != 4
                           else f'{m.mt.ident}={m.p}') # no quotes around patterns
    return ','.join(affixes)

def get_func_str(functions):
    return ','.join(('+'+fn if fv is None else fn+'='+fv for fn, fv in functions if fv != False))


########################################################################
#   Class Morpheme:                                                    #
#   so small, it could just as well be a namedtuple                    #
########################################################################
class Morpheme:
    '''Morpheme class'''

    def __init__(self, mt, p, s, a):
        self.mt = mt
        self.p = p
        self.s = s
        self.a = a


########################################################################
#   Class pfp:                                                         #
#   Paradigmatic form parser                                           #
########################################################################
class pfp:
    """Paradigmatic form parser

    Checks that morphemes are correctly made up
    of alphabetic and morpheme symbols.
    """
    def __init__(self):
        self._alphabet = []
        self._homography = []

    def load(self, a, s):
        """Load pfp variables

        a contains alphabet,
        s the homograph marker
        """
        self._alphabet = set(a)
        self._homography = s

    def parse(self, s):
        """Attempts to parse string s

        Returns (g, h) if successful, where g is the
        grapheme string and h the homograph number.
        Returns False if unsuccessful.
        """
        if not self._alphabet or not self._homography:
            raise Exception('Pfp not initialized')
        g, h = [], 0
        for c in s:
            if h == 0 and c in self._alphabet:
                g.append(c)
            elif c in self._homography:
                h += 1
            else:
                return False
        return (''.join(g), h)
