import xml.sax
import sys, io, re
from datetime import datetime
from sys import stderr, exit

arxiv_id = []
ar_id = ''
cs = False
categ_re = re.compile(r"(^|.*?,)cs.*?")

class metadata_reader(xml.sax.ContentHandler):

    def __init__(self) :
        self.content = None
        self.article = None
        self.count = 0
        self.count_a = 0
        # to find exact entries in meta file
        self.lastdate = datetime(2014,04,30).date()

    def startElement(self, name, attrs) :
        self.content = ""

#        if name == 'article' :
#            print '%d/%d'%(self.count_a,self.count)

    def characters(self, c) :
        self.content = c        

    def endElement(self, name) :
        global arxiv_id, ar_id, cs, categ_re

        if name == 'articles' :
            print '%d/%d'%(self.count_a,self.count)
             
        if name == 'article' :
            self.count += 1
            cs = False

        elif name == 'id': 
            ar_id = self.content
        
        elif name == 'categories' :
            # matches categories which start with cs tag
            if self.content.find('cs') == 0 :

            # matches all cs tags in categories, gives more results
#            if categ_re.search(self.content) != None :
               print self.content
               cs = True

        elif name == 'created' :
            try :
                date = datetime.strptime(self.content, '%Y-%m-%d').date()
#                print date
            except ValueError :
                print >> stderr, 'wrong date ',self.content
                date = self.lastdate

            if date <= self.lastdate and cs == True :
                arxiv_id.append(ar_id.replace('/',''))
                print arxiv_id[self.count_a]
                self.count_a += 1


def main(argv):
    if len(argv) != 3 :
        print '**Usage ', argv[0], ': metadata file, output file.'
        sys.exit()

    parser = xml.sax.make_parser()
#    parser.satFeature(xml.sax.handler.feature_namespacs, 0)
    parser.setContentHandler(metadata_reader())
    parser.parse(argv[1])

    with open(argv[2], 'w') as a_file :
        a_file.write('\n'.join(arxiv_id))

    pass

if __name__ == "__main__":
    main(sys.argv)
