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
    [x.extract() for x in soup.findAll('Math')]

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
        
#            sec_tag = Strain('section')
            soup = Soup(texml.read(), 'lxml')
#            os.makedirs(dest_path + '/' + article)
        
#            i = 0
#           for sec in soup.findAll('section') :
            dest_file = dest_path + '/' + article + '.txt'
            try :
                with io.open(dest_file, 'w', encoding='utf8') as ifile :
                    print 'dest_file ', dest_file 
                    ifile.write(xml_clean(sec) + '\n')
                    i += 1 
                ifile.closed
            except IOError :
                print dest_file,' not found'
                return 
                
            
#            texml_text = texml.read()
#            print len(texml_text)
#            
#            i = 0
#            istart = 0
#            iend = 0
#
#            wend = '</section>' #sys.argv[3]
#            wend_len = len(wend)
#            
#            while True:
#                istart = texml_text.find('<section ', iend)
#                if istart == -1 : break
#
#                iend = texml_text.find(wend, istart)
#
#                if iend != -1 :
#  
#                  with io.open(dest_path + article + '_' + str(i) + '.txt', 'w', encoding='utf8') as ifile :
#                        texml.seek(istart)
#                        soup = Soup(texml.read(iend + wend_len - istart), 'xml')
#                        ifile.write(unicode(xml_clean(soup)) + '\n')
#                        i += 1 
#                        texml.seek(iend)
#                  ifile.closed
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
        xml_open(f, dest_path)
    
    pass

if __name__ == "__main__":
    main(sys.argv)
