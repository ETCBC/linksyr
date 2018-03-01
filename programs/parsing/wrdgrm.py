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
        # self.alphabet = alphabet.get_alphabet(alphabet_file)['letters']
        # self.lexicon = lexicon.get_lexicon(lexicon_file)
        self.alphabet = alphabet.Alphabet(alphabet_file).letters
        self.lexicon = lexicon.Lexicon(lexicon_file).lexicon
        # wgr also needs attribute lexicon, esp on line 337
        # (in the method implicit_enum()):
        # ``` W.addmvenum(mtid, getattr(W, T_IDENTIFIER)) ```
        # where T_IDENTIFIER can only have the value 'lexicon'.
        # TODO: find better way to pass the lexicon to wgr
        wgr.W.lexicon = self.lexicon

        with open(word_grammar_file, 'r') as f:
            self.wgr = wgr.parse('grammar', f.read())


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
        morphemes = []
        surface_form = '' # this is the surface form of the whole word
        # a=analyzed form, p=paradigmatic form, s=surface form (of the morpheme)
        for mt, a in self.split_morphemes(string):
            # Previously, infixes were not handled properly by split_morphemes(),
            # so after a lexeme was interrupted by an infix, the second part of
            # the lexeme (and therefore also the rest of the word) were not
            # recognized.
            # By checking if the current morpheme type is 2 (i.e. infix), and
            # if so not closing the previous morpheme by setting prevmt to None,
            # the remainder of the lexeme is also recognized.
            # However, since the lexeme parts are now separate items in the
            # morphemes list, they have to be joined together in analyze_word().
            # An alternative would be to join them together already in
            # split_morphemes(), but then the surface_form cannot be recovered
            # since the position of the infix is unknown. A possibly easier
            # way could be to have split_morphemes() also return the
            # surface_form.
            if a is not None:
                p, s = self.an_decode(a)
                surface_form += s
                if mt not in self._m:
                    self._m[mt] = p # store paradigmatic forms
                    morphemes.append((mt, (p,s,a)))
                else: # if mt is already registered it is apparently a lexeme split by an infix
                    self._m[mt] += p # combine parts of paradigmatic form
                    # then find the mt in the morphemes list, and combine
                    i,m = [(i,m) for i,m in enumerate(morphemes) if m[0]==mt][0]
                    morphemes[i] = (mt, tuple(x+y for x,y in zip(m[1],(p,s,a))))
            else:
                self._m[mt] = None
        # apply rules one by one, which will set functions in self._f
        for rule in self.wgr._rules:
            self.apply_rule(rule)
            if self._jump == False: # TODO dirty hack
                break

        if self._f is not None:     # TODO dirty hack
            lexeme = dict(morphemes)['lex'][0]
            lex = self.lexicon[lexeme]

            # update functions with values from lexicon
            for f, v in lex[1]: # loop through descriptions in lexicon
                if f in self.wgr._fvalues: # check if function name is valid
                    # Values from lexicon always take precedence,
                    # also if the value was already set, even to False.
                    self._f[f] = v

            functions = tuple(self._f.items())

            return (surface_form, tuple(morphemes), functions, lex)

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
                if mt.pos != 2:
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

    def an_decode(self, a):
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
