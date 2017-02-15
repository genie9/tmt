from bs4 import BeautifulSoup as Soup 
from bs4 import SoupStrainer as Strain
from nltk.stem import SnowballStemmer
import re

stemmer = SnowballStemmer('english')

title_list = ['#file,article_title']
a_list = []
i = 0
label = '/data/pulp/to_mallet/secs/'
xml = '/data/mallet_tests/arXiv_cs_inone/'
#art_title = ''
#text = ''
with open('/data/pulp/support/section_titles.txt') as t_file :
    for line in t_file :
        instance,title = line.split(',')
        print line
        if title.lower().find('intro') != -1 :
            with open(xml+instance.split('_')[0]+'.xml') as xml_file :
                soup = Soup(xml_file.read(), 'lxml', parse_only=Strain('title'))
                art_title = stemmer.stem((re.sub('[^a-z0-9\-]', ' ', soup.find('title').text.lower())))
                title_list.append(instance.split('_')[0]+','+art_title)
                print art_title
            xml_file.closed
            with open(label+instance+'.txt') as abstr :
                text = abstr.read()
                print text
            abstr.closed
            a_list.append(instance+' '+label+' '+art_title+' '+text)
            print a_list[i]
            i += 1
t_file.closed

with open('/data/pulp/support/intros.txt', 'w') as a_file :
    a_file.write(''.join(a_list))
a_file.closed

with open('/data/pulp/support/full_titles.txt', 'w') as t_file :
    t_file.write('\n'.join(title_list))
a_file.closed
