from bs4 import BeautifulSoup as Soup
from bs4 import SoupStrainer as Strain
import nltk
from nltk.corpus import stopwords
#nltk.download('stopwords')
from nltk.stem import SnowballStemmer
import numpy as np
import pandas as pd
import string, re
import sys, os, io
import enchant
import datetime as date
today =  date.date.today().strftime('%m%d%y')

# Takes cl arguments for input and output paths.
# Divides tex.xml-text between 'section' or 'paragrath' tags, 
# cleans xml formating, math-tags, stop words and punctuation.
# Processes with stemmer.
# If 'split' is given as argument, processed file is separeted between tags and saved in individual files
# to destination path named by original article id and incremental count as txt files.
#
 

def xml_clean(soup) :

    [ x.extract() for x in soup.findAll('math')]

    s = soup.get_text()
    
    s_words = stopwords.words('english')
     
    stemmer = SnowballStemmer('english')

    enchant_dict_us = enchant.Dict('en_US')
    enchant_dict_gb = enchant.Dict('en_GB')

    bad_chars = set(string.digits + string.punctuation)

    s = s.lower().strip()
    
    s = re.sub(r'-\s+', '', s)

    s = re.sub('[^a-z]', ' ', s)
    
#    s = ''.join([ i if i not in bad_chars else ' ' for i in s ]) 

    s = ' '.join([ i if i not in s_words else '' for i in s.split() ])

    s = ' '.join([ i if len(i) > 2 else '' for i in s.split() ])
    
    english = open('/home/evly/tmt/english.txt')
        
    wordz = set(english.read().split('\n'))

    s = ' '.join([ i for i in s.split() if enchant_dict_us.check(i) or enchant_dict_gb.check(i) or i in wordz ])

    s = ' '.join([ stemmer.stem(i) for i in s.split() ])

########### when we have junklist file #############################

    junk_file = open('/data/mallet_tests/from_mallet/test/full4/junk.txt')
    junk = set(junk_file.read().split('\n'))

    s = ' '.join([ i for i in s.split() if i not in junk])
#    junk_list = pd.read_csv(b_file, delimiter='/n', header=None, index_col=False, names=['words'], na_values='', keep_default_na=False, engine='python')

#    text = pd.Series(s.split()).T
#    text = pd.DataFrame(text, columns=['words'])
#    
#    bool_tbl = text.words.isin(junk_list.words)
#
#    text = text[bool_tbl == False]
#    text = text.words.tolist()
#    text = ' '.join(text)
#    return unicode(text)
    junk_file.closed
####################################################################

    english.closed
 
    return s


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
                write_error(texml.name)
                return

            if size == 'split' :
                print make_sec_files(dest_path, article, soup, tag)
            if size == 'full' :
                print make_art_file(dest_path, article, soup)

        texml.closed

    except IOError :
        print in_file,' not found'
        return 

################################################################

def write_error(file_name) :
    try :
        with io.open('/data/mallet_tests/aaa_' + today + '_errorfiles.txt', 'a', encoding='utf8') as erfile :
            erfile.write(unicode(file_name) + '\n')
            print '%s added to error file' % file_name
        erfile.closed
    except IOError :
        print 'file not found'
        return                                  
    return

########################## new defs #############################

def make_sec_files(dest_path, article, soup, tag) :
    if not os.path.exists(dest_path + '/' + article) :
        os.makedirs(dest_path + '/' + article)

    i = 0
    for sec in soup.findAll(tag) :
        dest_file = dest_path + '/' + article + '/' + article + '_' + str(i) + '.txt'
        s = xml_clean(sec)

        if len(s)>0 :
            try :
                with io.open(dest_file, 'w', encoding='utf8') as ifile :
                    ifile.write(s+'\n')
                    i += 1 
                ifile.closed
            except IOError :
                print dest_file,' not found'
                return 

    return 'article %s processed, splited in %d files' % (article, i)

#################################################################            

def make_art_file(dest_path, article, soup) :    
    dest_file = dest_path + '/' + article + '.txt'
    s = xml_clean(soup)

    if len(s)>0 :
        try :
            with io.open(dest_file, 'w', encoding='utf8') as ifile :
                ifile.write(s+'\n')
            ifile.closed
        except IOError :
            print dest_file,' not found'
            return
        #sys.exit()
        return 'article %s processed' % article
    else : 
        write_error(article)

################################################################


def main(argv):
    
    if len(argv) != 4 :
        print '**Usage: ', argv[0], ' ( <full> | <split> ) <input path> <output path>'
        sys.exit()
    
    size = argv[1]
    
    if  size not in ['full','split'] :
        print '**Usage: ', argv[0], ' ( <full> | <split> )!! <input path> <output path>'
        sys.exit()

    in_path = argv[2]
    dest_path = argv[3]

    if os.path.exists('/data/mallet_tests/aaa_' + today + '_errorfiles.txt') :
        os.remove('/data/mallet_tests/aaa_'+ today + '_errorfiles.txt')
 
    if not os.path.exists(dest_path) :
        os.makedirs(dest_path)

    if dest_path[len(dest_path)-1] != '/' :
        dest_path += '/'
    
    i = 0    
    for f in os.listdir(in_path) :
        xml_open(in_path + f, dest_path, size)
        i += 1
        print i
    pass


if __name__ == "__main__":
    main(sys.argv)
