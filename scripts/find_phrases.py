from gensim.models.phrases import Phrases
import os, sys, subprocess
import pandas as pd
from nltk.stem import SnowballStemmer


stemmer = SnowballStemmer('english')

def print_bigrams(bigram,bigram_file) :
    #for phrase, score in bigram.export_phrases([j for i,j in read]) :
        #print (u'{0} {1}'.format(phrase,score))
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

i = 0
def save_docs(f,d,stem,dest_path) :
    global i
    print 'saving to ', dest_path

    d = map(lambda x: x.encode('utf8'), d)
#    d = ' '.join( map(lambda x: x.encode('utf8'), d))
    if stem == True : 
        d = ' '.join(map(lambda x : stemmer.stem(x), d))
    else :
        d = ' '.join(d)

    with open(dest_path+str(f.rsplit('/',1)[1]), 'w') as o :
        o.write(str(d))
        i += 1
    o.closed
    print i
  

def main(argv):

    if len(argv) < 6 :
        print '**Usage: ', argv[0], '<input path full> <input path sections> <output path full> <output path sections> <threshold [1-10]> [stem]'
        sys.exit()

    in_path_full = argv[1]
    in_path_sec = argv[2]
    dest_path_full = argv[3]
    dest_path_sec = argv[4]
    thres = float(argv[5])
    stem = False

    if len(argv) == 7 :
        if argv[6] == 'stem' :
            stem = True

    if not os.path.exists(dest_path_full) :
        os.makedirs(dest_path_full)
    if not os.path.exists(dest_path_sec) :
        os.makedirs(dest_path_sec)

    if dest_path_full[len(dest_path_full)-1] != '/' :
        dest_path_full += '/'
    if dest_path_sec[len(dest_path_sec)-1] != '/' :
        dest_path_sec += '/'

    files_full = os.listdir(in_path_full)
    opened = (open(in_path_full+f) for f in files_full)

    read = [(f, f.read().split()) for f in opened]
    t = [d for f,d in read]
    
    bigram = Phrases(t, threshold=thres,delimiter='-')

    ########## trigrams ###########################################

    #trigram = Phrases(bigram[t],threshold=5.0)
    #
    ## to print bigrams
    #for phrase, score in trigram.export_phrases(a):
    #    print (u'{0} {1}'.format(phrase,score))

    ##############################################################
#    # uncomment for use
#    print_bigrams(bigram, 'file')    
    
    [save_docs(f.name,bigram[d],stem,dest_path_full) for f,d in read]

    files_sec = subprocess.check_output(["find", in_path_sec, "-maxdepth", "2", "-mindepth", "2", "-type", "f"])
    
    [save_docs(i,bigram[d],stem,dest_path_sec) for i,d in [(f, open(f).read().split()) for f in files_sec.split() if os.path.isfile(f)]]

    pass

if __name__ == "__main__":
    main(sys.argv)
