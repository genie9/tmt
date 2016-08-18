from bs4 import BeautifulSoup as Soup
from bs4 import SoupStrainer as Strain
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string, re
import sys, os, io
#from os import listdir


# Takes cl arguments for input and output paths.
# Divides tex.xml-text between '<section' and '</section' tags, 
# cleans xml formating, math-tags, stop words and punctuation.
# Processes with stemmer.
# Processed file is separeted between sections and saved in individual files
# to destination path named by original article id and incremental count as txt files.
#
 
def xml_clean(soup) :
    [x.decompose() for x in soup.findAll('math')]

    s = soup.get_text()

    s_words = stopwords.words('english')

    stemmer = SnowballStemmer('english')
    
    bad_chars = set(string.digits + string.punctuation)

    s = s.lower().strip()

    s = ''.join([ i if i not in bad_chars else ' ' for i in s ])

    s = ' '.join([ i if i not in s_words else '' for i in s.split() ])
 
    s = ' '.join([ stemmer.stem(word) for word in s.split() ])
    return unicode(s)


def xml_open(in_file, dest_path) :
    try :
        with open(in_file, 'r') as texml :
            s = texml.name.rfind('/')
            e = texml.name.find('.xml', s)
            article = texml.name[s+1:e]
            
            print 'processing ', texml, ', output file :', article
        
            sec_tag = Strain('section')
            soup = Soup(texml.read(), 'lxml', parse_only=sec_tag )
        
            dest_file = dest_path + '/' + article + '.txt'

            try :
                with io.open(dest_file, 'w', encoding='utf8') as ifile :
                    print 'dest_file ', dest_file 
                    ifile.write(xml_clean(soup) + '\n')
                ifile.closed
            except IOError :
                print dest_file,' not found'
                return 
                
        texml.closed

    except IOError :
        print in_file,' not found'
        return 



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
        xml_open(in_path+f, dest_path)
    
    pass

if __name__ == "__main__":
    main(sys.argv)
