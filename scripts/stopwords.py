import re, sys
import pandas as pd
from nltk.text import TextCollection as tc


def stopwords(inpath, destpath) :
    r = '([0-9]+:[1-6]|$)'
    with open(inpath, 'r') as data :
        with open(destpath, 'w') as stopwords :
            for line in data :
                l = line.split()
                if len(l) == 3 :
                    s = l[2]
                    if len(re.sub(r,'',s)) == 0 :
                        stopwords.write(l[1]+'\n')
        stopwords.closed
    data.closed

def word2doc(in_file, dest_file) :
    with open(in_file, 'r') as words :
        a = [line.split()[1:] for line in words]
        a = ([line[0],len(line)-1] for line in a)
        df = pd.DataFrame(a)
        df.apply()
        print df
#            sys.exit()
    words.closed


def main(argv) :
#    if len(argv) != 3 :
#        print '**Usage ', argv[0], '<word list file> <output file>'
#        sys.exit()

    in_file = '/data/mallet_tests/from_mallet/topics_50/full/full_50_wordcounts.txt'# argv[1]
    dest_file = '/data/mallet_tests/from_mallet/words_appear.txt'#argv[2]
    all_words = 
#    stopwords(in_file, dest_file)

    word2doc(in_file, dest_file)
   
    pass

if __name__ == "__main__":
    main(sys.argv)
