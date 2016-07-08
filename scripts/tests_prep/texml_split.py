#!/usr/bin/pyhton

import re
import sys
import os
from bs4 import BeautifulSoup as Soup
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string


# Takes cl arguments for input file and output path.
# Divides text between '<section' and '</section' tags to separate files naming them by original file name 
# with indexing suffix and storing to destination path.
 
if len(sys.argv) != 3 :
    print '**Usage ', sys.argv[0], ': path to input file, path to output directory.'
    sys.exit()

dest_path = sys.argv[2]

if not os.path.exists(dest_path) :
    os.makedirs(dest_path)

if dest_path[len(dest_path)-1] != '/' :
    dest_path += '/'

with open(sys.argv[1], 'r') as texml :
    s = texml.name.rfind('/')
    e = texml.name.find('.', s)
    filename = texml.name[s+1:e]

    print texml

    texml_text = Soup(texml.read(),'xml')
    print len(texml_text)
#    soup = Soup(soupfile.read(), 'xml')
 #   print len(soup)

    i = 0
    istart = 0
    iend = 0
    
    wend = '</section>' #sys.argv[3]
    wend_len = len(wend)
    with open(dest_path + filename + '.txt', 'w') as secs :
        while True:
            istart = texml_text.find('<section ', iend)
            if istart != -1 :
    #            print "found start"
    #            print istart
                pass
            else: break
            iend = texml_text.find(wend, istart)
            if iend != -1 :
    #            print "found end"
    #            print iend
    #            ifile = open(dest_path + filename + '_' + str(i), 'w')
                texml.seek(istart)
                secs.write(texml.read(iend + wend_len - istart) + '\n\n\n')
                i += 1 
                texml.seek(iend)
    secs.closed
texml.closed

print ' splited in ', i, 'sections'
