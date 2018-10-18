import pandas as pd

df=pd.read_csv('DATA2.csv')

Search_for_These_values = ['PEA', 'DEF', 'XYZ'] #creating list

pattern = '|'.join(Search_for_These_values)     # joining list for comparison

IScritical=df['COLUMN_to_Check'].str.contains(pattern)

df['NEWcolumn'] = IScritical.replace((True,False), ('YES','NO'))


