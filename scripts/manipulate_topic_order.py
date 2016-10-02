import pandas as pd
import sys

full_keys = '/data/mallet_tests/from_mallet/topics_50/full2/full2_50_keys.txt'
full_comp = '/data/mallet_tests/from_mallet/topics_50/full2/full2_50_compostion.txt'
sect_keys = '/data/mallet_tests/from_mallet/topics_50/sections2/sections2_50_keys.txt'
sect_comp = '/data/mallet_tests/from_mallet/topics_50/sections2/sections2_50_compostion.txt'
new_order = '/data/mallet_tests/from_mallet/topics_50/new_order.txt'

df_full = pd.read_csv(full_keys, sep=' ',index_col=False,header=None,names=['word_0']+['word_'+str(i+1) for i in xrange(19)])
df_sect = pd.read_csv(sect_keys, sep=' ',index_col=False,header=None,names=['word_0']+['word_'+str(i+1) for i in xrange(19)])

df_full.word_0 = df_full.word_0.str.split('\t').str[2]
df_sect.word_0 = df_sect.word_0.str.split('\t').str[2]
###################
print df_full
print df_sect

def do_summs(df_full_i,df_sect) :    
    df_bool = [df_full_i.isin(df_sect.iloc[j]) for j in xrange(50)]
    df_bool = pd.DataFrame(df_bool,index=[i for i in xrange(50)]).T
    df_bool = df_bool.sum()
    return df_bool

df_summs = [do_summs(df_full.iloc[i],df_sect) for i in xrange(50)]

df_summs = pd.DataFrame(df_summs)

for i in xrange(50) :
    print df_summs.iloc[[i]].T

topics = df_summs.idxmax(axis=0)

with open(new_order,'w') as f :
    f.write(topics.to_string())
f.closed

print topics

