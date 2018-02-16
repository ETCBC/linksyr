# TODO add comments

#====================================================================
# General New Testament constants
#====================================================================

NT_BOOKS = (
    ('Matt',   (25, 23, 17, 25, 48, 34, 29, 34, 38, 42, 30, 50, 58, 36,
                39, 28, 27, 35, 30, 34, 46, 46, 39, 51, 46, 75, 66, 20)),
    ('Mark',   (45, 28, 35, 41, 43, 56, 37, 38, 50, 52, 33, 44, 37, 72,
                47, 20)),
    ('Luke',   (80, 52, 38, 44, 39, 49, 50, 56, 62, 42, 54, 59, 35, 35,
                32, 31, 37, 43, 48, 47, 38, 71, 56, 53)),
    ('John',   (51, 25, 36, 54, 47, 71, 53, 59, 41, 42, 57, 50, 38, 31,
                27, 33, 26, 40, 42, 31, 25)),
    ('Acts',   (26, 47, 26, 37, 42, 15, 60, 40, 43, 48, 30, 25, 52, 28,
                41, 40, 34, 28, 41, 38, 40, 30, 35, 27, 27, 32, 44, 31)),
    ('Rom',    (32, 29, 31, 25, 21, 23, 25, 39, 33, 21, 36, 21, 14, 23,
                33, 27)),
    ('1Cor',   (31, 16, 23, 21, 13, 20, 40, 13, 27, 33, 34, 31, 13, 40,
                58, 24)),
    ('2Cor',   (24, 17, 18, 18, 21, 18, 16, 24, 15, 18, 33, 21, 14)),
    ('Gal',    (24, 21, 29, 31, 26, 18)),
    ('Eph',    (23, 22, 21, 32, 33, 24)),
    ('Phil',   (30, 30, 21, 23)),
    ('Col',    (29, 23, 25, 18)),
    ('1Thess', (10, 20, 13, 18, 28)),
    ('2Thess', (12, 17, 18)),
    ('1Tim',   (20, 15, 16, 16, 25, 21)),
    ('2Tim',   (18, 26, 17, 22)),
    ('Titus',  (16, 15, 15)),
    ('Phlm',   (25,)),
    ('Heb',    (14, 18, 19, 16, 14, 20, 28, 13, 28, 39, 40, 29, 25)),
    ('James',  (27, 26, 18, 17, 20)),
    ('1Peter', (25, 25, 22, 19, 14)),
    ('2Peter', (21, 22, 18)),
    ('1John',  (10, 29, 24, 21, 21)),
    ('2John',  (13,)),
    ('3John',  (15,)),
    ('Jude',   (25,)),
    ('Rev',    (20, 29, 22, 11, 14, 17, 17, 13, 21, 11, 19, 17, 18, 20,
                8, 21, 18, 24, 21, 15, 27, 20)))

#====================================================================
# SyrNT constants
#====================================================================
class SyrNT:

    # SyroMorph Data format
    #
    # See also morph.app.SyriacDatum.java,
    # edu.byu.nlp.ccash.syriacmorphtag.gwt.SyrTagValues and the data files themselves.
    #
    # e.g., CTBA|CTBA#CTBA#CTB###0#0#0#3#1#0#2#0#0#2#0#0#2#0#0#0#0#0 ...
    #
    # On the left of the bar is the full token. On the right of the bar are the
    # annotations for that token.  All of the tokens in a verse are on the same line
    # separated by a space.
    #
    # The annotations are as follows:
    ANNOTATIONS = (             # <index> <name>
        ('stem', None),         #  0 stem
        ('lexeme', None),       #  1 lexeme (baseform)
        ('root', None),         #  2 root
        ('prefix', None),       #  3 prefix
        ('suffix', None),       #  4 suffix
        ('seyame', None),       #  5 seyame
        ('verbal_conjugation',  #  6 verb conjugation
            ('n/a',                 #  0 n/a
             'peal',                #  1 peal
             'ethpeal',             #  2 ethpeal
             'pael',                #  3 pael
             'ethpael',             #  4 ethpael
             'aphel',               #  5 aphel
             'ettaphal',            #  6 ettaphal
             'shaphel',             #  7 shaphel
             'eshtaphal',           #  8 eshtaphal
             'saphel',              #  9 saphel
             'estaphal',            # 10 estaphal
             'pauel',               # 11 pauel
             'ethpaual',            # 12 ethpaual
             'paiel',               # 13 paiel
             'ethpaial',            # 14 ethpaial
             'palpal',              # 15 palpal
             'ethpalpal',           # 16 ethpalpal
             'palpel',              # 17 palpel
             'ethpalpal2',          # 18 ethpalpal2
             'pamel',               # 19 pamel
             'ethpamel',            # 20 ethpamel
             'parel',               # 21 parel
             'ethparal',            # 22 ethparal
             'pali',                # 23 pali
             'ethpali',             # 24 ethpali
             'pahli',               # 25 pahli
             'ethpahli',            # 26 ethpahli
             'taphel',              # 27 taphel
             'ethaphal')            # 28 ethaphal
        ),
        ('aspect',              #  7 aspect
            ('n/a',                 # 0 n/a
             'perfect',             # 1 perfect
             'imperfect',           # 2 imperfect
             'imperative',          # 3 imperative
             'infinitive',          # 4 infinitive
             'participle')          # 5 participle
        ),
        ('state',               #  8 state
            ('n/a',                 # 0 n/a
             'absolute',            # 1 absolute
             'construct',           # 2 construct
             'emphatic')            # 3 emphatic
        ),
        ('number',              #  9 number
            ('n/a',                 # 0 n/a
             'singular',            # 1 singular
             'plural')              # 2 plural
        ),
        ('person',              # 10 person
            ('n/a',                 # 0 n/a
             'first',               # 1 first
             'second',              # 2 second
             'third')               # 3 third
        ),
        ('gender',              # 11 gender
            ('n/a',                 # 0 n/a
             'common',              # 1 common
             'masculine',           # 2 masculine
             'feminine')            # 3 feminine
        ),
        ('pronoun_type',        # 12 pronoun type
            ('n/a',                 # 0 n/a
             'personal',            # 1 personal
             'demonstrative',       # 2 demonstrative
             'interrogative')       # 3 interrogative
        ),
        ('demonstrative_category',
                                # 13 demonstrative category
            ('n/a',                 # 0 n/a
             'near',                # 1 near
             'far')                 # 2 far
        ),
        ('noun_type',           # 14 noun type
            ('n/a',                 # 0 n/a
             'propper',             # 1 propper
             'common')              # 2 common
        ),
        ('numeral_type',        # 15 numeral type
            ('n/a',                 # 0 n/a
             'cardinal',            # 1 cardinal
             'ordinal',             # 2 ordinal
             'cipher')              # 3 cipher
        ),
        ('participle_type',     # 16 participle type
            ('n/a',                 # 0 n/a
             'active',              # 1 active
             'passive')             # 2 passive
        ),
        ('grammatical_category',# 17 grammatical category
            ('verb',                # 0 verb
             'participle',          # 1 participle
             'noun',                # 2 noun
             'pronoun',             # 3 pronoun
             'numeral',             # 4 numeral
             'adjective',           # 5 adjective
             'particle',            # 6 particle
             'adverb',              # 7 adverb
             'idiom')               # 8 idiom
        ),
        ('suffix_contraction',  # 18 suffix contraction
            ('n/a',                 # 0 n/a
             'suffix',              # 1 suffix
             'contraction')         # 2 contraction
        ),
        ('suffix_gender',       # 19 suffix gender
            ('common OR n/a',       # 0 common OR n/a
             'masculine',           # 1 masculine
             'feminine')            # 2 feminine
        ),
        ('suffix_person',       # 20 suffix person
            ('n/a',                 # 0 n/a
             'first',               # 1 first
             'second',              # 2 second
             'third')               # 3 third
        ),
        ('suffix_number',       # 21 suffix number
            ('singular OR n/a',     # 0 singular OR n/a
             'plural')              # 1 plural
        ),
        ('feminine_he_dot', None),  # 22 feminine he dot
                                    # 0 does not have the feminine he dot
                                    # 1 has the feminine he dot
    )


#====================================================================
# SEDRA-III constants
#====================================================================
class SedraIII:

    # ROOTS.TXT
    ROOTS_ATTR = ((             # Attributes: 16-bit intiger as follows
        'SEYAME FLAG', 1, (     # 0  SEYAME FLAG:
            'NO SEYAME',        #     0 NO SEYAME
            'SEYAME'            #     1 SEYAME
        )), (
        'ROOT TYPE', 2, (       # 1-2 ROOT TYPE:
            'NORMAL',           #     00 NORMAL
            'PARETHESIED',      #     01 PARETHESIED
            'BRACKETED',        #     10 BRACKETED
            'HIGH FREQUENCY ROOT, e.g. propositons'
                                #     11 HIGH FREQUENCY ROOT, e.g. propositons
        )), (
        '<RESERVED>', 13, None  # 3-15 <RESERVED>
    ))
    # LEXEMES.TXT
    LEXEMES_ATTR = ((           # Attributes: 16-bit intiger as follows
        'SEYAME FLAG', 1, (     # 0 SEYAME FLAG:
            'NO SEYAME',        #     0 NO SEYAME
            'SEYAME'            #     1 SEYAME
        )), (
        'WORD TYPE', 1, (       # 1 WORD TYPE:
            'NORMAL',           #     0 NORMAL
            'PARENTHESISED'     #     1 PARENTHESISED
        )), (
        'GRAMMATICAL CATEGORY', 4, (
                                # 2-5 GRAMMATICAL CATEGORY:
            'VERB',             #     0000 VERB
            'PARTICIPLE ADJECTIVE',
                                #     0001 PARTICIPLE ADJECTIVE
            'DENOMINATIVE',     #     0010 DENOMINATIVE
            'SUBSTANTIVE',      #     0011 SUBSTANTIVE
            'NOUN',             #     0100 NOUN
            'PRONOUN',          #     0101 PRONOUN
            'PROPER_NOUN',      #     0110 PROPER_NOUN
            'NUMERAL',          #     0111 NUMERAL
            'ADJECTIVE',        #     1000 ADJECTIVE
            'PARTICLE',         #     1001 PARTICLE
            'IDIOM',            #     1010 IDIOM
            'ADVERB (ending with AiYT)',
                                #     1011 ADVERB (ending with AiYT)
            'ADJECTIVE OF PLACE',
                                #     1100 ADJECTIVE OF PLACE
            'ADVERB'            #     1101 ADVERB
        )), (
        'REST', 10, None        ##              /add -HV
        )
    )
    LEXEMES_FEAT = ((           # Morphological Type: 32-bit intiger as follows
        'First SUFFIX', 4, (    # 0-3 First SUFFIX:
            '<NONE>',           #     0000 <NONE>
            'ToA',              #     0001 ToA
            'YoA',              #     0010 YoA
            'NoA',              #     0011 NoA
            'oNoA',             #     0100 oNoA
            'iYNoA',            #     0101 iYNoA
            'uONoA',            #     0110 uONoA
            'ToNoA',            #     0111 ToNoA
            'TuONoA',           #     1000 TuONoA
            'uOSoA',            #     1001 uOSoA
            'oRoA',             #     1010 oRoA
            'QoNoA',            #     1011 QoNoA
            'i;N'               #     1100 i;N
        )), (
        'SECOND SUFFIX', 2, (   # 4-5 SECOND SUFFIX:
            '<NONE>',           #     00 <NONE>
            'oYoA',             #     01 oYoA
            'iYToA'             #     10 iYToA
        )), (
        'THIRD SUFFIX', 2, (    # 6-7 THIRD SUFFIX:
            '<NONE>',           #     00 <NONE>
            'uOToA',            #     01 uOToA
            'oAiYT'             #     10 oAiYT
        )), (
        'PREFIX', 2, (          # 8-9 PREFIX:
            '<NONE>',           #     00 <NONE>
            'M',                #     01 M
            'T',                #     10 T
            '?????????',        ##              /add -HV
        )), (
        'FIRST VOWEL', 3, (     # 10-12 FIRST VOWEL:
            '<NONE>',           #     000 <NONE>
            'a',                #     001 a
            'o',                #     010 o
            'e',                #     011 e
            'i',                #     100 i
            'u'                 #     101 u
        )), (
        'SECOND VOWEL', 3, (    # 13-15 SECOND VOWEL: as above
            '<NONE>',           ##    000 <NONE>
            'a',                ##    001 a
            'o',                ##    010 o
            'e',                ##    011 e
            'i',                ##    100 i
            'u'                 ##    101 u
        )), (
        'THIRD VOWEL', 3, (     # 16-18 THIRD VOWEL: as above
            '<NONE>',           ##    000 <NONE>
            'a',                ##    001 a
            'o',                ##    010 o
            'e',                ##    011 e
            'i',                ##    100 i
            'u'                 ##    101 u
        )), (
        'FOURTH VOWEL', 3, (    # 19-21 FOURTH VOWEL: as above
            '<NONE>',           ##    000 <NONE>
            'a',                ##    001 a
            'o',                ##    010 o
            'e',                ##    011 e
            'i',                ##    100 i
            'u'                 ##    101 u
        )), (
        'NUM_VOWELS', 3, None   # 22-24 Total no of vowels in lexeme: 0-7
        ), (
        'RADICAL TYPE', 3, (    # 25-27 RADICAL TYPE:
            '<NONE>',           #     000 <NONE>
            'BI',               #     001 BI
            'TRI',              #     010 TRI
            'FOUR_RADICAL',     #     011 FOUR_RADICAL
            'FIVE_RADICAL',     #     100 FIVE_RADICAL
            'SIX_RADICAL',      #     101 SIX_RADICAL
            'COMPOUND'          #     110 COMPOUND
        )), (
        'FORM', 4, (            # 28-31 FORM:
            '<NONE>',           #     0000 <NONE>
            'PEAL',             #     0001 PEAL
            'ETHPEAL',          #     0010 ETHPEAL
            'PAEL',             #     0011 PAEL
            'ETHPAEL',          #     0100 ETHPAEL
            'APHEL',            #     0101 APHEL
            'ETTAPHAL',         #     0110 ETTAPHAL
            'SHAPHEL',          #     0111 SHAPHEL
            'ESHTAPHAL',        #     1000 ESHTAPHAL
            'SAPHEL',           #     1001 SAPHEL
            'ESTAPHAL',         #     1010 ESTAPHAL
            'P',                #     1011 P
            'ETHP',             #     1100 ETHP
            'PALPEL',           #     1101 PALPEL
            'ETHPALPAL',        #     1110 ETHPALPAL
            '?????????',        ##              /add -HV
        ))
    )
    # WORDS.TXT
    WORDS_ATTR = ((             # Attributes: 16-bit intiger as follows
        'SEYAME FLAG', 1, (     # 0 SEYAME FLAG:
            'NO SEYAME',        #     0 NO SEYAME
            'SEYAME'            #     1 SEYAME
        )), (
        'ignore', 4, None       # 1-4 ignore
        ), (
        'ENCLITIC FLAG', 1, (   # 5 ENCLITIC FLAG:
            'NOT ENCLITIC',     #     0 NOT ENCLITIC
            'ENCLITIC'          #     1 ENCLITIC
        )), (
        'LEXEME FLAG', 1, (     # 6 LEXEME FLAG:
            'NO',               #     0 NO
            'YES, i.e. = word represents lexeme'
                                #     1 YES, i.e. = word represents lexeme
        )), (
        'REST', 9, None         ##              /add -HV
        )
    )
    WORDS_FEAT = ((             # Morphological Features: 32-bit intiger as follows
        '<RESERVED>', 2, None   # 0-1 <RESERVED>
        ), (
        'SUFFIX GENDER', 2, (   # 2-3 SUFFIX GENDER:
            'COMMON or <NONE>', #     00 COMMON or <NONE>
            'MASCULINE',        #     01 MASCULINE
            'SUFFEMININE'       #     10 SUFFEMININE
        )), (
        'SUFFIX PERSON', 2, (   # 4-5 SUFFIX PERSON:
            '<NONE>',           #     00 <NONE>
            'THIRD',            #     01 THIRD
            'SECOND',           #     10 SECOND
            'FIRST'             #     11 FIRST
        )), (
        'SUFFIX NUMBER', 1, (   # 6 SUFFIX NUMBER:
            'SINGULAR or <NONE>',
                                #     0 SINGULAR or <NONE>
            'PLURAL'            #     1 PLURAL
        )), (
        'SUFFIX/CONTRACTION', 2, (
                                # 7-8 SUFFIX/CONTRACTION:
            '<NONE>',           #     00 <NONE>
            'SUFFIX',           #     01 SUFFIX
            'CONTRACTION'       #     10 CONTRACTION
        )), (
        'PREFIX CODE', 6, None  # 9-14 PREFIX CODE: 0-63
        ), (
        'GENDER', 2, (          # 15-16 GENDER:
            '<NONE>',           #     00 <NONE>
            'COMMON',           #     01 COMMON
            'MASCULINE',        #     10 MASCULINE
            'FEMININE'          #     11 FEMININE
        )), (
        'PERSON', 2, (          # 17-18 PERSON:
            '<NONE>',           #     00 <NONE>
            'THIRD',            #     01 THIRD
            'SECOND',           #     10 SECOND
            'FIRST'             #     11 FIRST
        )), (
        'NUMBER', 2, (          # 19-20 NUMBER:
            '<NONE>',           #     00 <NONE>
            'SINGULAR',         #     01 SINGULAR
            'PLURAL'            #     10 PLURAL
        )), (
        'STATE', 2, (           # 21-22 STATE:
            '<NONE>',           #     00 <NONE>
            'ABSOLUTE',         #     01 ABSOLUTE
            'CONSTRUCT',        #     10 CONSTRUCT
            'EMPHATIC'          #     11 EMPHATIC
        )), (
        'TENSE', 3, (           # 23-25 TENSE:
            '<NONE>',           #     000 <NONE>
            'PERFECT',          #     001 PERFECT
            'IMPERFECT',        #     010 IMPERFECT
            'IMPERATIVE',       #     011 IMPERATIVE
            'INFINITIVE',       #     100 INFINITIVE
            'ACTIVE_PARTICIPLE',#     101 ACTIVE_PARTICIPLE
            'PASSIVE_PARTICIPLE',
                                #     110 PASSIVE_PARTICIPLE
            'PARTICIPLES'       #     111 PARTICIPLES
        )), (
        'FORM', 6, (            # 26-31 FORM:
            '<NONE>',           #     000000 <NONE>
            'PEAL',             #     000001 PEAL
            'ETHPEAL',          #     000010 ETHPEAL
            'PAEL',             #     000011 PAEL
            'ETHPAEL',          #     000100 ETHPAEL
            'APHEL',            #     000101 APHEL
            'ETTAPHAL',         #     000110 ETTAPHAL
            'SHAPHEL',          #     000111 SHAPHEL
            'ESHTAPHAL',        #     001000 ESHTAPHAL
            'SAPHEL',           #     001001 SAPHEL
            'ESTAPHAL',         #     001010 ESTAPHAL
            'PAUEL',            #     001011 PAUEL
            'ETHPAUAL',         #     001100 ETHPAUAL
            'PAIEL',            #     001101 PAIEL
            'ETHPAIAL',         #     001110 ETHPAIAL
            'PALPAL',           #     001111 PALPAL
            'ETHPALPAL',        #     010000 ETHPALPAL
            'PALPEL',           #     010001 PALPEL
            'ETHPALPAL',        #     010010 ETHPALPAL
            'PAMEL',            #     010011 PAMEL
            'ETHPAMAL',         #     010100 ETHPAMAL
            'PAREL',            #     010101 PAREL
            'ETHPARAL',         #     010110 ETHPARAL
            'PALI',             #     010111 PALI
            'ETHPALI',          #     011000 ETHPALI
            'PAHLI',            #     011001 PAHLI
            'ETHPAHLI',         #     011010 ETHPAHLI
            'TAPHEL',           #     011011 TAPHEL
            'ETHAPHAL'          #     011100 ETHAPHAL
        ))
    )
    # ENGLISH.TXT
    ENGLISH_ATTR = ((           # Attributes: 15-bit intiger as follows:
        '<RESERVED>', 1, None   # 0 <RESERVED>
        ), (
        'COMMENT POSITION', 1, (# 1 COMMENT POSITION:
            'COMMENT BEFORE MEANING',
                                #     0 COMMENT BEFORE MEANING
            'COMMENT AFTER MEANING'
                                #     1 COMMENT AFTER MEANING
        )), (
        'COMMENT FONT', 1, (    # 2 COMMENT FONT:
            'NORMAL',           #     0 NORMAL
            'ITALIC'            #     1 ITALIC
        )), (
        'STRING BEFORE FONT', 1, (
                                # 3 STRING BEFORE FONT: as above
            'NORMAL',           ##    0 NORMAL
            'ITALIC'            ##    1 ITALIC
        )), (
        'STRING AFTER FONT', 1, (
                                # 4 STRING AFTER FONT: as above
            'NORMAL',           ##    0 NORMAL
            'ITALIC'            ##    1 ITALIC
        )), (
        'VERB TYPE', 2, (       # 5-6 VERB TYPE:
            '<NONE>',           #     00 <NONE>
            'TRANSITIVE',       #     01 TRANSITIVE
            'INTRANSITIVE'      #     10 INTRANSITIVE
        )), (
        'NUMBER', 2, (          # 7-8 NUMBER: as above
            '<NONE>',           ##    00 <NONE>
            'SINGULAR',         ##    01 SINGULAR
            'PLURAL'            ##    10 PLURAL
        )), (
        'GENDER', 2, (          # 9-10 GENDER: as above
            '<NONE>',           ##    00 <NONE>
            'COMMON',           ##    01 COMMON
            'MASCULINE',        ##    10 MASCULINE
            'FEMININE'          ##    11 FEMININE
        )), (
        'FORM', 5, None         # 11-15 FORM: as above
                                ## TODO: what forms are these?
                                ## Below the attested values:
                                ## (5 bits; the sixth bit is always 0)
                                ## 000001  1
                                ## 000010  2
                                ## 000011  3
                                ## 000100  4
                                ## 000101  5
                                ## 000110  6
                                ## 000111  7
                                ## 001000  8
                                ## 001001  9
                                ## 001101 13
                                ## 001110 14
                                ## 010000 16
                                ## 010010 18
                                ## 010110 22
        )
    )
    # ETIMOLGY.TXT
    ETYMOLOGY_ATTR = ((         # Attributes: 16-bit intigier as follows:
        'LANGUAGE', 4, (        # 0-3 LANGUAGE:
            'SYRIAC',           #     0000  SYRIAC
            'AKKADIAN',         #     0001  AKKADIAN
            'ARAMAIC',          #     0010  ARAMAIC
            'ARABIC',           #     0011  ARABIC
            'ARMENIAN',         #     0100  ARMENIAN
            'GREEK',            #     0101  GREEK
            'HEBREW',           #     0110  HEBREW
            'LATIN',            #     0111  LATIN
            'PERSIAN',          #     1000  PERSIAN
            'SANSKRIT'          #     1001  SANSKRIT
        )), (
        'TYPE', 1, (            # 4 TYPE:
            'NORMAL',           #     0 NORMAL
            'PARENTHESIED'      #     1 PARENTHESIED
        )), (
        'REST', 11, None        ##              /add -HV
        )
    )
