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
#from multiprocessing import Pool


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
#title_list_main = 'article,title\n'
title_list = '#article,title\n'

# errorfile
#error_file = '/data/mallet_tests/support/aaa_' + today + '_errorfiles.txt'
error_file = '/data/pulp/support/errorfiles_' + today + '.txt'

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


def xml_clean(s, stem) :
    title = do_title(s)
   
    # to find compound words uncomment below and comment other re.sub...
#    s = re.sub(r'\s+-', ' ', re.sub('[^a-z\-]', ' ', re.sub(r'-\s+', '', s.text.lower().strip())))
    s = re.sub(r'\s+-', ' ', re.sub('[^a-z]', ' ', s.text.lower().strip()))
    
    s = [ i if len(i) > 1 else '' for i in s.split() ]
    
    s = pd.Series(s)

    s = s[-s.isin(s_words)]

    non = s[-s.isin(wordz)].astype(np.object).str.cat(sep=' ')
    non = ' '.join(( i for i in non.split() if enchant_dict_us.check(i) or enchant_dict_gb.check(i) ))

    eng = s[s.isin(wordz)].astype(np.object).str.cat(sep=' ')

    s = eng+' '+non

    if stem == True :
        s = ' '.join( map(stemmer.stem, s.split()) )

    return [title,s]
    

def do_title(s) :
    title = ''
    t = s.find('title')
    if t not in [None, -1]:
        title = (re.sub('[^a-zA-Z0-9\-]', ' ', t.text))
    return title


i = 0
keep = False
def xml_open(in_file, dest_path, stem) :
    global i, today, keep
    keep = False
    text_len = 0
#    dest_path = dest_path+'/'+today
    
    print in_file
    

    def save_secs(s, sec_len, title, sec_num, text_len) :
        global title_list, keep
        
        dest_path_sec = dest_path+'/secs/'
        text_len += sec_len
        if sec_len > 10 :
            keep = True
            if not os.path.exists(dest_path_sec) :
                os.makedirs(dest_path_sec)
            dest_file = dest_path_sec+article+'_'+str(sec_num)+'.txt'

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
        print keep
    

    # opening file and extracting file ID/article
    try :
        with open(in_file, 'r') as texml :
            print 'processing ', texml
            
            s = texml.name.rfind('/')
            e = texml.name.find('.xml', s)
            article = texml.name[s+1:e]
            soup = Soup(texml.read(), 'lxml')
            print 'soup done'
        texml.closed
        
        # find main title of article    
#        title_main = do_title(soup)

        # remove math-tags
        [ x.extract() for x in soup.findAll('math')]
        
        # find abstract
        a = soup.find('abstract')
        
        # find sections
        s = soup.findAll('section') 

        # if not even a paragraph add to error
        if len(s) == 0 :
            s = soup.findAll('paragraph')
            if len(s) == 0 :
                write_error(article, '-1')
                return

        # clean sections and find corresponding titles
        secs = map(lambda sec : xml_clean(sec,stem), s)
        print 'cleaning done'
        
        # if abstract found process it separately
        if a != None:
            a = xml_clean(a,stem)
            a[0] = 'abstr'
            secs.insert(0, a)

        # save sections
        map(lambda x : save_secs(x[1], len(x[1].split()),x[0], secs.index(x), text_len), secs)       

        # FULL ARTICLE: adding main title to main title list and saving full article
        print keep
        if keep == True :
#            title_list_main += article+','+title_main+'\n'
        
            # combain full article from sections
            text = reduce(lambda x,y : x+' '+y, map(lambda x : x[1], secs))
            dest_path_full = dest_path + '/full/'
            if not os.path.exists(dest_path_full) :
                os.makedirs(dest_path_full)
            dest_file = dest_path_full + article + '.txt'
            try :
                with io.open(dest_file, 'w', encoding='utf8') as ifile :
                    ifile.write(text+'\n')
                ifile.closed
            except IOError :
                print dest_file,' not found'
                return
        else :
            write_error(article, str(text_len))
             
        print 'article %s processed, split in %d files' % (article, len(secs))
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


################################################################


def main(argv):

    if len(argv) < 3 :
        print '**Usage: ', argv[0], '<input path> <output path> [stem]'
        sys.exit()

    in_path = argv[1]
    dest_path = argv[2]
    stem = False

    if len(argv) == 4 :
        if argv[3] == 'stem' :
            stem = True
        else :
            print "**Usage:  ", argv[0], "<input path> <output path> [stem].\n\tDid u mean 'stem'?"
            sys.exit()

    if not os.path.exists(dest_path) :
        os.makedirs(dest_path)

    if dest_path[len(dest_path)-1] != '/' :
        dest_path += '/'

    map(lambda doc : xml_open(in_path+doc, dest_path, stem), os.listdir(in_path)) 

    global title_list

    with io.open('/data/pulp/support/'+'sectons'+'_'+today+'_title.txt','a', encoding='utf8') as title_file :
        title_file.write(title_list)
    title_file.closed

#    with io.open('/data/mallet_tests/support/'+'full'+'_'+today+'_doc_title.txt','a', encoding='utf8') as main_title_file :
#        main_title_file.write(title_list_main)
#    main_title_file.closed

    pass


if __name__ == "__main__":
    main(sys.argv)
