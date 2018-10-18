import fuzzywuzzy
import pandas as pd
import numpy as np

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

data = pd.read_csv('BLC.txt', sep=" ", header=None)
data2 = pd.read_csv('index_of_places.csv')

df1=pd.DataFrame.from_dict(data,orient='index')
df2=pd.DataFrame.from_dict(data2,orient='index')

df1.columns=['Strings']
df2.columns=['Locations']

def match(Col1,Col2):
    overall=[]
    for n in Col1
        result=[(fuzz.partial_ratio(n, n2),n2)
                for n2 in Col2 if fuzz.partial_ratio(n, n2)>85]
        if len(result):
            result.sort()
            print('result {}'.format(result))
            print("Best M={}".format(result[-1][1]))
            overall.append(result[-1][1])
        else:
            overall.append(" ")
    return overall

print (match(df1.String, df2.Location))


