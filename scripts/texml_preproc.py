from bs4 import BeautifulSoup as Soup
from bs4 import SoupStrainer as Strain
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string, re
import sys, os, io


# Takes cl arguments for input and output paths.
# Divides tex.xml-text between 'section' or 'paragrath' tags, 
# cleans xml formating, math-tags, stop words and punctuation.
# Processes with stemmer.
# If 'split' is given as argument, processed file is separeted between tags and saved in individual files
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


def xml_open(in_file, dest_path, size) :
    soup = ''
    tag = ''
    print in_file
    try :
        with open(in_file, 'r') as texml :
            s = texml.name.rfind('/')
            e = texml.name.find('.xml', s)
            article = texml.name[s+1:e]
            
            par = 'paragraph'
            sec = 'section'

            print 'processing ', texml, ', output file :', article
            
            sec_tag = Strain(sec)
            par_tag = Strain(par)

            soup_s = Soup(texml.read(), 'lxml', parse_only=sec_tag)
#            print 'section %s' % len(soup_s)
            texml.seek(0)
            soup_p = Soup(texml.read(), 'lxml', parse_only=par_tag)
#            print 'paragraph %s' % len(soup_p)

            if len(soup_s) == 0 :
#                print 'NOT FOUND SECTION'           
                if len(soup_p) != 0 :
                    tag = par
                    soup = soup_p
#                    print 'FOUND PARAGRAPH'
#                else : print 'NOT FOUND PARAGRAPH'
            if len(soup_s) != 0 :
                tag = sec
                soup = soup_s
#                print 'FOUND SECTION' 
            if len(soup_s) == 0 and len(soup_p) == 0 : 
                try :
                    with io.open('/data/mallet_tests/'+ size + 'aaa_errorfiles.txt', 'a', encoding='utf8') as erfile :
                        erfile.write(unicode(texml.name) + '\n')
                        print '%s added to error file' % texml.name
                    erfile.closed
                except IOError :
                    print 'file not found'
                    return                                  
                return

            if size == 'split' :
                print make_sec_files(dest_path, article, soup, tag)
            if size == 'full' :
                print make_art_file(dest_path, article, soup)

        texml.closed

    except IOError :
        print in_file,' not found'
        return 



########################## new defs #############################

def make_sec_files(dest_path, article, soup, tag) :
    os.makedirs(dest_path + '/' + article)

    i = 0
    for sec in soup.findAll(tag) :
        dest_file = dest_path + '/' + article + '/' + article + '_' + str(i) + '.txt'
        try :
            with io.open(dest_file, 'w', encoding='utf8') as ifile :
                ifile.write(xml_clean(sec) + '\n')
                i += 1 
            ifile.closed
        except IOError :
            print dest_file,' not found'
            return 

#    if make_sec_files(dest_path, soup)[0] == 0 :
    return 'article %s processed, splited in %d files' % (article, i)

#################################################################            

def make_art_file(dest_path, article, soup) :
    
    dest_file = dest_path + '/' + article + '.txt'
    try :
        with io.open(dest_file, 'w', encoding='utf8') as ifile :
            ifile.write(xml_clean(soup) + '\n')
        ifile.closed
    except IOError :
        print dest_file,' not found'
        return 

    return 'article %s processed' % article

################################################################


def main(argv):
    
    if len(argv) != 4 :
        print '**Usage: ', argv[0], ' ( <full> | <split> ) <input path> <output path>'
        sys.exit()
    
    size = argv[1]
    
    if  size != 'full' or size != 'split' :
        print '**Usage: ', argv[0], ' ( <full> | <split> ) <input path> <output path>'
        sys.exit()

    in_path = argv[2]
    dest_path = argv[3]

    if os.path.exists('/data/mallet_tests/'+ size + '/aaa_errorfiles.txt') :
        os.remove('/data/mallet_tests/'+ size + 'aaa_errorfiles.txt')
 
    if not os.path.exists(dest_path) :
        os.makedirs(dest_path)

    if dest_path[len(dest_path)-1] != '/' :
        dest_path += '/'
    
    for f in os.listdir(in_path) :
         xml_open(in_path + f, dest_path, size)
    
    pass


if __name__ == "__main__":
    main(sys.argv)
