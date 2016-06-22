import pandas as pd
#import numpy as np
from pandas import read_csv
from csv import DictReader 
import os, glob, json


path = "/home/evly/tmt/bigdata/"

mega_list = pd.read_csv(path+'find', delimiter='/', names=['A','path0','path1','path2','path3', 'FILE'], na_values=[''], dtype=object)
mega_list = mega_list.drop('A', axis=1)
mega_list['id'] = mega_list['path3']
print 'first.0 done'
#print mega_list.iloc[6000000:6000005,]
print mega_list.shape

short_list = mega_list[mega_list.path3.str.contains('.xml') == True]
#short_to_mallet = short_list
short_list['id'] = short_list.id.str.replace('.xml', '')
short_list['path'] = short_list['path0']+'/'+short_list['path1']+'/'+short_list['path2']+'/'+short_list['path3']
print 'first.1 done'
#print short_list.iloc[0:5,]
print short_list.shape

mega_list = mega_list[mega_list.FILE.str.contains('.xml') == True]
#mega_to_mallet = mega_list
mega_list['id'] = mega_list['path3']
mega_list['path'] = mega_list['path0']+'/'+mega_list['path1']+'/'+mega_list['path2']+'/'+mega_list['path3']+'/'+mega_list['FILE']
print 'first.2 done'
#print mega_list.iloc[60000:60005,]
print mega_list.shape

mega_list = pd.concat([mega_list, short_list])
#mega_to_mallet =  pd.concat([mega_to_mallet, short_to_mallet])
print 'first.3 done'
#print mega_list.iloc[10:30,]
print mega_list.shape

all_arxiv = glob.glob(os.path.join(path+'arxiv_meta/', "*"))
print 'second done' 

arxiv_list = pd.concat(pd.read_json(f, dtype=object) for f in all_arxiv) 
print 'third done' 
#print arxiv_list.iloc[10000:10015,]
print arxiv_list.shape

new_list = pd.merge(mega_list, arxiv_list, left_on='id', right_on='id', how='inner')
#new_list['path'] = new_list['path0']+'/'+new_list['path1']+'/'+new_list['path2']+'/'+new_list['path3']+'/'+new_list['FILE']
new_list = new_list.drop(['path0','path1','path2','path3', 'FILE'], axis=1)
print 'fourth done' 
#print new_list.iloc[10000:10010,]
print new_list.shape

#new_list.drop(new_list.columns[['id', 'url']], axis=1, inplace=True)

with open(path+'file_matrix.csv', 'r+') as c_data :
    #new_list.pivot(index=new_list['id'], values=new_list['path'])
    new_list.to_csv(c_data, sep=':', index=False)
    with open(path+'file_matrix.json', 'w') as j_data :
        fields = ('id','path')
        reader = DictReader(c_data,fields)
        out = json.dumps([row for row in reader])
        print 'parsed'
        j_data.write(out)
#        for row in reader :
#            json.dump(row, j_data)
#            j_data.write('\n')     
    j_data.closed
c_data.closed

