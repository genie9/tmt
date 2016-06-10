from bs4 import BeautifulSoup as Soup
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string, re
import sys, os, io
#from os import listdir


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



def xml_open(in_file, dest_file) :
    #print in_file
    try :
        with open(in_file, 'r') as meta :
            s = meta.name.rfind('/')
            e = meta.name.find('.', s)
           # filename = dest_path + meta.name[s+1:e] + '.txt'

            print meta
            
            meta_text = meta.read()
            print len(meta_text)
            
           # i = 0
           # istart = 0
           # iend = 0
           # secs_text = ''

           # wend = '</section>' #sys.argv[3]
           # wend_len = len(wend)
            
            with io.open(dest_file, 'w', encoding='utf8') as data :
#                while True:
#                    istart = meta_text.find('<section ', iend)
#                    if istart == -1 : break

#                    iend = meta_text.find(wend, istart)

 #                   if iend != -1 :
 #                       meta.seek(istart)
      
                        soup = Soup(meta.read(iend + wend_len - istart), 'xml')

        for record in root.find(OAI+'ListIdentifiers').findall(OAI+"header"):
             arxiv_id = record.find(OAI+'identifier')
             dateed = info.find(ARXIV+"datestamp").text
             created = datetime.datetime.strptime(created, "%Y-%m-%d")
 
             contents = {'id': arxiv_id.text[4:],
                         'created': created,
                         }
 
             df = df.append(contents, ignore_index=True)
                        
                       # data += xml_clean(soup)
                       # secs.write(secs_text + '\n\n\n')
                        
                       # i += 1 
                       # meta.seek(iend)
            data.closed
        meta.closed
    except IOError :
        print in_file/dest_file,' not found'
        return 
    print ' splited in ', i, 'sections'
    
 
#         root = ET.fromstring(xml)
 


def main(argv):
    if len(argv) != 3 :
        print '**Usage ', argv[0], ': metadata file, output file.'
        sys.exit()

    in_file = argv[1]
    dest_file = argv[2]

    xml_open(in_path, dest_file)
    
    pass

if __name__ == "__main__":
    main(sys.argv)
