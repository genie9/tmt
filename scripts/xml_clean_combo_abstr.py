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
# Files are separeted between tags and saved in individual files
# to destination path named by original article id and incremental count as txt files.


#####################################################
###                 global stuff                  ###
#####################################################

today =  date.date.today().strftime('%m%d%y')

# destination files
dest_path_sec = ''
dest_path_full = ''

# list of articles' sections ids and their titiles
title_list = []
# temporary title list per article to track duplicates
tmp_titles = []
# uncomment to save article titles
#title_list_main = 'article,title\n'

# list of error texts
err_list = []

# Alan's compilation of english nonbasic words
english = open('english.txt')
wordz = set(english.read().split('\n'))
#df_wordz = pd.Series(list(wordz))
english.closed

# enchant dictionary
enchant_dict_us = enchant.Dict('en_US')
enchant_dict_gb = enchant.Dict('en_GB')

# nltk text processing helpers
nltk.download('stopwords')
s_words_nltk = set(stopwords.words('english'))
# put here words to extend stopword list
s_words_genie = set(['also','thus','however','therefore','about','followed','following','follows','etc','always','among','amongst'])
s_words = s_words_nltk.union(s_words_genie)
#s_words = pd.Series(list(s_words))

stemmer = SnowballStemmer('english')

# helpers: 
# keeps track of number of written articles
i = 0
# holds information of article's cleaned sections cumulative word count,
# used to check if article should be saved
text_len = 0
# minimum length of section to keep
min_len = 0


def xml_clean(s, stem) :
    title = do_title(s)
    if title == 0: 
        print 'Duplicate found, section will not be recorded'
        return ['','']

    # to find compound words uncomment below and comment other re.sub...
#    s = re.sub(r'\s+-', ' ', re.sub('[^a-z\-]', ' ', re.sub(r'-\s+', '', s.text.lower().strip())))

    s = re.sub(r'\s+-', ' ', re.sub('[^a-z]', ' ', s.text.lower().strip()))
   
    # keep words with legth over 1 char
    s = [ i if len(i) > 1 else '' for i in s.split() ]
    
    s = pd.Series(s)
    s = s[-s.isin(s_words)]

    non = s[-s.isin(wordz)].astype(np.object).str.cat(sep=' ')
    non = ' '.join(( i for i in non.split() if enchant_dict_us.check(i) \
            or enchant_dict_gb.check(i) ))
    eng = s[s.isin(wordz)].astype(np.object).str.cat(sep=' ')
    s = eng+' '+non

    if stem == 'stem' :
        s = ' '.join( map(stemmer.stem, s.split()) )
    
    return [title,s]
    

def do_title(s) :
    global tmp_titles

    t = s.find('title')

    if t in [None, -1] :
         return ''

    title = (re.sub('[^a-zA-Z0-9\-]', ' ', t.text))
    
    # check for duplicate e.g. from other versions of document
    if t.text.lower() in tmp_titles :
        print 'possible duplicate {}'.format(title.lower())
#        print 'sections titles {}'.format(tmp_titles)
        return 0
    
    if t.text != '' :
        tmp_titles.append(t.text.lower())

    return title


def xml_open(in_file, stem) :
    global i, text_len, tmp_titles

    tmp_titles = []
    text_len = 0

    # opening file and extracting file's ID/article
    try :
        with open(in_file, 'r') as texml :
            print 'processing ', texml           
            article = texml.name.split('/')[-1].split('.xml')[0]
            soup = Soup(texml.read(), 'lxml')
            print '%s soup done'%article
        texml.closed
    except IOError :
        print in_file,' not found'
        return 
    
    # find main title of article    
    title_main = do_title(soup)

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
        a[0] = 'Abstract'
        secs.insert(0, a)

    # save sections
    map(lambda x : save_secs(x[1], len(x[1].split()), x[0], secs.index(x), article), secs)       

    # FULL ARTICLE: (adding main title to main title list and) saving full article
    if text_len >= min_len :

        # uncomment to save article titles
#        global title_list_main        
#        title_list_main += article+','+title_main+'\n'
    
        # combain full article from sections
        text = title_main + reduce(lambda x,y : x+' '+y, map(lambda x : x[1], secs))

        dest_file = dest_path_full + article + '.txt'

        try :
            with io.open(dest_file, 'w', encoding='utf8') as ifile :
                ifile.write(text)
            ifile.closed
        except IOError :
            print dest_file,' not found'
            return
    else :
        write_error(article, str(text_len))
         
    print 'article %s processed, split in %d files' % (article, len(secs))
    i += 1
    print i


def save_secs(s, sec_len, title, sec_num, article) :
    global title_list, tmp_titles, text_len, dest_path_sec
    
    len_lim = min_len
    if title == 'Abstract' : 
        len_lim = 10
    if sec_len >= len_lim :
        text_len += sec_len
        dest_file = dest_path_sec+article+'_'+str(sec_num)+'.txt'
        title_list.append(article+'_'+str(sec_num)+','+title)
#        title_list += article+'_'+str(sec_num)+','+title+'\n'

        try :
            with io.open(dest_file, 'w', encoding='utf8') as ifile :
                ifile.write(s)
            ifile.closed
        except IOError :
            print dest_file,' not found'
            return
    else :
        write_error(article + '_' + str(sec_num), sec_len)


def write_error(file_name, size) :
    global err_list
    err_list.append(file_name+','+str(size))
    print '{0} added to error list, word count {1}'.format(file_name,size)
    return


################################################################


def main(argv):
    global dest_path_sec, dest_path_full, min_len

    if len(argv) != 4 :
        print '**Usage: ', argv[0], ', <work folder> <min length> <stem|nonstem>'
        sys.exit()

    root = argv[1]
    min_len = int(argv[2])
    stem = argv[3]

    in_path = '{}arXiv_raw/'.format(root)
    dest_path = '{0}preproc_{1}_{2}/'.format(root,stem,min_len)
    titles = '{0}section_titles_{1}.txt'.format(root,min_len)
    errors = '{0}errorfiles_{1}_{2}.txt'.format(root,stem,min_len)

#    if in_path[-1] != '/' :
#        in_path += '/'
#    
#    if not os.path.exists(dest_path) :
#        os.makedirs(dest_path)
#
#    if dest_path[-1] != '/' :
#        dest_path += '/'

    dest_path_sec = '{0}sect/'.format(dest_path, stem, min_len)

    if not os.path.exists(dest_path_sec) :
        os.makedirs(dest_path_sec)

    dest_path_full = '{0}full/'.format(dest_path, stem, min_len)
    
    if not os.path.exists(dest_path_full) :
        os.makedirs(dest_path_full)
   
    raw = os.listdir(in_path)
    map(lambda doc : xml_open(in_path+doc, stem), raw) 
    
    with io.open(titles,'w', encoding='UTF-8') as f :
        f.write('\n'.join(title_list))
    f.closed

    with io.open(errors, 'w', encoding='utf8') as erfile :
        erfile.write(unicode('\n'.join(err_list)))
    erfile.closed

    # uncomment to save article titles
#    with io.open('data/main_titles_{}.txt'.format{min_len},'w', encoding='utf8') as f :
#        f.write(title_list_main)
#    f.closed
    
    print 'processed {}/{} articles'.format(raw,i)
    pass


if __name__ == "__main__":
    main(sys.argv)
