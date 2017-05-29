import pandas as pd
from pandas import read_csv
import os, glob, json, sys


argv = sys.argv
if len(argv) < 3 :
    print '**Usage ', argv[0], ': <root to arxiv file> <root to working file>.'
    sys.exit()

a_root = argv[1]
root = argv[2]

# number 4 stands for length of standard arxiv path length
n = len(a_root.split('/'))+3

all_arxiv = '{}all_arxiv.txt'.format(a_root)
set_ids = '{}meta_ids.txt'.format(root)

mega_list = pd.read_csv(all_arxiv, delimiter='/', names=range(n), na_values=[''], dtype=object)
mega_list['id'] = mega_list[n-2]

# catenating path's elements 
mega_list['path'] =mega_list.iloc[:,0:n-1].apply(lambda x: '/'.join(x), axis=1) 

print 'done building paths'
print mega_list.shape

# finding and cleaning id numbers from shorter paths 
short_list = mega_list[mega_list[n-2].str.contains('.xml') == True]
short_list['id'] = short_list.id.str.replace('.xml', '')

print 'outer XML files found'
print short_list.shape

# finding and cleaning id numbers from deeper paths with xml files
mega_list = mega_list[mega_list[n-1].str.contains('.xml') == True]
mega_list.drop_duplicates(subset='id', keep='first', inplace=True)

print 'inner XML files found'
print mega_list.shape

# combining path data and cleaning table
mega_list = pd.concat([mega_list, short_list])
mega_list = mega_list.drop(range(n), axis=1)

print 'done building id table'
print mega_list.shape

# combining data with interesting id numbers
arxiv_list = pd.read_csv(set_ids, delimiter='\n', names=['id'], dtype=object)

print 'fetched arxiv ids to table' 
print arxiv_list.shape

# comparing interesting id numbers with available 
new_list = pd.merge(mega_list, arxiv_list, left_on='id', right_on='id', how='inner')
print new_list

print 'done matching paths with ids' 
print new_list.shape

# saving to scv and json
new_list.to_csv('{}paths.csv'.format(root), header=False, index=False )

print 'done, ids and paths saved to file'

