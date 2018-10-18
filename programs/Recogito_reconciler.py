import csv
import sys
file1 = sys.argv[1]
file2 = sys.argv[2]
with open(file2, 'r') as r:
    with open(file1, 'r') as f:
        csv_f = csv.reader(f)
        csv_r = csv.reader(r)
        bar = [linex for linex in csv_r]
        foo = [liney[2:] for liney in csv_f]
        zipped = zip(bar,foo)
        result = [x+y for (x,y) in list(zipped)]
        for i in result:
            print(','.join(i))
