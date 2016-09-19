#from bs4 import BeautifulSoup as Soup
#from bs4 import SoupStrainer as Strain
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
#import numpy as np
#import pandas as pd
import string, re
import sys, os, io
#import enchant
#import datetime as date

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
#today =  date.date.today().strftime('%m%d%y')
#error_file = '/data/mallet_tests/aaa_' + today + '_errorfiles.txt'

# Alan's compilation of english nonbasic words
#english = open('/home/evly/tmt/english.txt')
#wordz = set(english.read().split('\n'))
#english.closed

# enchant dictionary
#enchant_dict_us = enchant.Dict('en_US')
#enchant_dict_gb = enchant.Dict('en_GB')

# nltk text processing helpers
nltk.download('stopwords')
s_words = stopwords.words('english')
stemmer = SnowballStemmer('english')

# python's charachter methods
# deprecated after taking regex sub method in use
#bad_chars = set(string.digits + string.punctuation)

# unfrequent an too frequent words
# examined from output data after first run of this script
#junk_file = open('/data/mallet_tests/junkwords3.txt')
#junk = [line.split(',')[0] for line in junk_file]
#junk_file.closed


def xml_clean(text) :

#    [ x.extract() for x in soup.findAll('math')]

#    s = soup.get_text()
    
#    s = s.lower().strip()
    
#    s = re.sub(r'-\s+', '', s)

#    s = re.sub('[^a-z]', ' ', s)
    
#    s = ''.join([ i if i not in bad_chars else ' ' for i in s ]) 

#    s = ' '.join(( i if i not in s_words else '' for i in s.split() ))

#    s = ' '.join(( i if len(i) > 2 else '' for i in s.split() ))
    
#    s = ' '.join(( i for i in s.split() if enchant_dict_us.check(i) or enchant_dict_gb.check(i) or i in wordz ))

    s = ' '.join(( stemmer.stem(i) for i in s.split() ))

#    s = ' '.join(( i for i in s.split() if i not in junk))
 
    return s

i = 0
def txt_clean(in_file, doc, dest_path) :
    global i
    i += 1
    try :   
        with open(in_file+doc, 'r') as txt :
            print 'processing ', txt, ', output file :', doc
            
            s = ' '.join(( stemmer.stem(i) for i in txt.read().split() ))
            
            dest_file = dest_path + doc

            with io.open(dest_file, 'w', encoding='utf8') as clean_txt :
                print 'saving to ', clean_txt.name
                clean_txt.write(s+'\n')
            clean_txt.closed

            print '%d   article %s processed' % (i,doc)
        txt.closed
    
    except IOError :
        print in_file,' not found'
        return 


################################################################


def main(argv):
    
    if len(argv) != 3 :
        print '**Usage: ', argv[0], '<input path> <output path>'
        sys.exit()
    
    in_path = argv[1]
    dest_path = argv[2]

    if not os.path.exists(dest_path) :
        os.makedirs(dest_path)

   
    if dest_path[len(dest_path)-1] != '/' :
        dest_path += '/'

    map(lambda x : txt_clean(in_path, x, dest_path), os.listdir(in_path))
    
    pass


if __name__ == "__main__":
    main(sys.argv)
