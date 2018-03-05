import wgr, alphabet, lexicon

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

    def __init__(self, word, word_grammar_file, lexicon_file, alphabet_file):
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

        split_word = self.split_word(word, self.wgr._mtypes)
        meta_word = ''.join(m[1] for m in split_word)
        p, s = self.an_decode(meta_word, self.wgr._metas)

        self.word = word            # fully annotated form
        self.meta_word = meta_word  # word annotated with meta characters
        self.paradigmatic_form = p  # paradigmatic form
        self.surface_form = s       # surface form

        self.morphemes = self.get_morphemes(split_word, self.wgr._metas)
        self.lexeme = dict(self.morphemes)['lex'][0] # paradigmatic form of 'lex' morpheme
        self.lex = self.lexicon[self.lexeme]
        self.functions = self.analyze_word()

    def get_morphemes(self, split_word, metas):
        '''Returns tuples with morphemes: (mtype, (p, s, a))

        Where mtype is a string with the morpheme type,
        and p, s and a are the different realizations of the morpheme:
        p=paradigmatic form, s=surface form, a=annotated metastring
        '''
        mtypes = []
        morphemes = []
        for mtype, a in split_word:
            if mtype in mtypes:
                morphemes[mtypes.index(mtype)] += a
            else:
                mtypes.append(mtype)
                morphemes.append(a)

        # replace annotated metastring with tuple (p,s,a)
        # where p=paradigmatic form, s=surface form, a=annotated metastring
        morphemes = ((*self.an_decode(a, metas), a) for a in morphemes)

        # return tuples
        return tuple( zip(mtypes, morphemes) )

    ####################################################################
    # Morpheme operations
    ####################################################################

    def analyze_word(self):
        """Returns analyzed word functions"""
        self._jump = None   # may contain label to jump to
        self._m = {}        # contains morphemes
        self._f = {}        # contains functions

        # make dict with paradigmatic form, or None, for all morpheme types
        for mtype in self.wgr._mtypes:
            self._m[mtype.ident] = None
        for mtype, (p, s, a) in self.morphemes:
            self._m[mtype] = p

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

    def split_word(self, s, mtypes, mclass=0):
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
                result.append((prevmt.ident, s[p:l]))
                p = l + len(m[0])
                if mt.pos != 2:
                    prevmt = None
            elif l == p:
                p += len(m[0])
            elif l == -1 or l > p: # not found at current position
                # result.append((mt.ident, None))
                continue
            r = s.find(m[1], p) if m[1] else None
            if r is None:
                prevmt = mt
            elif r == -1 and l is None: # not found
                # result.append((mt.ident, None))
                continue
            elif r == -1:   # r not found, while l was found
                raise Exception(leftnotright.format(mt.ident))
            elif r >= p:
                result.append((mt.ident, s[p:r]))
                p = r + len(m[1])
        if prevmt is not None:
            result.append((prevmt.ident, s[p:]))
        return tuple(result)

    def an_decode(self, a, metas):
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
