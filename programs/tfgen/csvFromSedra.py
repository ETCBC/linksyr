import sys
import os
import collections
from shutil import rmtree

# import modified version in this directory
# not the one next to sedra.py !

import constants  # noqa: F401

sys.path.append('../parsing')

import sedra  # noqa: E402

REPO = '~/github/etcbc/linksyr'
DEST = 'sedra'
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
        linkType=('roots', 'root_addr'),
        hasFeats=True,
        main=[('lexeme', 'lex_str')],
        skipFeats=set(),
    ),
    english=dict(
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
        linkType=('lexemes', 'lex_addr'),
        hasFeats=False,
        main=[],
        skipFeats=set(),
    ),
    roots=dict(
        linkType=None,
        hasFeats=False,
        main=[('root', 'rt_str')],
        skipFeats={
            'RESERVED',
        },
    ),
)


def makeCsv():
    if os.path.exists(CSV_BASE):
        rmtree(CSV_BASE)
    os.makedirs(CSV_BASE)

    tables = {}
    fields = {}

    def collect():
        for (d, (dataType, dataConfig)) in enumerate(dataTypes.items()):
            tables[dataType] = []
            lines = tables[dataType]
            fields[dataType] = []
            theseFields = fields[dataType]

            linkType = dataConfig['linkType']
            hasFeats = dataConfig['hasFeats']
            skipFeats = dataConfig['skipFeats']
            mainFeatures = dataConfig['main']
            data = getattr(db, dataType)
            print(f'{dataType:<10}: items 0 .. {len(data) -1:>5}')
            for (i, item) in enumerate(data):
                sys.stderr.write(f'{"":<12} item      {i:>5}\r')
                values = []
                if linkType:
                    (linkDataType, linkField) = linkType
                    if i == 0:
                        theseFields.append(f'{linkDataType}Id')
                    link = getattr(item, linkField)
                    num = link[1] if link else ''
                    values.append(num)

                for (k, f) in mainFeatures:
                    if k not in skipFeats:
                        if i == 0:
                            theseFields.append(k)
                        values.append(getattr(item, f))
                for (k, v) in item.attributes._asdict().items():
                    if k not in skipFeats:
                        if i == 0:
                            theseFields.append(k)
                        values.append(v)
                if hasFeats:
                    for (k, v) in item.features._asdict().items():
                        if k not in skipFeats:
                            if i == 0:
                                theseFields.append(k)
                            values.append(v)
                lines.append(values)
            print(f'{"":<12} item      {i:>5}')

    def combineForth():
        for dataType in ('roots',):
            fieldMap = dict(
                root='root',
                seyame='root_seyame',
                root_type='root_type',
            )
            fields['lexemes'].pop(0)
            fields['lexemes'].extend(
                (f'{fieldMap[f]}' for f in fields[dataType])
            )
            noValues = ('', ) * (len(fields[dataType]))
            for (li, values) in enumerate(tables['lexemes']):
                ri = values.pop(0)
                values.extend(
                    noValues
                    if ri == '' else tables[dataType][int(ri) - 1]
                )
            del tables[dataType]
            del fields[dataType]
        print(f'combination step 1: {" ".join(tables.keys())}')

    def combineBack():
        for dataType in ('etymology',):
            fields['lexemes'].extend(
                (f'{dataType[0:3]}_{f}' for f in fields[dataType][1:])
            )
            lookup = {}
            for (di, values) in enumerate(tables[dataType]):
                lexId = values[0]
                if lexId != '':
                    li = int(lexId) - 1
                    if li in lookup:
                        print(
                            f'WARNING: multiple {dataType}s add features to'
                            f' {li}: {di} overrides {lookup[li]}'
                        )
                    lookup[li] = di
            noValues = ('', ) * (len(fields[dataType]) - 1)
            for (li, values) in enumerate(tables['lexemes']):
                di = lookup.get(li, None)
                values.extend(
                    noValues
                    if di is None else tables[dataType][lookup[li]][1:]
                )
            del tables[dataType]
            del fields[dataType]
        print(f'combination step 2: {" ".join(tables.keys())}')

    def write():
        for dataType in tables:
            theseFields = fields[dataType]
            print(dataType, theseFields)
            with open(f'{CSV_BASE}/{dataType}.csv', 'w') as fh:
                fieldsFmt = ('{}\t' * (len(theseFields) - 1)) + '{}\n'
                lines = tables[dataType]
                fh.write(fieldsFmt.format(*theseFields))
                for values in lines:
                    fh.write(fieldsFmt.format(*values))
            print(f'written {dataType}.csv')

    collect()
    combineForth()
    combineBack()
    write()


makeCsv()
