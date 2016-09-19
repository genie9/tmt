from gensim.models.phrases import Phrases
import os, sys
import pandas as pd
from nltk.stem import SnowballStemmer


stemmer = SnowballStemmer('english')

path = '/data/mallet_tests/preproc/full_stem/'
files = os.listdir(path)
opened = (open(path+f) for f in files if f not in ['full'])
read = [(f, f.read().split()) for f in opened]
t = [d for f,d in read]
bigram = Phrases(t, threshold=5.0)


#for phrase, score in bigram.export_phrases([j for i,j in read]) :
#    print (u'{0} {1}'.format(phrase,score))
#sys.exit()

####### analyse bigrams ########################################

#bigr = [(u'{0} {1}'.format(phrase,score)) for phrase, score in bigram.export_phrases(read)]
#df = pd.DataFrame(bigr)
#df = df.sort_values(0)
#df['phrase'] = apply(df['0'][0])
#u = open('/data/mallet_tests/bigrams_non_stem.txt', 'w')
#u.write(str(df[0].unique()))
#u.closed
#print df[0].unique()
#sys.exit()
################################################################

def save_docs(f,d) :
#    print d
#    sys.exit()
    d = map(lambda x: x.encode('utf8'), d)
#    d = ' '.join( map(lambda x: x.encode('utf8'), d))
    
#    d = ' '.join(( stemmer.stem(i) for i in d.split() ))
#    d = ' '.join(map(lambda x : stemmer.stem(x), d))
    d = ' '.join(d)

    o = open('/data/mallet_tests/to_mallet/bigrams/full_stem_5/'+str(f.name.rsplit('/',1)[1]), 'w')
    o.write(str(d))
    o.closed

  
[save_docs(f,bigram[d]) for f,d in read]


########## trigrams ###########################################

#trigram = Phrases(bigram[t],threshold=5.0)
#
#for phrase, score in trigram.export_phrases(a):
#    print (u'{0} {1}'.format(phrase,score))

##############################################################
