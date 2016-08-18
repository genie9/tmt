from bs4 import BeautifulSoup as Soup
from bs4 import SoupStrainer as Strain
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string, re
import sys, os, io


# Takes cl arguments for input and output paths.
# Divides tex.xml-text between '<section' and '</section' tags, 
# cleans xml formating, math-tags, stop words and punctuation.
# Processes with stemmer.
# Processed file is separeted between sections and saved in individual files
# to destination path named by original article id and incremental count as txt files.
#
 
def xml_clean(soup) :
    [x.extract() for x in soup.findAll('math')]

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
    print in_file
    try :
        with open(in_file, 'r') as texml :
            s = texml.name.rfind('/')
            e = texml.name.find('.xml', s)
            article = texml.name[s+1:e]
            
            print 'processing ', texml, ', output file :', article
            
            sec_tag = Strain('section')
            soup = Soup(texml.read(), 'lxml', parse_only=sec_tag)
            
            os.makedirs(dest_path + '/' + article)
        
            i = 0
            for sec in soup.findAll('section') :
                dest_file = dest_path + '/' + article + '/' + article + '_' + str(i) + '.txt'
                try :
                    with io.open(dest_file, 'w', encoding='utf8') as ifile :
                        ifile.write(xml_clean(sec) + '\n')
                        i += 1 
                    ifile.closed
                except IOError :
                    print dest_file,' not found'
                    return 

        texml.closed

    except IOError :
        print in_file,' not found'
        return 

    if i == 0 :
        try :
            with io.open(dest_path+'aaa_errorfiles.txt', 'a', encoding='utf8') as erfile :
                erfile.write(unicode(texml.name) + '\n')
            erfile.closed
        except IOError :
            print 'file not found'
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
