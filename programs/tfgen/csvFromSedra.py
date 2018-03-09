import sys
import os
import collections

# import modified version in this directory
# not the one next to sedra.py !

import constants  # noqa: F401

sys.path.append('../parsing')

import sedra  # noqa: E402

REPO = '~/github/etcbc/linksyr'
DEST = 'SEDRA'
CSV_BASE = os.path.expanduser(f'{REPO}/data/csv/{DEST}')

db = sedra.SedraIII()
'''
print(db.__dict__.keys())

print('ROOTS')
print(len(db.roots))
print(db.roots[10].__dict__)

print('LEXEMES')
print(len(db.lexemes))
print(db.lexemes[10].__dict__)

print('ENGLISH')
print(len(db.english))
print(db.english[10].__dict__)

print('ETYMOLOGY')
print(len(db.etymology))
print(db.etymology[10].__dict__)
'''

# print(db.english[14].__dict__)

dataTypes = collections.OrderedDict(
    words=dict(
        nodeType='word',
        linkType=('lexemes', 'lex_addr'),
        hasFeats=True,
        main=[
            ('cons', 'cons_str'),
            ('voc', 'voc_str'),
        ],
        skipFeats={
            'RESERVED',
        },
    ),
    lexemes=dict(
        nodeType='lexeme',
        linkType=('roots', 'root_addr'),
        hasFeats=True,
        main=[('lexeme', 'lex_str')],
        skipFeats=set(),
    ),
    english=dict(
        nodeType='english',
        linkType=('lexemes', 'lex_addr'),
        hasFeats=False,
        main=[
            ('meaning', 'meaning'),
            ('before', 'before'),
            ('after', 'after'),
            ('comment', 'comment'),
            ('ignore', 'ignore'),
        ],
        skipFeats={
            'comment_position',
            'comment_font',
            'string_before_font',
            'string_after_font',
            'form',
            'RESERVED',
        },
    ),
    etymology=dict(
        nodeType='etymology',
        linkType=('lexemes', 'lex_addr'),
        hasFeats=False,
        main=[],
        skipFeats=set(),
    ),
    roots=dict(
        nodeType='root',
        linkType=None,
        hasFeats=False,
        main=[('root', 'rt_str')],
        skipFeats={
            'RESERVED',
        },
    ),
)


def makeCsv():
    os.makedirs(CSV_BASE, exist_ok=True)

    for (d, (dataType, dataConfig)) in enumerate(dataTypes.items()):
        nodeType = dataConfig['nodeType']
        linkType = dataConfig['linkType']
        hasFeats = dataConfig['hasFeats']
        skipFeats = dataConfig['skipFeats']
        mainFeatures = dataConfig['main']
        data = getattr(db, dataType)
        print(f'{dataType:<10}: items 0 .. {len(data) -1:>5}')
        fields = ['id']
        with open(f'{CSV_BASE}/{nodeType}.csv', 'w') as fh:
            for (i, item) in enumerate(data):
                sys.stderr.write(f'{"":<12} item      {i:>5}\r')
                values = [i]
                if linkType:
                    (linkDataType, linkField) = linkType
                    linkNodeType = dataTypes[linkDataType]['nodeType']
                    if i == 0:
                        fields.append(f'{linkNodeType}Id')
                    link = getattr(item, linkField)
                    num = link[1] if link else ''
                    values.append(num)

                for (k, f) in mainFeatures:
                    if k not in skipFeats:
                        if i == 0:
                            fields.append(k)
                        values.append(getattr(item, f))
                for (k, v) in item.attributes._asdict().items():
                    if k not in skipFeats:
                        if i == 0:
                            fields.append(k)
                        values.append(v)
                if hasFeats:
                    for (k, v) in item.features._asdict().items():
                        if k not in skipFeats:
                            if i == 0:
                                fields.append(k)
                            values.append(v)
                if i == 0:
                    fieldsFmt = ('{}\t' * (len(fields) - 1)) + '{}\n'
                    fh.write(fieldsFmt.format(*fields))
                fh.write(fieldsFmt.format(*values))
        print(f'{"":<12} item      {i:>5}')

    return


makeCsv()
