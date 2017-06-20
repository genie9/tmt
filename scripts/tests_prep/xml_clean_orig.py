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

today =  date.date.today().strftime('%m%d%y')

# list of article or their parts IDs and matching title
title_list = 'article,title\n'

# errorfile
error_file = '/data/mallet_tests/support/aaa_' + today + '_errorfiles.txt'

# Alan's compilation of english nonbasic words
english = open('/home/evly/tmt/english.txt')
wordz = set(english.read().split('\n'))
#df_wordz = pd.Series(list(wordz))
english.closed

# enchant dictionary
enchant_dict_us = enchant.Dict('en_US')
enchant_dict_gb = enchant.Dict('en_GB')

# nltk text processing helpers
nltk.download('stopwords')
s_words_nltk = set(stopwords.words('english'))
s_words_evly = set(['also','thus','however','therefore','about','followed','following','follows','etc','always','among','amongst'])
s_words = s_words_nltk.union(s_words_evly)
#s_words = pd.Series(list(s_words))

stemmer = SnowballStemmer('english')


def xml_clean(s, stem, opt) :
    title = ''
    if opt == 'split' :
        t = s.find('title')
        if t != None :
            title = (re.sub('[^a-zA-Z0-9\-]', ' ', t.text))
#            print title
    print type(s)
    s = s.get_text()

    s = re.sub(r'\s+-', ' ', re.sub('[^a-z\-]', ' ', re.sub(r'-\s+', '', s.lower().strip())))

    s = [ i if len(i) > 1 else '' for i in s.split() ]
    
    s = pd.Series(s)

    s = s[-s.isin(s_words)]

    non = s[-s.isin(wordz)].str.cat(sep=' ')
    non = ' '.join(( i for i in non.split() if enchant_dict_us.check(i) or enchant_dict_gb.check(i) ))

    eng = s[s.isin(wordz)].str.cat(sep=' ')

    s = eng+' '+non

    if stem == True :
        s = ' '.join( (stemmer.stem(i) for i in s.split()) )

    if opt == 'split' :
        return [title,s]
    print type(s)
    return s

i = 0
def xml_open(in_file, dest_path, opt, stem) :
    global title_list, i
    print in_file

    try :
        with open(in_file, 'r') as texml :
            s = texml.name.rfind('/')
            e = texml.name.find('.xml', s)
            article = texml.name[s+1:e]

            print 'processing ', texml, ', output file :', article

            s = Soup(texml.read(), 'lxml')

        texml.closed

        [ x.extract() for x in s.findAll('math')]

        title = ''
        t = s.find('title')
        if title != None :
            title = t.text

        soup = s.findAll('section') 

        if len(soup) == 0 :
            soup = s.findAll('paragraph')
            if len(soup) == 0 :
                write_error(article, '-1')
                return

        if opt == 'split' :
            print make_sec_files(dest_path, article, soup, stem, opt)
        if opt == 'full' :
            title_list += article+','+title+'\n'
            print make_art_file(dest_path, article, soup, stem, opt)
        
        i += 1
        print i

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


def make_sec_files(dest_path, article, soup, stem, opt) :
    if not os.path.exists(dest_path + article) :
        os.makedirs(dest_path + article)

    def save_secs(s, sec_len, title, sec_num) :
        global title_list
        dest_file = dest_path+'/'+article+'/'+article+'_'+str(sec_num)+'.txt'
        print dest_file
        if sec_len > 10 :
            title_list += article+'_'+str(sec_num)+','+title+'\n'
            try :
                with io.open(dest_file, 'w', encoding='utf8') as ifile :
                    ifile.write(s+'\n')
                ifile.closed
            except IOError :
                print dest_file,' not found'
                return
        else :
            write_error(article + '_' + str(sec_num), sec_len)

    secs = map(lambda sec : xml_clean(sec,stem,opt), soup)
    map(lambda x : save_secs(x[1], len(x[1].split()),x[0], secs.index(x)), secs)

    return 'article %s processed, splited in %d files' % (article, len(secs))


def make_art_file(dest_path, article, soup, stem, opt) :    
    dest_file = dest_path + '/' + article + '.txt'
    s = reduce(lambda x,y : x+' '+y, map(lambda sec : xml_clean(sec,stem,opt), soup))

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

    if len(argv) < 4 :
        print '**Usage: ', argv[0], ' ( <full> | <split> ) <input path> <output path> [stem]'
        sys.exit()

    opt = argv[1]
    in_path = argv[2]
    dest_path = argv[3]
    stem = False

    if opt not in ['full','split'] :
        print '**Usage: ', argv[0], ' ( <full> | <split> )!! <input path> <output path> [stem]'
        sys.exit()

    if len(argv) == 5 :
        if argv[4] == 'stem' :
            stem = True
        else :
            print "**Usage:  ", argv[0], " ( <full> | <split> ) <input path> <output path> [stem].\n\tDid u mean 'stem'?"
            sys.exit()


    if not os.path.exists(dest_path) :
        os.makedirs(dest_path)

    if dest_path[len(dest_path)-1] != '/' :
        dest_path += '/'

    map(lambda doc : xml_open(in_path+doc, dest_path, opt, stem), os.listdir(in_path)) 

    global title_file
    with open('/data/mallet_tests/support/'+opt+'_'+today+'_doc_title.txt') as title_file :
        title_file.write(title_list)
    title_file.closed

    pass


if __name__ == "__main__":
    main(sys.argv)
