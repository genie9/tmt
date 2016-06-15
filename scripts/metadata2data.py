from bs4 import BeautifulSoup as Soup
import demjson as json
import sys, os, io
from itertools import islice
import datetime


def xml_open(in_file, dest_file) :
#    size = os.path.getsize(in_file)
    try :
        with open(in_file, 'r') as meta :
            print meta

            meta.readline() 
            meta.readline() 

            parsed = ''
            j = 0
            stop = 0

            while stop == 0 :
                to_read = ''

                for i in range(0,11): 
                    to_read += meta.readline()  #list(islice(meta, i, j) )

                    if to_read == '\n' :
                        stop = 1
                        print 'break'
                        continue 

                    res = test2( Soup(str(to_read), 'xml') )

                if res[0] == 1 :
                    if stop == 1 :
                        print 'stop = 1'
                    parsed += json.encode(res[1]) + '\n'
                    j += 1
                    print 'red in ', j, ' parts'

                    if j % 1000 == 0 or stop == 1 :  
                        if stop == 1 :
                            print 'stop = 1'
                        with io.open(dest_file + '_' + str(j), 'w', encoding='utf8') as data :
                            data.write((parsed) + u"\u000A") # '\n')
                            parsed = '' 
                        data.closed
        meta.closed
    except IOError :
        print in_file/dest_file,' not found'
        return 
#    print ' splited in ', i, 'sections'


def test2(soup) :    
    cs = 0    
    if cs == 0 :
        print 'ei l√ydy'
    elif soup.find('categories') != None and soup.categories.string.find('cs') == 0 :
        cs = 1
        arxiv_id = soup.id.get_text()
#        arxiv_id = arxiv_id[len(arxiv_id)-9 : len(arxiv_id)]

#        title = soup.title.get_text()
#        author = soup.author.get_text()
        url = soup.url.get_text()

#        dated = soup.updated.get_text()
#        if dated != 'NA' :
#            dated = datetime.datetime.strptime(dated, "%Y-%m-%d")
         
#        created = soup.created.get_text()
#        created = datetime.datetime.strptime(created, "%Y-%m-%d")
        
        contents = [{'id': arxiv_id,
              #  'title': title,
              #  'author': author,
              #  'created': created,
              #  'updated': dated,
                'url': url
                 }]

#      df = df.append(contents, ignore_index=True)
        return (cs, contents)
    else : return (cs, '')


def test() :
                for record in soup.findall("article"):
                    if record.find('venue').get_text == 'arXiv Computer Science' :
                        arxiv_id = record.find('id').get_text
                        arxiv_id = arxiv_id[len(arxiv_id)-9 : len(arxiv_id)-1]

                        title = record.find('title').get_text
                        author = record.find('author').get_text
                        url = record.find('url').get_text

                        dated = record.find("updated").get_text
                        dated = datetime.datetime.strptime(dated, "%Y-%m-%d")
                         
                        created = record.find("created").get_text
                        created = datetime.datetime.strptime(created, "%Y-%m-%d")

                        contents = [{'id': arxiv_id,
                                'title': title,
                                'author': author,
                                'created': created,
                                'updated': dated,
                                'url': url
                                 }]

#                        df = df.append(contents, ignore_index=True)
                        
                        data.write(json.encode(contents) + '\n') 


def main(argv):
    if len(argv) != 3 :
        print '**Usage ', argv[0], ': metadata file, output file.'
        sys.exit()

    in_file = argv[1]
    dest_file = argv[2]

    xml_open(in_file, dest_file)
    
    pass

if __name__ == "__main__":
    main(sys.argv)
