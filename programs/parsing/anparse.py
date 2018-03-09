# import modules
import os
from wrdgrm import WordGrammar

# set base directory for data projects
data_dir = os.path.abspath('../../data')

def conf_parser(conf_file):
    '''Very simple parser. Works only on very simple files'''
    # Does not work on files with multiple language conf definitions.
    # For a real example with multiple language conf definitions,
    # see /projects/calap/etc/at2ps.conf

    # example simple conf file:
    # # Language configuration file for Turgama
    #
    # lib=/projects/lib
    #
    # language "syriac" {
    #    dir=$lib/syriac
    #
    #    lexica { lexicon: syrlex }
    #
    #    alphabet:	$dir/alphabet
    #    lexicon:	syrlex
    #    psdef:	syrpsd
    #    word_grammar:	syrwgr
    # }

    import re

    definitions = {}
    values = {}

    with open(conf_file) as f:
        for line in f:
            line = line.strip()
            if '{' in line:
                line = line.split('{')[1]
            if '}' in line:
                line = line.split('}')[0]
            if '$' in line: # replace defined variables with regex
                line = re.sub('\$([A-Za-z][A-Za-z0-9_]*)',
                              lambda x: definitions[x.group(1)], line)
            if '=' in line:
                name, value = (e.strip() for e in line.split('=', 1))
                definitions[name] = value # .replace(*replace)
            if ':' in line:
                key, value = (e.strip() for e in line.split(':'))
                values[key] = value

    return values

def check_file(filename, default_dir=data_dir):
    # replace '/projects' directory with our own data directory
    replace = ('/projects/', '/home/')

    if filename[0] != '/':
        filename = os.path.join(default_dir, filename)

    for string in replace: # replace /projects and /home, except if the path actually exists on local machine
        if filename.startswith(string) and not os.path.isfile(filename):
            filename = os.path.join(data_dir, filename[len(string):])

    # if os.path.isfile(filename):
    return os.path.abspath(filename)
    # else:
        # return False #raise ValueError(f'File not found: {filename}')

def parse_args(*args, **kw):
    '''
    Resolves arguments into filenames of auxiliary files

    args: an_file, word_grammar_file, lexicon_file        |
          an_file [, [conf_file=]'at2ps.conf']
                  [, word_grammar = 'word_grammar_file']
                  [, lexicon = 'lexicon_file']         |
          an_file, WordGrammar

    Three positional arguments are assumed to be an_file, word_grammar_file
    and lexicon_file.
    Two positional arguments can be either an_file and conf_file, or an_file
    and WordGrammar. If the second argument is a WordGrammar object, no
    keyword arguments are accepted.
    Filenames are assumed to be either absolute, starting with
    a slash '/', or relative to the data directory, which is set
    in the module variable data_dir.
    '''

    # set default filename for configuration file
    conf_file = 'at2ps.conf'

    err_none = 'At least one argument \'an_file\' is required.'
    err_many = 'Too many arguments. One, two or three expected.'

    if len(args) == 0:
        raise ValueError(err_none)
    elif len(args) > 3:
        raise ValueError(err_many)

    # check an_file, and expand if necessary
    an_file = check_file(args[0], data_dir)

    # if second argument is a WordGrammar object, we are done
    if len(args) > 1 and type(args[1]) is WordGrammar:
        if len(args) > 2 or len(kw):
            raise ValueError(err_many)
        return an_file, args[1]

    # otherwise continue:
    # set project dir to containing directory
    # (to look for auxiliary files)
    project_dir = os.path.dirname(an_file)

    word_grammar_file = None
    lexicon_file = None

    # check if filenames are provided in keyword args
    if 'word_grammar' in kw:
        word_grammar_file = check_file(kw['word_grammar'], project_dir)
    if 'lexicon' in kw:
        lexicon_file = check_file(kw['lexicon'], project_dir)

    # if word_grammar_file and lexicon_file have been explicitly provided:
    if len(args) == 3:
        if len(kw): # both positional AND keyword args is too much
            raise ValueError(err_many)
        word_grammar_file = check_file(args[1], project_dir)
        lexicon_file = check_file(args[2], project_dir)

    # if not: look for at2ps.conf, either provided in args[1] or default
    elif len(args) == 1 or len(args) == 2:
        if len(args) == 2:
            conf_file = args[1]
        conf_file = check_file(conf_file, project_dir)
        project_dir = os.path.dirname(conf_file)        # update project dir in case conf_file is in another location
        conf_dict = conf_parser(conf_file)
        if word_grammar_file is None and 'word_grammar' in conf_dict:
            word_grammar_file = check_file(conf_dict['word_grammar'], project_dir)
        if lexicon_file is None and 'lexicon' in conf_dict:
             lexicon_file = check_file(conf_dict['lexicon'], project_dir)

    # attempt to return a WordGrammar object with the obtained filenames
    return(an_file, WordGrammar(word_grammar_file, lexicon_file))

def parse_anfile(*args, **kw):
    an_file, wg = parse_args(*args, **kw)
    with open(an_file) as f:
        for line in f:
            verse, s, a = line.split() # verse, surface form, analyzed form
            yield (verse, s, a, tuple(wg.analyze(e) for e in a.split('-')))

# e.g.:
# laws=parse_anfile('blc/Laws.an')
# next(laws)

def print_anfile(*args, **kw):
    for line in parse_anfile(*args, **kw):
        verse, surface, analysis, words = line
        yield '\t'.join((verse, surface, analysis))
        for word in words:
        # for word_element, (surface_form, morphemes, functions, lex) in word_elements:
            yield '    ' + word.word
            yield '\tmorphemes: ' + str(tuple((m.mt.ident, m.p) for m in word.morphemes))
            yield '\tfunctions: ' + str(word.functions)
            yield '\tlex      : ' + str(word.lex)

def dump_anfile(title, *args, **kw):
    for verse, surface, analysis, words in parse_anfile(*args, **kw):
        for word in words:
            yield(word.dmp_str(title, verse))
