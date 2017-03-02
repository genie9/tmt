import pandas as pd
from pandas import read_csv
import os, glob, json


path = '/data/pulp/support/'

mega_list = pd.read_csv('/home/evly/tmt/bigdata/find', delimiter='/', names=['A','path0','path1','path2','path3', 'FILE'], na_values=[''], dtype=object)
mega_list = mega_list.drop('A', axis=1)

# creating id-column for matching
mega_list['id'] = mega_list['path3']
# catenating path's elements 
mega_list['path'] = '/'+mega_list['path0']+'/'+mega_list['path1']+'/'+mega_list['path2']+'/'+mega_list['path3']

print 'first.0 done'
print mega_list.shape

# finding and cleaning id numbers from shorter paths 
short_list = mega_list[mega_list.path3.str.contains('.xml') == True]
short_list['id'] = short_list.id.str.replace('.xml', '')

print 'first.1 done'
print short_list.shape

# finding and cleaning id numbers from deeper paths with xml files
mega_list = mega_list[mega_list.FILE.str.contains('.xml') == True]
mega_list.drop_duplicates(subset='id', keep='first', inplace=True)

print 'first.2 done'
print mega_list.shape

# combining path data and cleaning table
mega_list = pd.concat([mega_list, short_list])
mega_list = mega_list.drop(['path0','path1','path2','path3', 'FILE'], axis=1)

print 'first.3 done'
print mega_list.shape

# combining data with interesting id numbers
arxiv_list = pd.read_csv(path+'meta_arxiv.txt', delimiter='\n', names=['id'], dtype=object)

print 'second done, interesting ids:' 
print arxiv_list.shape

# comparing interesting id numbers with available 
new_list = pd.merge(mega_list, arxiv_list, left_on='id', right_on='id', how='inner')
new_list = new_list[['id', 'path']]

print 'third done, ids found:' 
print new_list.shape

# saving to scv and json
with open(path+'file_matrix.csv', 'w') as c_data :
    new_list.to_csv(c_data, index=False)
    print 'csv parsed'
c_data.closed
with open(path+'file_matrix.json', 'w') as j_data :
    new_list.to_json(j_data, orient='records')
    print 'json parsed'
j_data.closed

print 'fourth done' 


#lines.id.value_counts()

