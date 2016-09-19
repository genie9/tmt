import sys,os
import pandas as pd


def do_count(s) :
    print s
    counted = (f.split().count(s) for f in red)
    counted = [i for i in counted if i > 0]
    
    docs = len(counted)
    print docs
    
    doc_cov = (float(docs)/float(35162))*100#35162
    print doc_cov

    freq = sum(counted)
    print freq

    per_doc = 0
    if freq > 0 :
        per_doc = freq/docs
    print per_doc
    return [docs, doc_cov, freq, per_doc]


path = '/data/mallet_tests/to_mallet/full4/'

files = os.listdir(path)

opened = (open(path+f) for f in files)

red = [f.read() for f in opened]

nonii = [line.split(',')[0] for line in open('/data/mallet_tests/word_dist.csv')]

df = pd.DataFrame( (do_count(s) for s in nonii), index=nonii, columns=['docs', 'doc_cov', 'freq', 'per_doc'])
print df
df.sort_values(by='doc_cov',inplace =True)
print df
df.to_csv('/data/mallet_tests/word_docs_dist.txt')
