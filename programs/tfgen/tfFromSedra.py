import sys
import collections

# import modified version in this directory
# not the one next to sedra.py !

import constants  # noqa: F401

sys.path.append('../parsing')

import sedra  # noqa: E402

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
        toNode=True,
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
        toNode=True,
        linkType=('roots', 'root_addr'),
        hasFeats=True,
        main=[('lexeme', 'lex_str')],
        skipFeats=set(),
    ),
    english=dict(
        nodeType='lexeme',
        toNode=False,
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
        nodeType='lexeme',
        toNode=False,
        linkType=('lexemes', 'lex_addr'),
        hasFeats=False,
        main=[],
        skipFeats=set(),
    ),
    roots=dict(
        nodeType='root',
        toNode=True,
        linkType=None,
        hasFeats=False,
        main=[('root', 'rt_str')],
        skipFeats={
            'RESERVED',
        },
    ),
)


def makeTf():
    nodeFeatures = collections.defaultdict(dict)
    oSlots = collections.defaultdict(set)

    for (d, (dataType, dataConfig)) in enumerate(dataTypes.items()):
        nodeType = dataConfig['nodeType']
        toNode = dataConfig['toNode']
        linkType = dataConfig['linkType']
        hasFeats = dataConfig['hasFeats']
        skipFeats = dataConfig['skipFeats']
        mainFeatures = dataConfig['main']
        data = getattr(db, dataType)
        print(f'{dataType:<10}: items 0 .. {len(data) -1:>5}')
        for (i, item) in enumerate(data):
            sys.stderr.write(f'{"":<12} item      {i:>5}\r')
            if linkType:
                (linkDataType, linkField) = linkType
                linkNodeType = dataTypes[linkDataType]['nodeType']
                link = getattr(item, linkField)
                num = link[1] if link else None

            if d == 0:
                curNode = ('word', i + 1)
                if num is not None:
                    oSlots[(linkNodeType, num + 1)].add(i + 1)
            else:
                if toNode:
                    curNode = (nodeType, i + 1)
                    if linkType:
                        if num is not None:
                            oSlots[(linkNodeType, num + 1)] |= oSlots[curNode]
                else:
                    if linkType:
                        if num is not None:
                            curNode = (linkNodeType, num + 1)

            for (k, f) in mainFeatures:
                if k not in skipFeats:
                    nodeFeatures[k][curNode] = getattr(item, f)
            for (k, v) in item.attributes._asdict().items():
                if k not in skipFeats:
                    nodeFeatures[k][curNode] = v
            if hasFeats:
                for (k, v) in item.features._asdict().items():
                    if k not in skipFeats:
                        nodeFeatures[k][curNode] = v
        print(f'{"":<12} item      {i:>5}')

    # print(nodeFeatures)
    return
    for feat in sorted(nodeFeatures):
        print(f'{feat}')
        for (ntp, n) in sorted(nodeFeatures[feat]):
            print(f'\t{ntp}{n} => {nodeFeatures[feat][(ntp, n)]}')

    print('\n')
    print('oslots')
    for (ntp, n) in sorted(oSlots):
        print(f'\t{ntp}{n} => {oSlots[(ntp, n)]}')


makeTf()
