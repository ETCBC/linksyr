
# preparser

from collections import namedtuple
# import alphabet, lexicon

class word_grammar:
    '''Word grammar thingy

    Class with attributes and methods used by wgr.py
    to create word grammar tables, and methods to
    apply the word grammar tables to
    '''
    # class variables
    # alphabet = alphabet.letters
    # lexicon = lexicon.lexicon
    _morpheme_type = namedtuple('MORPHEME_TYPE',
        ['ident', 'mclass', 'pos', 'markers'])
    _meta_keys = namedtuple('META_KEYS',
        ['addition', 'elision', 'root_sep', 'homography'])

    def __init__(self):
        self.reset() # possible to reuse object for new grammar

    def reset(self):
        """Set or reset initial values"""
        # object/instance variables
        self._ds = {}       # descriptive strings
        self._mclass = None # morpheme class: mc_inflection or mc_derivation
        self._mtypes = []   # list of morpheme types and markers
        self._mvalues = {}  # lists of possible values per mtype
        self._fvalues = {}  # lists of possible values per function
        self._metas = None  # meta symbols
        self._rules = []    # word grammar rules

    def setmclass(self, mclass):
        """Set morpheme class: mc_inflection or mc_derivation"""
        self._mclass = mclass

    def getmclass(self):
        """Get morpheme class: mc_inflection or mc_derivation"""
        return self._mclass

    # mtid: string, morpheme type id (e.g. pfm, lex, etc)
    # p:    int, position (e.g. 0=prefix, 1=core, 2=infix, etc)
    # m:    list with strings or None, markers
    # ds:   string, descriptive string
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

%%

# Uiteindelijk moeten we een parser hebben,
# die een string accepteert, en een lijst
# terugstuurt, met
# - het lexeem
# - de oppervlaktevorm
# - de 'paradigmatische' vorm
# - de morfologische onderdelen
# - de grammaticale functies zoals
#   gedefinieerd in de 'word grammar'
#
# Eerst wordt in de word grammar de morfologie
# vastgesteld, bestaande uit 'inflection' en
# 'derivation'. Momenteel wordt 'derivation'
# niet gebruikt. Beide kunnen bestaan uit
# vier onderdelen, die elk door verschillende
# in de word grammar vast te leggen elementen
# ingevuld kunnen worden: prefix, core, infix,
# suffix, en pattern.

parser wgr:

    # ignore whitespace
    ignore:                     '\\s+'

    # ignore comments - but this means that the pound sign
    # cannot be used at all in the word grammar files!
    ignore:                     '#[^\\n]*'

    # Definitions and reserved words adapted from lexer.l
    # Since yapps chooses the first matching token pattern,
    # the more specific patterns (i.e. the reserved words)
    # are declared first, then the more general patterns.

    # /* Reserved words */

    token T_ACCEPT:             "accept"
    token T_CORE:               "core"
    token T_DERIVATION:         "derivation"
    token T_END:                "end"
    token T_EXIST:              "exist"
    token T_FORMS:              "forms"
    token T_FUNCTIONS:          "functions"
    token T_GOTO:               "goto"
    token T_INFIX:              "infix"
    token T_INFLECTION:         "inflection"
    token T_LABEL:              "label"
    token T_LEXICAL:            "lexical"
    token T_META:               "meta"
    token T_NOT:                "not"
    token T_PATTERN:            "pattern"
    token T_PREFIX:             "prefix"
    token T_REJECT:             "reject"
    token T_RULES:              "rules"
    token T_SHARED:             "shared"
    token T_SUFFIX:             "suffix"
    token T_WORD:               "word"

    # /* Definitions */

    token T_ACTION_OPERATOR:    "::"
    token T_AND:                "&&"
    token T_CHARACTER:          '.'
    token T_COMMENT:            '#.*'
    token T_EQUALITY:           "=="
    token T_IDENTIFIER:         '[A-Za-z_][A-Za-z0-9_]*'
    token T_INEQUALITY:         "!="
    token T_STRING:             '\"[^"]*\"'
    token T_LWSP:               '[\\t\\v\\f\\r ]+'
    token T_OR:                 "\|\|"

    token END:                  "$"

    # /* Grammar rules */

    rule grammar:
        word forms functions rules
        END                 {{ return W }}

    rule word:
        T_WORD              {{ W.reset() }}
        word_inflection
        word_derivation

    rule forms:
        T_FORMS
        metasymbols
        forms_declaration*

    rule functions:
        T_FUNCTIONS function_declaration*

    rule rules:
        T_RULES
        rules_inflection
        rules_derivation

    rule word_inflection:
        T_INFLECTION        {{ W.setmclass(mc_inflection) }}
        prefix core infix suffix pattern

    rule word_derivation:
        T_DERIVATION        {{ W.setmclass(mc_derivation) }}
        prefix core infix suffix pattern

    rule metasymbols:
        T_META              {{ metas = [] }}
        string              {{ metas.append(string[1]) }}
        string              {{ metas.append(string[1]) }}
        string              {{ metas.append(string[1]) }}
        string              {{ metas.append(string[1]) }}
                            {{ W.setmetas(metas) }}

    rule forms_declaration:
        identifier
        forms_enumeration<<identifier[1]>>

    rule function_declaration:
        wf_declaration '='  {{ fvenum = set() }}
        fv_declaration      {{ fvenum.add(fv_declaration) }}
        (',' fv_declaration {{ fvenum.add(fv_declaration) }}
        )*                  {{ W.addfvenum(wf_declaration, fvenum) }}

    rule rules_inflection:
        T_INFLECTION        {{ W.setmclass(mc_inflection) }}
        ( rule_             {{ W.addrule(rule_) }} )*
        {{ pass }}

        # for some reason, with rule_* after T_DERIVATION,
        # it does not parse? Error message:
        # Error in rule rules_derivation:
        # * ( (  ) | ( T_DERIVATION rule_* ) )
        # * These tokens could be matched by more than one clause:
        # * T_DERIVATION
        # With dummy statement {{ pass }}, it does parse,
        # however (also true for other cases below)

    rule rules_derivation:
        # empty
        |
        T_DERIVATION        {{ W.setmclass(mc_derivation) }}
        ( rule_             {{ W.addrule(rule_) }} )*
        {{ pass }}

    rule prefix:
        # empty
        |
        T_PREFIX '=' mt_declaration<<prefix>>*
        {{ pass }}

    rule core:
        T_CORE '=' mt_declaration<<core>>

    rule infix:
        # empty
        |
        T_INFIX '=' mt_declaration<<infix>>*
        {{ pass }}

    rule suffix:
        # empty
        |
        T_SUFFIX '=' mt_declaration<<suffix>>*
        {{ pass }}

    rule pattern:
        # empty
        |
        T_PATTERN '=' mt_declaration<<pattern>>*
        {{ pass }}

    rule forms_enumeration<<mtid>>:
        explicit_enum<<mtid>>
        |
        implicit_enum<<mtid>>

    rule explicit_enum<<mtid>>:  {{ mvenum = set() }}
        '=' mv_declaration  {{ mvenum.add(mv_declaration) }}
        (',' mv_declaration {{ mvenum.add(mv_declaration) }} )*
                            {{ W.addmvenum(mtid, mvenum) }}

    rule implicit_enum<<mtid>>:
        '<' T_IDENTIFIER    {{ W.addmvenum(mtid, getattr(W, T_IDENTIFIER)) }}

    rule mv_declaration:
        T_IDENTIFIER        {{ return T_IDENTIFIER }}
        |
        string              {{ return string[1] }}

    # word function declaration
    rule wf_declaration:
        T_IDENTIFIER
        ':' string          {{ W.addwf(T_IDENTIFIER, string[1]) }}
                            {{ return T_IDENTIFIER }}

    # function value declaration
    rule fv_declaration:
        T_IDENTIFIER ':'
        string              {{ W.addfv(T_IDENTIFIER, string[1]) }}
                            {{ return T_IDENTIFIER }}

    rule mt_declaration<<p>>:
        T_IDENTIFIER ':' marker_set<<p>> string
        {{ W.addmt(T_IDENTIFIER, p, marker_set, string[1]) }}

    # with underscore because 'rule' is reserved word in Yapps
    rule rule_:
        label rule_definition   # TODO: test label jumping
        {{ return ('label', (label, rule_definition)) if label else rule_definition }}
        #{{ return ('rule', (label, rule_definition)) }}

    rule label:
        # empty
        |
        T_LABEL T_IDENTIFIER  {{ return T_IDENTIFIER }}

    rule rule_definition:
        simple_rule         {{ return ('simple_rule', simple_rule) }}
        |
        block               {{ return ('block', block) }}

    rule marker_set<<p>>:
        '{'                 {{ m = [None, None] }}
        [ string            {{ m[left] = string[1] }}
          [ ',' string      {{ m[right] = string[1] }} ] ] '}'
        {{ if (m[right] is None and p == prefix): m.reverse() }}
                            {{ return m }}

    rule simple_rule:
        expression
        T_ACTION_OPERATOR   {{ actions = [] }}
        action              {{ actions.append(action) }}
        ( ',' action        {{ actions.append(action) }} )*
                            {{ return (expression, actions) }}

    rule block:
        shared_rule         {{ rules = [] }}
        ( rule_             {{ rules.append(rule_) }} )+
        T_END               {{ return (shared_rule, rules) }}

    rule shared_rule:
        T_SHARED '{' expression shared_actions '}'
                            {{ return (expression, shared_actions) }}

    rule expression:        {{ e = [] }}
        term                {{ e.append(term) }}
        ( T_OR term         {{ e.append(term) }} )*
        {{ return e[0] if len(e) == 1 else ('or', tuple(e)) }}

    rule shared_actions:
        # empty
        |
        T_ACTION_OPERATOR   {{ a = [] }}
        action              {{ a.append(action) }}
        ( ',' action        {{ a.append(action) }} )*
                            {{ return a }}

        #{{ pass }}
        # for some reason, when adding an 'empty'
        # choice here, it does not parse. Error message:
        # Error in rule shared_actions:
        #  * ( (  ) | ( T_ACTION_OPERATOR action ) )
        #  * These tokens could be matched by more than one clause:
        #  * T_ACTION_OPERATOR
        # With dummy statement {{ pass }}, it does parse,
        # however. Other solution is to make 'shared_actions'
        # in 'shared_rule' optional with square brackets

    rule action:
        attribution         {{ return attribution }}
        |
        shift               {{ return shift }}

    rule attribution:
        assignment          {{ return ('assignment', assignment) }}
        |
        exclusion           {{ return ('exclusion', exclusion) }}
        |
        inclusion           {{ return ('inclusion', inclusion) }}

    rule shift:
        jump                {{ return ('jump', jump) }}
        |
        T_ACCEPT            {{ return ('accept', T_ACCEPT) }}
        |
        T_REJECT            {{ return ('reject', T_REJECT ) }}

    rule assignment:
        T_IDENTIFIER        {{ f = T_IDENTIFIER }} # function identifier
        '=' T_IDENTIFIER    {{ return (f, T_IDENTIFIER) }}

    rule jump:
        T_GOTO T_IDENTIFIER {{ return T_IDENTIFIER }}

    rule exclusion:
        '-' T_IDENTIFIER    {{ return T_IDENTIFIER }}

    rule inclusion:
        '\+' T_IDENTIFIER   {{ return T_IDENTIFIER }}

    rule term:              {{ t = [] }}
        factor              {{ t.append(factor) }}
        ( T_AND factor      {{ t.append(factor) }} )*
        {{ return t[0] if len(t) == 1 else ('and', tuple(t)) }}

    rule factor:
        simple_factor       {{ return simple_factor }}
        |
        negated_factor      {{ return negated_factor }}
        |
        grouped_factor      {{ return grouped_factor }}

    rule simple_factor:
        comparison          {{ return comparison }}
        |
        existence           {{ return existence }}

    rule negated_factor:
        T_NOT factor        {{ return ('not', factor) }}

    rule grouped_factor:
        '\\(' expression '\\)'
                            {{ return expression }}

    rule comparison:
        T_IDENTIFIER relational_operator value
                            {{ c = (T_IDENTIFIER, value, relational_operator) }}
                            {{ return ('cmp', c) }}
    rule existence:
        T_EXIST '\\(' T_IDENTIFIER '\\)'
                            {{ return ('exist', T_IDENTIFIER) }}

    rule relational_operator:
        T_EQUALITY          {{ return True }}
        |
        T_INEQUALITY        {{ return False }}

    rule value:
        single_value        {{ return set([single_value]) }}
        |
        value_set           {{ return value_set }}

    rule single_value:
        identifier          {{ return identifier[1]  }}
        |
        string              {{ return string[1] }}

    rule value_set:
        '{'                 {{ vset = set() }}
        single_value        {{ vset.add(single_value) }}
        ( ',' single_value  {{ vset.add(single_value) }} )*
        '}'                 {{ return vset }}


    rule string:
        T_STRING            {{ return ('str', T_STRING[1:-1]) }}

    rule identifier:
        T_IDENTIFIER        {{ return ('ident', T_IDENTIFIER) }}

%%

# some helper functions
# these are to check the grammar
# there should be more of those
# but since we only use grammars that are already checked
# we actually don't need any tests

# def check_markers(m, p):
#     if p == prefix:
#         if not m[left]:
#             raise Exception('Prefix: needs at least one marker')
#         elif not m[right]:
#             m = [None, m[left]]
#     elif p == core:
#         if m[left]:
#             raise Exception('Core: marker not allowed')
#     elif p == infix:
#         if not m[right]:
#             raise Exception('Infix: needs two markers')
#     elif p == suffix or p == pattern:
#         if not m[left]:
#             raise Exception('{}: needs at least one marker'.format(
#                 ['Suffix','Pattern'][p-3]))
#     return tuple(m)

# import wrdgrm
# W = wrdgrm.wrdgrm()
W = word_grammar()

# give distinctive values to some useful keywords
mc_inflection, mc_derivation = range(2)
prefix, core, infix, suffix, pattern = range(5)
left, right = range(2)


# with open('tstwgr','r') as f:
#     gr=f.read()
# wgr = parse('grammar', gr)

if __name__ == '__main__':
    from sys import argv, stdin
    if len(argv) >= 2:
        if len(argv) >= 3:
            f = open(argv[2],'r')
        else:
            f = stdin
        print(parse(argv[1], f.read()))
    else: print ('Args:  <rule> [<filename>]', file=sys.stderr)
