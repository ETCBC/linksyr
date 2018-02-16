import os
import collections
import operator
from shutil import rmtree
from glob import glob
from functools import reduce
from tf.fabric import Fabric

from constants import NT_BOOKS, SyrNT

BASE_DIR = os.path.expanduser(f'~/github/etcbc')
REPO = 'linksyr'
REPO_DIR = (f'{BASE_DIR}/{REPO}')
ORIGIN = 'syrnt'
SOURCE_DIR = f'{REPO_DIR}/data/{ORIGIN}'

TF_BASE = f'{REPO_DIR}/data/tf'
TF_DIR = f'{TF_BASE}/{ORIGIN}'

TEMP_DIR = f'{REPO_DIR}/_temp'

# -1 is unlimited

LIMIT = -1
SHOW = True

for cdir in (TEMP_DIR, TF_DIR):
    os.makedirs(cdir, exist_ok=True)

commonMetaData = dict(
    dataset=ORIGIN,
    datasetName='Syriac New Testament',
    source='SEDRA',
    sourceUrl='?',
    encoders=('? (transcription),'
              '? (annotation)'
              'and Dirk Roorda (TF)'),
    email1=('?'),
    email2='dirk.roorda@dans.knaw.nl',
)
specificMetaData = dict(
    book='book name',
    chapter='chapter number',
    verse='verse number',
    form='full form of the word',
)
numFeatures = set(
    '''
    chapter
    verse
    feminine_he_dot
'''.strip().split()
)

oText = {
    'sectionFeatures': 'book,chapter,verse',
    'sectionTypes': 'book,chapter,verse',
    'fmt:text-orig-full': '{form} ',
}


def readCorpus():
    files = glob(f'{SOURCE_DIR}/*.txt')
    nLines = 0
    stop = False
    for f in files:
        (dirF, fileF) = os.path.split(f)
        (corpus, ext) = os.path.splitext(fileF)
        print(f'File "{corpus}" ...')
        with open(f) as fh:
            for (ln, line) in enumerate(fh):
                if nLines == LIMIT:
                    stop = True
                    break
                nLines += 1
                yield (ln + 1, line.rstrip('\n'))
        if stop:
            break


def getVerseLabels():
    verseLabels = []
    for (book, chapters) in NT_BOOKS:
        for (chapter, verseCount) in enumerate(chapters):
            for v in range(1, verseCount + 1):
                verseLabels.append((book, chapter + 1, v))
    return verseLabels


def parseCorpus():
    annotSpecs = SyrNT.ANNOTATIONS
    cur = collections.Counter()
    curSlot = 0
    context = []
    nodeFeatures = collections.defaultdict(dict)
    edgeFeatures = collections.defaultdict(
        lambda: collections.defaultdict(set)
    )
    oSlots = collections.defaultdict(set)
    verseLabels = getVerseLabels()
    (prevBook, prevChapter) = (None, None)
    for p in readCorpus():
        (book, chapter, verse) = verseLabels[cur['verse']]
        if book != prevBook:
            print(
                f'\t{book:<12} current:'
                f' b={cur["book"]:>2}'
                f' c={cur["chapter"]:>3}'
                f' v={cur["verse"]:>4}'
                f' w={curSlot:>6}'
            )
            if prevChapter is not None:
                context.pop()
                prevChapter = None
            if prevBook is not None:
                context.pop()
            cur['book'] += 1
            prevBook = book
            nodeFeatures['book'][('book', cur['book'])] = book
            context.append(('book', cur['book']))
        if chapter != prevChapter:
            if prevChapter is not None:
                context.pop()
            cur['chapter'] += 1
            prevChapter = chapter
            nodeFeatures['chapter'][('chapter', cur['chapter'])] = chapter
            context.append(('chapter', cur['chapter']))

        cur['verse'] += 1
        nodeFeatures['verse'][('verse', cur['verse'])] = verse
        (ln, line) = p
        words = line.split()
        context.append(('verse', cur['verse']))
        for word in words:
            curSlot += 1
            (form, annotationStr) = word.split('|', 1)
            annotations = annotationStr.split('#')
            nodeFeatures['form'][('word', curSlot)] = form
            for ((feature, values), data) in zip(annotSpecs, annotations):
                value = data if values is None else values[int(data)]
                nodeFeatures[feature][('word', curSlot)] = value
            for (nt, curNode) in context:
                oSlots[(nt, curNode)].add(curSlot)
        context.pop()
    context.pop()
    context.pop()

    print('')

    if SHOW:
        if LIMIT == -1:
            for ft in sorted(nodeFeatures):
                print(ft)
                for n in range(1, 5):
                    for ntp in ('book', 'chapter', 'verse', 'word'):
                        if (ntp, n) in nodeFeatures[ft]:
                            print(f'\t"{nodeFeatures[ft][(ntp, n)]}"')
        else:
            print(nodeFeatures)
            print(oSlots)

    if len(context):
        print('Context:', context)

    print(f'\n{curSlot:>7} x slot')
    for (nodeType, amount) in sorted(cur.items(), key=lambda x: (x[1], x[0])):
        print(f'{amount:>7} x {nodeType}')

    nValues = reduce(
        operator.add, (len(values) for values in nodeFeatures.values()), 0
    )
    print(f'{len(nodeFeatures)} node features with {nValues} values')
    print(f'{len(oSlots)} nodes linked to slots')

    print('Compiling TF data')
    print(f'Building warp feature otype')
    nodeOffset = {'word': 0}
    oType = {}
    n = 1
    for k in range(n, curSlot + 1):
        oType[k] = 'word'
    n = curSlot + 1
    for (nodeType, amount) in sorted(cur.items(), key=lambda x: (x[1], x[0])):
        nodeOffset[nodeType] = n - 1
        for k in range(n, n + amount):
            oType[k] = nodeType
        n = n + amount
    print(f'{len(oType)} nodes')

    print('Filling in the nodes for features')
    newNodeFeatures = collections.defaultdict(dict)
    for (ft, featureData) in nodeFeatures.items():
        newFeatureData = {}
        for ((nodeType, node), value) in featureData.items():
            newFeatureData[nodeOffset[nodeType] + node] = value
        newNodeFeatures[ft] = newFeatureData
    newOslots = {}
    for ((nodeType, node), slots) in oSlots.items():
        newOslots[nodeOffset[nodeType] + node] = slots

    nodeFeatures = newNodeFeatures
    nodeFeatures['otype'] = oType
    edgeFeatures['oslots'] = newOslots

    print(f'Node features: {" ".join(nodeFeatures)}')
    print(f'Edge features: {" ".join(edgeFeatures)}')

    metaData = {
        '': commonMetaData,
        'otext': oText,
        'oslots': dict(valueType='str'),
    }
    for ft in set(nodeFeatures) | set(edgeFeatures):
        metaData.setdefault(
            ft, {}
        )['valueType'] = 'int' if ft in numFeatures else 'str'
        if ft in specificMetaData:
            metaData[ft]['description'] = specificMetaData[ft]

    print(f'Remove existing TF directory')
    rmtree(TF_DIR)
    print(f'Save TF dataset')
    TF = Fabric(locations=TF_DIR, silent=True)
    TF.save(
        nodeFeatures=nodeFeatures,
        edgeFeatures=edgeFeatures,
        metaData=metaData
    )


def loadTf():
    print(f'Load TF dataset for the first time')
    TF = Fabric(locations=TF_DIR, modules=[''])
    TF.load('')
    allFeatures = TF.explore(silent=False, show=True)
    loadableFeatures = allFeatures['nodes'] + allFeatures['edges']
    TF.load(loadableFeatures)

    print('All done')


def main():
    # parseCorpus()
    loadTf()


main()
