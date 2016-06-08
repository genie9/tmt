from bs4 import BeautifulSoup as Soup
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string, re
import sys, os, io
#from os import listdir


# Takes cl arguments for input file and output path.
# Divides tex.xml-text between '<section' and '</section' tags, 
# cleans xml formating, stop words and punctuation.
# Processes with stemmer.
# Processed file is separeted between sections  with two (2) 'new lines' and
# saved to destination path with original file name and .txt extension.
#
 
def xml_clean(soup) :
    [x.extract() for x in soup.findAll('Math')]

    s = soup.get_text()

    s_words = stopwords.words('english')

    stemmer = SnowballStemmer('english')
    
    bad_chars = set(string.digits + string.punctuation)

    s = s.lower().strip()

    s = ''.join([ i if i not in bad_chars else ' ' for i in s ])

    s = ' '.join([ i if i not in s_words else '' for i in s.split() ])
 
    s = ' '.join([ stemmer.stem(word) for word in s.split() ])

    return s


def xml_open(in_file, dest_path) :
    print in_file
    try :
        with open(in_file, 'r') as texml :
            s = texml.name.rfind('/')
            e = texml.name.find('.', s)
            filename = texml.name[s+1:e]

            print texml
            
            texml_text = texml.read()
            print len(texml_text)
            
            i = 0
            istart = 0
            iend = 0

            wend = '</section>' #sys.argv[3]
            wend_len = len(wend)
            
            while True:
                istart = texml_text.find('<section ', iend)
                if istart == -1 : break

                iend = texml_text.find(wend, istart)

                if iend != -1 :
                    with io.open(dest_path + filename + '_' + str(i) + '.txt', 'w', encoding='utf8') as ifile :
                        texml.seek(istart)
                        soup = Soup(texml.read(iend + wend_len - istart), 'xml')
                        ifile.write(xml_clean(soup) + '\n')
                        i += 1 
                        texml.seek(iend)
                    ifile.closed
        texml.closed

    except IOError :
        print in_file,' not found'
        return 

    print ' splited in ', i, 'files'


def main(argv):
    if len(argv) != 3 :
        print '**Usage ', argv[0], ': path to input directory, path to output directory.'
        sys.exit()

    in_path = argv[1]
    dest_path = argv[2]

    if not os.path.exists(dest_path) :
        os.makedirs(dest_path)

    if dest_path[len(dest_path)-1] != '/' :
        dest_path += '/'
    
    for f in os.listdir(in_path) :
        xml_open(in_path + f, dest_path)
    
    pass

if __name__ == "__main__":
    main(sys.argv)
