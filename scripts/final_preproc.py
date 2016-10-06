import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import pandas as pd
import sys, os, io


# nltk text processing helpers
nltk.download('stopwords')
s_words = stopwords.words('english')
stemmer = SnowballStemmer('english')
#s = ' '.join(( stemmer.stem(i) for i in s.split() ))

i = 0
def txt_match(in_file, doc, dest_path, junk) :
    global i
    i += 1

    s = pd.Series(open(in_file+doc).read().split())
    s = s[-s.isin(junk)].str.cat(sep=' ')
 
    dest_file = dest_path + doc

    with io.open(dest_file, 'w', encoding='utf8') as clean_txt :
        print 'saving to ', clean_txt.name
        clean_txt.write(unicode(s)+'\n')
    clean_txt.closed
    
    print i

################################################################


def main(argv):
    
    if len(argv) != 4 :
        print '**Usage: ', argv[0], '<input path> <output path> <stopwords file>'
        sys.exit()
    
    in_path = argv[1]
    dest_path = argv[2]
    junk_file = argv[3]

    junk = pd.Series(open(junk_file).read().split()+['let'])
    
    if not os.path.exists(dest_path) :
        os.makedirs(dest_path)

    if dest_path[len(dest_path)-1] != '/' :
        dest_path += '/'

    map(lambda x : txt_match(in_path, x, dest_path, junk), os.listdir(in_path))
    
    pass


if __name__ == "__main__":
    main(sys.argv)
