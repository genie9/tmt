import re, sys
import pandas as pd


def find_junk(words_file, junk_file, doc_freq, word_freq, doc_cov) :
    tbl = pd.read_csv(words_file, sep=',', header=0, names=['word','doc_freq','word_freq','doc_cov'])
    junk = tbl[(tbl['doc_freq']<4) | (tbl['word_freq']<6) | (tbl['doc_cov']>80)] 
    
    print junk.shape
    print junk
    
    junk['word'].to_csv(junk_file, index=False)    


def main(argv) :
    if len(argv) != 6 :
        print '**Usage ', argv[0], '<word list file> <junk file> <document coverage < num> <word count < num> <document coverage > p%>'
        sys.exit()

    words_file = argv[1]
    junk_file = argv[2]
    doc_freq = argv[3]
    word_freq = argv[4]
    doc_cov = argv[5]
    
    find_junk(words_file, junk_file, doc_freq, word_freq, doc_cov)
 
    pass


if __name__ == "__main__":
    main(sys.argv)








#def stopwords(inpath, destpath) :
#    r = '([0-9]+:[1-6]|$)'
#    with open(inpath, 'r') as data :
#        with open(destpath, 'w') as stopwords :
#            for line in data :
#                l = line.split()
#                if len(l) == 3 :
#                    s = l[2]
#                    if len(re.sub(r,'',s)) == 0 :
#                        stopwords.write(l[1]+'\n')
#        stopwords.closed
#    data.closed
#
#def word2doc(in_file, dest_file) :
#    with open(in_file, 'r') as words :
#        a = [line.split()[1:] for line in words]
#        a = ([line[0],len(line)-1] for line in a)
#        df = pd.DataFrame(a)
#        df.apply()
#        print df
##            sys.exit()
#    words.closed
#
