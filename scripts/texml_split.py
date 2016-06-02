from bs4 import BeautifulSoup as Soup
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string, re
import sys, os, io


# Takes cl arguments for input file and output path.
# Divides tex.xml-text between '<section' and '</section' tags, 
# cleans xml formating, stop words and punctuation.
# Processes with stemmer.
# Processed file is separeted between sections  with two (2) 'new lines' and
# saved to destination path with original file name and .txt extension.
#
 
def xml_clean(soup) :
    [x.extract() for x in soup.findAll('Math')]

    s = soup.get_text()

    s_words = stopwords.words('english')

    stemmer = SnowballStemmer('english')
    
    bad_chars = set(string.digits + string.punctuation)

    s = s.lower().strip()

    s = ''.join([ i if i not in bad_chars else ' ' for i in s ])

    s = ' '.join([ i if i not in s_words else '' for i in s.split() ])
 
    s = ' '.join([ stemmer.stem(word) for word in s.split() ])

    return s



def xml_open(in_file, dest_path) :

    with open(in_file, 'r') as texml :
        s = texml.name.rfind('/')
        e = texml.name.find('.', s)
        filename = dest_path + texml.name[s+1:e] + '.txt'

        print texml
        
        texml_text = texml.read()
        print len(texml_text)
        
        i = 0
        istart = 0
        iend = 0
        secs_text = ''

        wend = '</section>' #sys.argv[3]
        wend_len = len(wend)
        
        with io.open(filename, 'w', encoding='utf8') as secs :
            while True:
                istart = texml_text.find('<section ', iend)
                if istart == -1 : break

                iend = texml_text.find(wend, istart)

                if iend != -1 :
                    texml.seek(istart)
  
                    soup = Soup(texml.read(iend + wend_len - istart), 'xml')
                    secs_text += xml_clean(soup)
                    secs.write(secs_text + '\n\n\n')
                    
                    i += 1 
                    texml.seek(iend)
        secs.closed
    texml.closed

    print ' splited in ', i, 'sections'


def main(argv):
    if len(argv) != 3 :
        print '**Usage ', argv[0], ': path to input file, path to output directory.'
        sys.exit()

    dest_path = argv[2]

    if not os.path.exists(dest_path) :
        os.makedirs(dest_path)

    if dest_path[len(dest_path)-1] != '/' :
        dest_path += '/'

    xml_open(argv[1], dest_path)
    
    pass

if __name__ == "__main__":
    main(sys.argv)
