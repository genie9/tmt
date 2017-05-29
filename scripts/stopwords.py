import re, sys
import pandas as pd


def find_junk(words_file, junk_file, doc_freq, word_freq, doc_cov) :
    tbl = pd.read_csv(words_file, sep=',', header=0, names=['word','doc_freq','word_freq','doc_cov'])
    junk = tbl[(tbl['doc_freq']<doc_freq) | (tbl['word_freq']<word_freq) | (tbl['doc_cov']>doc_cov)] 
    
    print junk.shape
    print junk
    
    junk['word'].to_csv(junk_file, index=False)    


def main(argv) :
    if len(argv) != 6 :
        print '**Usage ', argv[0], '<corpus file> <junk file> <document coverage < num> <word count < num> <document coverage > p%>'
        sys.exit()

    corpus = argv[1]
    junk = argv[2]
    doc_freq = argv[3]
    word_freq = argv[4]
    doc_cov = argv[5]
   
    find_junk(corpus, junk, int(doc_freq), int(word_freq), int(doc_cov))
 
    pass


if __name__ == "__main__":
    main(sys.argv)

