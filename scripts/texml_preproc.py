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


def xml_open(in_file, dest_path, new) :
    print in_file
    try :
        with open(in_file, 'r') as texml :
            s = texml.name.rfind('/')
            e = texml.name.find('.xml', s)
            article = texml.name[s+1:e]
            
            print 'processing ', texml, ', output file :', article
            
            sec_tag = Strain('section')
            soup = Soup(texml.read(), 'lxml', parse_only=sec_tag)
            
            if new == 'split' :
                if make_sec_files(dest_path, soup) == 0 :
                    try :
                        with io.open(dest_path+'aaa_errorfiles.txt', 'a', encoding='utf8') as erfile :
                            erfile.write(unicode(texml.name) + '\n')
                        erfile.closed
                    except IOError :
                        print 'file not found'
                        return 
                                        
                print ' splited in ', i, 'files'
            if new == 'full' :
                print make_art_file(dest_path)

        texml.closed

    except IOError :
        print in_file,' not found'
        return 



########################## new defs #############################
def make_sec_files(dest_path, soup) :
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

    return i

#################################################################            

def make_art_files(dest_path, soup) :

        dest_file = dest_path + '/' + article + '.txt'
        try :
            with io.open(dest_file, 'w', encoding='utf8') as ifile :
                s = xml_clean(soup)
                s_count = s 
                ifile.writei(s + '\n')
            ifile.closed
        except IOError :
            print dest_file,' not found'
            return 

    return i
#################################################################            

def main(argv):
    if len(argv) != 4 :
        print '**Usage: ', argv[0], ' ( <full> | <split> ) <input path> <output path>'
        sys.exit()

    in_path = argv[2]
    dest_path = argv[3]
  
    if not os.path.exists(dest_path) :
        os.makedirs(dest_path)

    if dest_path[len(dest_path)-1] != '/' :
        dest_path += '/'
    
    for f in os.listdir(in_path) :
         xml_open(in_path + f, dest_path)
    
    pass


if __name__ == "__main__":
    main(sys.argv)
