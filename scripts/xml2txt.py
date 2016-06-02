#!/usr/bin/python

from bs4 import BeautifulSoup as Soup
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string
import sys


if len(sys.argv) != 2 :
    print '**Usage ', sys.argv[0], ': path to input file.'
    sys.exit()

soup = []

with open(sys.argv[1], 'r') as soupfile :
        soup = Soup(soupfile.read(), 'xml')
#        print soup
        [x.extract() for x in soup.findAll('Math')]

        s = soup.get_text()

        s_words = stopwords.words('english')

        stemmer = SnowballStemmer('english')

        bad_chars = set(string.digits + string.punctuation)

        s = s.lower().strip()
        s = ''.join([ i if i not in bad_chars else ' ' for i in s ])

        s = ' '.join([ i if i not in s_words else '' for i in s.split() ])

        s = ' '.join([ stemmer.stem(word) for word in s.split() ])
soupfile.closed

print s 
