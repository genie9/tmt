from gensim.models.phrases import Phrases
import os, sys
import pandas as pd
from nltk.stem import SnowballStemmer


stemmer = SnowballStemmer('english')

def print_bigrams(bigram,bigram_file) :
    #for phrase, score in bigram.export_phrases([j for i,j in read]) :
        print (u'{0} {1}'.format(phrase,score))
    #sys.exit()

    ####### save unique sorted bigrams ########################################

    bigr = [(u'{0} {1}'.format(phrase,score)) for phrase, score in bigram.export_phrases(read)]
    df = pd.DataFrame(bigr)
    df = df.sort_values(0)
    df['phrase'] = apply(df['0'][0])
    with open(bigram_file, 'w') as u :
        u.write(str(df[0].unique()))
    u.closed

    print df[0].unique()
    #sys.exit()


def save_docs(f,d,stem,dest_path) :
#    print d
    d = map(lambda x: x.encode('utf8'), d)
#    d = ' '.join( map(lambda x: x.encode('utf8'), d))
    if stem == True : 
        d = ' '.join(map(lambda x : stemmer.stem(x), d))
    else :
        d = ' '.join(d)

    with open(dest_path+str(f.name.rsplit('/',1)[1]), 'w') as o :
        o.write(str(d))
    o.closed

  

def main(argv):

    if len(argv) < 4 :
        print '**Usage: ', argv[0], '<input path> <output path> <threshold [1-10]> [stem]'
        sys.exit()

    in_path = argv[1]
    dest_path = argv[2]
    thres = float(argv[3])
    stem = False

    if len(argv) == 5 :
        if argv[4] == 'stem' :
            stem = True

    if not os.path.exists(dest_path) :
        os.makedirs(dest_path)

    if dest_path[len(dest_path)-1] != '/' :
        dest_path += '/'

    files = os.listdir(in_path)
    opened = (open(path+f) for f in files)
    
    read = [(f, f.read().split()) for f in opened]
    t = [d for f,d in read]
    
    bigram = Phrases(t, threshold=thres)

    ########## trigrams ###########################################

    #trigram = Phrases(bigram[t],threshold=5.0)
    #
    ## to print bigrams
    #for phrase, score in trigram.export_phrases(a):
    #    print (u'{0} {1}'.format(phrase,score))

    ##############################################################
#    # uncomment for use
#    print_bigrams(bigram, 'file')    
    
    [save_docs(f,bigram[d],stem,dest_path) for f,d in read]

    pass

if __name__ == "__main__":
    main(sys.argv)
