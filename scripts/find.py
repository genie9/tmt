import pandas as pd
import numpy as np
from pandas import read_csv
import os, glob

#pd.options.display.float_format = '{:,.4f}'
mega_list = pd.read_csv("/home/evly/tmt/bigdata/find", delimiter='/', names=['A','B','C','D','E', 'F'], na_values=[''], dtype=object)
print 'first.0 done'
print mega_list.iloc[6000000:6000005,]
print mega_list.shape

E_list = mega_list[mega_list.E.str.contains('.xml') == True]
F_list = E_list.F
E_list.drop('F', 1)
pd.concat([E_list, F_list], axis=1, names=['A','B','C','D','E', 'F'])
E_list = E_list.E.str.replace('.xml', '')

print 'first.1 done'
print E_list.iloc[0:5,]
print E_list.shape

mega_list = mega_list[mega_list.F.str.contains('.xml') == True]
print 'first.2 done'
print mega_list.iloc[60000:60005,]
print mega_list.shape
#for f in os.listdir("/home/evly/tmt/bigdata/arxiv_meta/"):
#    print f

mega_list = pd.concat([mega_list, E_list])
print 'first.3 done'
print mega_list.iloc[0:10,]
print mega_list.shape

path = "/home/evly/tmt/bigdata/arxiv_meta/"
all_arxiv = glob.glob(os.path.join(path, "*"))
print 'second done' 

arxiv_list = pd.concat(pd.read_json(f, dtype=object) for f in all_arxiv) #, sep='"', names=['A','B','C','D','E','F','G','I','J']
print 'third done' 
print arxiv_list.iloc[0:5,]
print arxiv_list.shape

new_list = pd.merge(mega_list, arxiv_list, left_on='E', right_on='id', how='inner')
#print new_list.iloc[0:30,]
print 'fourth done' 

print new_list.shape
