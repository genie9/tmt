from bs4 import BeautifulSoup as Soup
import json
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

            parsed = [] 
            j = 0
            k = 0
            stop = 0

            while stop == 0 :
                to_read = ''

                for i in range(0,11): 
                    tmp = meta.readline()

                    if tmp == '' or tmp == '\n' :
                        stop = 1
                        print 'must end after that'
                        break

                    to_read += tmp  #list(islice(meta, i, j) )


                res = test2( Soup(str(to_read), 'xml') )

                if res == 0 :
                    k += 1
                    print 'stop = ', stop
                    print res, 'bad part #', k
                
                elif res[0] == 1 or stop == 1 :
                    if stop == 1 and parsed != [] : 
                        write_dest(dest_file, j, parsed) 
                        print 'vika stop'
                        return
                    parsed.append(res[1])
                    j += 1
                    print 'red in ', j, ' parts'

                    if j % 1000 == 0 : 
                        write_dest(dest_file, j, parsed) 
                        parsed = []
                        print 'empty?? ', parsed
        meta.closed
    except IOError :
        print in_file, ' not found'
        return 
    

def  write_dest(dest_file, j, parsed) :
    try :
        with io.open(dest_file + '_' + str(j), 'w', encoding='utf8') as data :
            data.write(unicode(json.dumps(parsed, ensure_ascii=False)))  #+ u"\u000A") # '\n')
        data.closed
    except IOError :
        print dest_file,' not found'
        return 



def test2(soup) :    
    cs = 0    
    if soup.find('categories') != None and soup.categories.string.find('cs') == 0 :
        cs = 1
        arxiv_id = soup.id.get_text().replace('/', '')
        url = soup.url.get_text()
        
        contents = {
            'id': arxiv_id,
            'url': url
        }

        return (cs, contents)
    else : return 0


def test() :
    cs = 0    
    if soup.find('categories') != None and soup.categories.string.find('cs') == 0 :
        cs = 1
        arxiv_id = soup.id.get_text().replace('/', '')
        arxiv_id = arxiv_id[len(arxiv_id)-9 : len(arxiv_id)]

        title = soup.title.get_text()
        author = soup.author.get_text()
        url = soup.url.get_text()

        dated = soup.updated.get_text()
        if dated != 'NA' :
            dated = datetime.datetime.strptime(dated, "%Y-%m-%d")
         
        created = soup.created.get_text()
        created = datetime.datetime.strptime(created, "%Y-%m-%d")
        
        contents = [{'id': arxiv_id,
                'title': title,
                'author': author,
                'created': created,
                'updated': dated,
                'url': url
                 }]

#      df = df.append(contents, ignore_index=True)
        return (cs, year, contents)
    else : return 0


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
