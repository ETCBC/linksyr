import wgr, alphabet, lexicon

########################################################################
#   Class wrdgrm:                                                      #
#   Word grammar                                                       #
########################################################################
class wrdgrm:
    '''Word grammar thingy

    Class with attributes and methods used by wgr.py
    to create word grammar tables, and methods to
    apply the word grammar tables to
    '''

    def __init__(self, word_grammar_file, lexicon_file, alphabet_file):
        """Init"""
        with open(word_grammar_file, 'r') as f:
            self.wgr = wgr.parse('grammar', f.read())
        self.alphabet = alphabet.get_alphabet(alphabet_file)['letters']
        self.lexicon = lexicon.get_lexicon(lexicon_file)

        self._jump = None
        # replace m and f by word object:
        # self.word = None
        self._m = {}
        self._f = {}


    ####################################################################
    # Morpheme operations
    ####################################################################

    def analyze_word(self, string):
        """Returns word object with analyzed word forms"""
        # self.word = word(string)
        self._m = {}
        self._f = {}
        w = {'morphemes': {}, 'functions': {}}
        # a=analyzed form, p=paradigmatic form, s=surface form
        for mt, a in self.split_morphemes(string):
            if a is not None:
                p, s = self.analyze_morpheme(a)
                self._m[mt] = p # store paradigmatic forms
                w['morphemes'][mt] = (p,s,a)
            else:
                self._m[mt] = None
        # apply rules one by one, which will set functions in self._f
        for rule in self.wgr._rules:
            self.apply_rule(rule)
            if self._jump == False: # TODO dirty hack
                break

        if self._f is not None:     # TODO dirty hack
            w['functions'] = self._f
            w['lex'] = self.wgr.lexicon[w['morphemes']['lex'][0]]
            return w
        else:
            raise Exception('No paradigmatic form found.')

    def split_morphemes(self, s, mclass=0):
        """Splits morphologically analyzed string into morphemes.

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
        for mt in [mt for mt in self.wgr._mtypes if mt.mclass == mclass]:
            m = mt.markers
            l = s.find(m[0], p) if m[0] else None
            if l is None:
                if prevmt is not None:
                    raise Exception(emptymarkers.format(mt.ident))
            elif l >= p and prevmt is not None:
                result.append((prevmt.ident, s[p:l]))
                p = l + len(m[0])
                prevmt = None
            elif l == p:
                p += len(m[0])
            elif l == -1 or l > p: # not found at current position
                result.append((mt.ident, None))
                continue
            r = s.find(m[1], p) if m[1] else None
            if r is None:
                prevmt = mt
            elif r == -1 and l is None: # not found
                result.append((mt.ident, None))
                continue
            elif r == -1:   # r not found, while l was found
                raise Exception(leftnotright.format(mt.ident))
            elif r >= p:
                result.append((mt.ident, s[p:r]))
                p = r + len(m[1])
        if prevmt is not None:
            result.append((prevmt.ident, s[p:]))
        return result

    def analyze_morpheme(self, a):
        """Return paradigmatic and surface forms of annotated string"""
        meta = None
        p, s = [], []  # p: paradigmatic form, s: surface form
        for c in a:
            if c in (self.wgr._metas.addition, self.wgr._metas.elision):
                meta = c
            else:
                if meta is None or meta == self.wgr._metas.addition:
                    p.append(c)
                if c != self.wgr._metas.homography and (meta is None
                        or meta == self.wgr._metas.elision):
                    s.append(c)
                meta = None
        return (''.join(p), ''.join(s))

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

class word:
    """Analyzed word"""
    def __init__():
        pass


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
