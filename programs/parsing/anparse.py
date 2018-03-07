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

    keys = ('alphabet', 'lexicon', 'psdef', 'word_grammar')

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

    if all(e in values for e in keys):
        return tuple(values[key] for key in keys)
    else:
        raise ValueError(f'Invalid configuration file: {conf_file}')

def check_file(filename, default_dir):
    if filename[0] != '/':
        filename = os.path.join(default_dir, filename)
    if not os.path.isfile(filename):
        raise ValueError(f'File not found: {filename}')
    return os.path.abspath(filename)

def parse_args(an_file, *args):
    '''
    Resolves arguments into filenames of auxiliary files

    args: an_file [, alphabet, lexicon, psdef, word_grammar]   |
          an_file [, conf_file='at2ps.conf']

    Filenames are assumed to be either absolute, starting with
    a slash '/', or relative to the data directory, which is set
    in the module variable data_dir.
    '''

    # set default filename for configuration file
    conf_file = 'at2ps.conf'
    # replace '/projects' directory with our own data directory
    replace = '/projects'

    if len(args) not in (0, 1, 4):
        raise ValueError(f'Not enough arguments. One, two or five expected, {len(args)+1} given.')

    # check an_file, and expand if necessary
    an_file = check_file(an_file, data_dir)
    # set project dir to containing directory
    # (to look for auxiliary files)
    project_dir = os.path.dirname(an_file)

    if len(args) == 4: # if separate auxiliary files provided:
        aux_files = args
    else:
        # if conf_file provided, replace default
        if len(args) == 1 and type(args[0]) is str:
            conf_file = args[0]
        # expand path if necessary and check if file exists
        conf_file = check_file(conf_file, project_dir)
        # change project dir to the containing directory
        # of the conf_file, if that is different from
        # that of the an_file
        project_dir = os.path.dirname(conf_file)
        # parse conf_file to get auxiliary filenames
        aux_files = conf_parser(conf_file)

    # replace '/projects' directory with our own data directory
    aux_files = (e.replace(replace, data_dir, 1) if e.startswith(replace) else e for e in aux_files)
    # prefix filenames without path with project directory
    # aux_files = (os.path.join(project_dir, e) if not '/' in e else e for e in aux_files)
    aux_files = (check_file(aux_file, project_dir) for aux_file in aux_files)

    return (an_file, *aux_files)

# e.g.:
# parse_args('/home/gdwarf/github/etcbc/linksyr/data/blc/Laws.an')
# ('/home/gdwarf/github/etcbc/linksyr/data/blc/Laws.an',
#  '/home/gdwarf/github/etcbc/linksyr/data/lib/syriac/alphabet',
#  '/home/gdwarf/github/etcbc/linksyr/data/blc/syrlex',
#  '/home/gdwarf/github/etcbc/linksyr/data/blc/syrpsd',
#  '/home/gdwarf/github/etcbc/linksyr/data/blc/syrwgr')

def parse_anfile(an_file, *args):
    an_file, alphabet, lexicon, psdef, word_grammar = parse_args(an_file, *args)
    wg = WordGrammar(word_grammar, lexicon) #, alphabet)
    with open(an_file) as f:
        for line in f:
            verse, s, a = line.split() # verse, surface form, analyzed form
            yield (verse, s, a, tuple(wg.analyze(e) for e in a.split('-')))

# e.g.:
# laws=parse_anfile('/home/gdwarf/github/etcbc/linksyr/data/blc/Laws.an')
# next(laws)

def print_anfile(an_file, *args):
    for line in parse_anfile(an_file, *args):
        verse, surface, analysis, words = line
        yield '\t'.join((verse, surface, analysis))
        for word in words:
        # for word_element, (surface_form, morphemes, functions, lex) in word_elements:
            yield '    ' + word.word
            yield '\tmorphemes: ' + str(word.morphemes)
            yield '\tfunctions: ' + str(word.functions)
            yield '\tlex      : ' + str(word.lex)

def dump_anfile(project_name, an_file, *args):
    for line in parse_anfile(an_file, *args):
        verse, surface, analysis, words = line
        heading = f'{project_name} {verse}'
        for word in words:
            # surface_form = ''.join((m[1][1] for m in morphemes if m[0] != 'vpm'))
            # lexeme = dict(morphemes)['lex'][0]
            affixes = [m for m in word.morphemes if m[0] != 'lex'] # TODO affix may not be the right term?
            affix_str = ('-' if not affixes else
                ','.join((f'{e[0]}="{e[1][0]}"' if e[0] != 'vpm' else f'{e[0]}={e[1][0]}' for e in affixes)))
            func_str = ','.join(('+'+fn if fv is None else fn+'='+fv for fn, fv in word.functions if fv != False))

            yield '\t'.join((heading, word.word, word.surface_form, word.lexeme, affix_str, func_str))
