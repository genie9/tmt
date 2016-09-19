from bs4 import BeautifulSoup as Soup
from bs4 import SoupStrainer as Strain
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import numpy as np
import pandas as pd
import string, re
import sys, os, io, timeit
import enchant
import datetime as date

# Takes cl arguments for input and output paths.
# Divides tex.xml-text between 'section' or 'paragrath' tags, 
# cleans xml formating, math-tags, stop words and punctuation.
# Cheks if word is in vocalaburary or not misspeled.
# Processes with stemmer.
# If 'split' is given as argument, processed file is separeted between tags and saved in individual files
# to destination path named by original article id and incremental count as txt files.


#####################################################
###                 global stuff                  ###
#####################################################

# errorfile
today =  date.date.today().strftime('%m%d%y')
error_file = '/data/mallet_tests/aaa_' + today + '_errorfiles.txt'

# Alan's compilation of english nonbasic words
english = open('/home/evly/tmt/english.txt')
wordz = set(english.read().split('\n'))
df_wordz = pd.Series(list(wordz))
english.closed

# enchant dictionary
enchant_dict_us = enchant.Dict('en_US')
enchant_dict_gb = enchant.Dict('en_GB')

# nltk text processing helpers
nltk.download('stopwords')
s_words_nltk = set(stopwords.words('english'))
s_words_evly = set(['also','thus','however','therefore','about','followed','following','follows','etc','always','among','amongst'])
s_words = s_words_nltk.union(s_words_evly)

stemmer = SnowballStemmer('english')

# python's charachter methods
# deprecated after taking regex sub method in use
bad_chars = sorted(set(string.digits + string.punctuation))

# unfrequent and too frequent words
# examined from output data after first run of this script
junk_file = open('/data/mallet_tests/junkwords3.txt')
junk = ([line.split(',')[0] for line in junk_file])
df_junk = pd.Series(junk)
junk_file.closed


def xml_clean(soup) :

    [ x.extract() for x in soup.findAll('math')]

    s = soup.get_text()
    
    s = s.lower().strip()
    
    s = re.sub(r'-\s+', '', s)

    s = re.sub('[^a-z]', ' ', s)
    
#    s = ''.join([ i if i not in bad_chars else ' ' for i in s ]) 

    s = ' '.join(( i if i not in s_words else '' for i in s.split() ))

    s = ' '.join(( i if len(i) > 2 else '' for i in s.split() ))
    
    s = ' '.join(( i for i in s.split() if enchant_dict_us.check(i) or enchant_dict_gb.check(i) )) 
    
    df_soup = pd.Series(s.split())
    
    df_soup = df_soup[df_soup.isin(df_wordz)==True]
    
    s = ' '.join(i for i in df_soup.tolist())
    
    s = ' '.join(( stemmer.stem(i) for i in s.split() ))
    
    df_soup = pd.Series(s.split())
    
    df_soup = df_soup[df_soup.isin(df_junk)==False]
    
    s = ' '.join(i for i in df_soup.tolist())

#    print s
#    s = ' '.join(( i for i in s.split() if i not in junk))
#    sys.exit()
 
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
            texml.seek(0)
            soup_p = Soup(texml.read(), 'lxml', parse_only=par_tag)

            if len(soup_s) == 0 :
                if len(soup_p) != 0 :
                    tag = par
                    soup = soup_p
            if len(soup_s) != 0 :
                tag = sec
                soup = soup_s
            if len(soup_s) == 0 and len(soup_p) == 0 : 
                write_error(texml.name, '-1')
                return

            if size == 'split' :
                print make_sec_files(dest_path, article, soup, tag)
            if size == 'full' :
                print make_art_file(dest_path, article, soup)

        texml.closed

    except IOError :
        print in_file,' not found'
        return 


def write_error(file_name, size) :
    try :
        with io.open(error_file, 'a', encoding='utf8') as erfile :
            erfile.write('%s, %s\n' % (unicode(file_name),size))
            print '%s added to error file' % file_name
        erfile.closed
    except IOError :
        print 'file not found'
        return                                  
    return


def make_sec_files(dest_path, article, soup, tag) :
    if not os.path.exists(dest_path + '/' + article) :
        os.makedirs(dest_path + '/' + article)

    i = 0
    for sec in soup.findAll(tag) :
        dest_file = dest_path + '/' + article + '/' + article + '_' + str(i) + '.txt'
        s = xml_clean(sec)

        size = len(s.split())

        if size > 10 :
            try :
                with io.open(dest_file, 'w', encoding='utf8') as ifile :
                    ifile.write(s+'\n')
                    i += 1 
                ifile.closed
            except IOError :
                print dest_file,' not found'
                return 
        else :
            write_error(article + '_' + str(i), str(size))

    return 'article %s processed, splited in %d files' % (article, i)


def make_art_file(dest_path, article, soup) :    
    dest_file = dest_path + '/' + article + '.txt'
    s = xml_clean(soup)

    size = len(s.split())

    if size > 10 :
        try :
            with io.open(dest_file, 'w', encoding='utf8') as ifile :
                ifile.write(s+'\n')
            ifile.closed
        except IOError :
            print dest_file,' not found'
            return
        return 'article %s processed' % article
    else : 
        write_error(article, str(size))

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

    if os.path.exists(error_file) :
        os.remove(error_file)
 
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
