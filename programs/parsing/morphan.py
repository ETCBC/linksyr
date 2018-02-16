
# coding: utf-8

# In[1]:


# import the database
# import syrnt
# nt=syrnt.SyrNT()


# In[2]:


# pattern functions
import difflib

def get_pattern(stem, lexeme):
    # TODO check if this method can be improved, e.g. by looking for patterns
    # matching as many forms as possible, instead of simplest pattern?
    # especially infixed verb forms
    '''Create pattern strings using difflib.ndiff'''
    pattern = ''
    for e in difflib.ndiff(stem, lexeme):
        if e[0] == ' ':
            pattern += ' '
        else:
            pattern += e[0]+e[2]
    return pattern

def check_pattern_length(p):
    '''Returns the length of the expected string for pattern p'''
    length=len(p)
    skip=False
    for c in p:
        if skip:
            skip=False
            continue
        if c == '+':
            length -= 2
            skip=True
        elif c == '-':
            length -= 1
            skip=True
    return length

def test_pattern(s, p):
    '''Test if string conforms to pattern, returns transformed string or False'''
    # first check the length of the expected string
    if len(s) != check_pattern_length(p):
        return False
    # now set initial values
    result=''
    poss=0
    posp=0
    # and loop over string s and pattern p strings
    while posp < len(p):
        if p[posp] == ' ': # for space in pattern, copy character from s
            result += s[poss]
            poss += 1
            posp += 1
        elif p[posp] == '-': # for minus in pattern:
            posp += 1        # move pattern pointer forward...
            if s[poss] == p[posp]: # ... and if s has the pattern character,
                poss += 1          # delete it by not adding to result
                posp += 1          # and moving pointers forward
            else:                  # if s does not have the character,
                return False       # the string does not conform to pattern
        elif p[posp] == '+': # for plus in pattern:
            posp += 1        # move pattern pointer forward...
            result += p[posp]      # ... and add pattern character to result
            posp += 1              # and move pattern character again
        else:
            raise Exception # should not happen
    return result


# In[3]:


# function to get tag
def get_tag(w):
#     prefix = (w.prefix != '')
#     suffix = (w.suffix != '')
    a = w.annotation
    # template for assigning values: px,sx,ps,c,a,s,p,n,g = get_tag(w) # ps = part of speech = grammatical_category
#     return (prefix, suffix, a.grammatical_category, a.verbal_conjugation, a.aspect, a.state, a.person, a.number, a.gender)
    return (a.grammatical_category, a.verbal_conjugation, a.aspect, a.state, a.person, a.number, a.gender)


# In[4]:


# create dicts with lookup tables

# number_lexemes = dict()   # total lexeme count in corpus, for probability calculation
# number_tags = dict()      # total tag count in corpus, for probability calculation
# lexemes_per_tag = dict()  # to check if a lexeme occurs with a given tag
# tags_per_pattern = dict() # to check if a tag occurs with a given pattern
# patterns_per_length = dict() # to look up patterns faster by looking only at the length of the stem
# number_patterntag = dict()
#
# for w in nt:
#     tag = get_tag(w)
#     pattern = get_pattern(w.stem, w.lexeme)
#     lexeme = w.lexeme
#     length = len(w.stem)
#
#     if lexeme not in number_lexemes:
#         number_lexemes[lexeme] = 0
#     number_lexemes[lexeme] += 1
#
#     if tag not in number_tags:
#         number_tags[tag] = 0
#     number_tags[tag] += 1
#
#     if tag not in lexemes_per_tag:
#         lexemes_per_tag[tag] = set()
#     lexemes_per_tag[tag].add(lexeme)
#
#     if pattern not in tags_per_pattern:
#         tags_per_pattern[pattern] = set()
#     tags_per_pattern[pattern].add(tag)
#
#     if length not in patterns_per_length:
#         patterns_per_length[length] = set()
#     patterns_per_length[length].add(pattern)
#
#     if (pattern, tag) not in number_patterntag:
#         number_patterntag[(pattern, tag)] = 0
#     number_patterntag[(pattern, tag)] += 1


# In[5]:


# prefixes = set(w.prefix for w in nt)
# suffixes = set(w.suffix for w in nt)
prefixes = {'', 'D', 'DL', 'DB', 'DD', 'B', 'WLD', 'DLD', 'WBD', 'WB', 'L',
            'W', 'WD', 'BD', 'WDB', 'LDL', 'WL', 'LD', 'WDL'}
suffixes = {'', 'JHJ', 'WNNJ', 'WNH', 'J', 'KJ', 'WNKJ', 'JWHJ', 'WH', 'HTJ',
            'WNJHJ', 'W', 'HWN', 'KJN', 'WHJN', 'HJN', 'WNJ', 'WKWN', 'WHWN',
            'NN', 'WHJ', 'N>', 'JN', 'WNKWN', 'HJKWN', 'T', 'JHWN', 'TWN',
            'NK', 'JH', 'HJK', 'JNJ', 'HJH', 'JKWN', 'JHJN', 'WK', 'JKJ',
            'NJHJ', 'WNN', 'K', 'H', 'KWN', 'JKJN', 'WN', 'JK', 'HWHJ', 'NJ',
            'WKJ', 'WNK', 'N', 'HJ'}

# In[6]:


# len(tags_per_pattern)


# In[7]:


# helper functions for analysis
def check_affixes(word):
    for suffix in suffixes:
        if word.endswith(suffix):
            for prefix in prefixes:
                if word.startswith(prefix) and len(word) > len(prefix+suffix):
                    stem = word[len(prefix):len(word)-len(suffix)]
                    yield (prefix, stem, suffix)

# totalnumberofwordsincorpus = len(nt) # 109640
#
# # calculate the probabilities for each tag
# def getprb(lexeme, tag, pattern):
#     # is this indeed the right way to calculate the probability
#     # of the combination of tag and lexeme?
#     # TODO maybe it is better to check for the combination
#     # of the pattern and the tag?
#     lxprb = number_lexemes[lexeme]/totalnumberofwordsincorpus
# #     tgprb = number_tags[tag]/totalnumberofwordsincorpus
#     tgprb = number_patterntag[(pattern,tag)]/totalnumberofwordsincorpus
#     return lxprb*tgprb

def normalize(probs):
    if probs:
        prob_factor = 1 / sum(probs)
        return [prob_factor * p for p in probs]
    else:
        return probs

def normalized_analyses(analyses):
    normalized = normalize([a[1] for a in analyses])
    return [(a,n) for (a, p), n in zip(analyses, normalized)]

def best_analysis(analyses):
    best_p = 0
    result = None
    for a, p in analyses:
        if p > best_p:
            best_p = p
            result = a
    return result

# # here is the crucial function
# def analyze(word):
#     analyses = []
#     for prefix, stem, suffix in check_affixes(word):
#         if len(stem) in patterns_per_length:
#             for pattern in patterns_per_length[len(stem)]:
#                 lexeme = test_pattern(stem, pattern)
#                 if lexeme:
#                     for tag in tags_per_pattern[pattern]:
#                         if lexeme in lexemes_per_tag[tag]:
#                             analyses.append(((prefix, stem, suffix, lexeme, tag), getprb(lexeme, tag, pattern)))
#
# #     probabilities = normalize([getprb(lexeme, tag, pattern) for lexeme, tag, pattern in analyses])
# #     return sorted(zip(analyses, probabilities), key=lambda x: x[1], reverse=True)
#     return normalized_analyses(analyses)

# word = nt[1]
# best_analysis(analyze(word.cons_str)), get_tag(word)


# # In[14]:
#
#
# lexemes_found = 0
# tags_found = 0
# tandlfound = 0
#
# good_segmentation = 0
# good_lexemes = 0
# good_seglex = 0
# good_tags = 0
# good_seglextags = 0
# good_pos = 0
# good_poslex = 0
#
# for i,w in enumerate(nt):
#     tag = get_tag(w)
#     pattern = get_pattern(w.stem, w.lexeme)
#     lexeme = w.lexeme
#     postag = w.annotation.grammatical_category
#
#     a = best_analysis(analyze(w.cons_str))
#
#     if (a[:3] == (w.prefix, w.stem, w.suffix)):
#         good_segmentation += 1
#     if a[3] == lexeme:
#         good_lexemes += 1
#     if (a[:3] == (w.prefix, w.stem, w.suffix)) and a[3] == lexeme:
#         good_seglex += 1
#     if a[4] == tag:
#         good_tags += 1
#     if (a[:3] == (w.prefix, w.stem, w.suffix)) and a[3] == lexeme and a[4] == tag:
#         good_seglextags += 1
#     if a[4][0] == postag:
#         good_pos += 1
#     if a[4][0] == postag and a[3] == lexeme:
#         good_poslex += 1
#     print(f'word {i+1} of {len(nt)} ({(((i+1)/len(nt))*100):.2f}%)', end='\r')
# print('\n')
#
# print('Lexemes recognized:       {:.2f} %'.format((100*(good_lexemes/len(nt)))))
# print('PartofSpeech recognized:  {:.2f} %'.format((100*(good_pos/len(nt)))))
# print('PoS and lexeme recognized:{:.2f} %'.format((100*(good_poslex/len(nt)))))
# print('Segmentation recognized:  {:.2f} %'.format((100*(good_segmentation/len(nt)))))
# print('Lexemes and segmentation: {:.2f} %'.format((100*(good_seglex/len(nt)))))
# print('Tags recognized:          {:.2f} %'.format((100*(good_tags/len(nt)))))
# print('All recognized:           {:.2f} %'.format((100*(good_seglextags/len(nt)))))


class MorphAn:

    def __init__(self):
        self._trained = False

    def train(self, train_corpus):
        self.corpus_length = len(train_corpus)
        self.number_lexemes = dict()   # total lexeme count in corpus, for probability calculation
        self.number_tags = dict()      # total tag count in corpus, for probability calculation
        self.lexemes_per_tag = dict()  # to check if a lexeme occurs with a given tag
        self.tags_per_pattern = dict() # to check if a tag occurs with a given pattern
        self.patterns_per_length = dict() # to look up patterns faster by looking only at the length of the stem
        self.number_patterntag = dict()

        for w in train_corpus:
            tag = get_tag(w)
            pattern = get_pattern(w.stem, w.lexeme)
            lexeme = w.lexeme
            length = len(w.stem)

            if lexeme not in self.number_lexemes:
                self.number_lexemes[lexeme] = 0
            self.number_lexemes[lexeme] += 1

            if tag not in self.number_tags:
                self.number_tags[tag] = 0
            self.number_tags[tag] += 1

            if tag not in self.lexemes_per_tag:
                self.lexemes_per_tag[tag] = set()
            self.lexemes_per_tag[tag].add(lexeme)

            if pattern not in self.tags_per_pattern:
                self.tags_per_pattern[pattern] = set()
            self.tags_per_pattern[pattern].add(tag)

            if length not in self.patterns_per_length:
                self.patterns_per_length[length] = set()
            self.patterns_per_length[length].add(pattern)

            if (pattern, tag) not in self.number_patterntag:
                self.number_patterntag[(pattern, tag)] = 0
            self.number_patterntag[(pattern, tag)] += 1

        self._trained = True

    # here is the crucial function
    def analyze(self, word_string):
        analyses = []
        for prefix, stem, suffix in check_affixes(word_string):
            if len(stem) in self.patterns_per_length:
                for pattern in self.patterns_per_length[len(stem)]:
                    lexeme = test_pattern(stem, pattern)
                    if lexeme:
                        for tag in self.tags_per_pattern[pattern]:
                            if lexeme in self.lexemes_per_tag[tag]:
                                analyses.append(
                                    ( (prefix, stem, suffix, lexeme, tag),
                                      self.getprb(lexeme, tag, pattern) )
                                )

        # probabilities = normalize([getprb(lexeme, tag, pattern) for lexeme, tag, pattern in analyses])
        # return sorted(zip(analyses, probabilities), key=lambda x: x[1], reverse=True)
        return normalized_analyses(analyses)

    # calculate the probabilities for each tag
    def getprb(self, lexeme, tag, pattern):
        # is this indeed the right way to calculate the probability
        # of the combination of tag and lexeme?
        # TODO maybe it is better to check for the combination
        # of the pattern and the tag?
        lxprb = self.number_lexemes[lexeme]/self.corpus_length
        # tgprb = number_tags[tag]/totalnumberofwordsincorpus
        tgprb = self.number_patterntag[(pattern,tag)]/self.corpus_length
        return lxprb*tgprb


    def test(self, test_corpus):
        if not self._trained:
            return False

        # In[14]:

        c_length = len(test_corpus)

        # lexemes_found = 0
        # tags_found = 0
        # tandlfound = 0

        good_lexemes = 0
        good_pos = 0
        good_poslex = 0
        good_segmentation = 0
        good_seglex = 0
        good_tags = 0
        good_seglextags = 0

        for i,w in enumerate(test_corpus):
            tag = get_tag(w)
            pattern = get_pattern(w.stem, w.lexeme)
            lexeme = w.lexeme
            postag = w.annotation.grammatical_category

            a = best_analysis(self.analyze(w.cons_str))

            if a:
                if a[3] == lexeme:
                    good_lexemes += 1
                if a[4][0] == postag:
                    good_pos += 1
                if a[4][0] == postag and a[3] == lexeme:
                    good_poslex += 1
                if (a[:3] == (w.prefix, w.stem, w.suffix)):
                    good_segmentation += 1
                if (a[:3] == (w.prefix, w.stem, w.suffix)) and a[3] == lexeme:
                    good_seglex += 1
                if a[4] == tag:
                    good_tags += 1
                if (a[:3] == (w.prefix, w.stem, w.suffix)) and a[3] == lexeme and a[4] == tag:
                    good_seglextags += 1
            print(f'word {i+1} of {c_length} ({(((i+1)/c_length)*100):.2f}%)', end='\r')
        print('\n')
        return (good_lexemes, good_pos, good_poslex, good_segmentation, good_seglex, good_tags, good_seglextags)

        # print('Lexemes recognized:       {:.2f} %'.format((100*(good_lexemes/c_length))))
        # print('PartofSpeech recognized:  {:.2f} %'.format((100*(good_pos/c_length))))
        # print('PoS and lexeme recognized:{:.2f} %'.format((100*(good_poslex/c_length))))
        # print('Segmentation recognized:  {:.2f} %'.format((100*(good_segmentation/c_length))))
        # print('Lexemes and segmentation: {:.2f} %'.format((100*(good_seglex/c_length))))
        # print('Tags recognized:          {:.2f} %'.format((100*(good_tags/c_length))))
        # print('All recognized:           {:.2f} %'.format((100*(good_seglextags/c_length))))
