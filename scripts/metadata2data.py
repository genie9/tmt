import xml.sax
import sys, io


arxiv_id = []
ar_id = ''

class metadata_reader(xml.sax.ContentHandler):

    def __init__(self) :
        self.content = None
        self.article = None
        self.count = 0
        self.count_a = 0

    def startElement(self, name, attrs) :
        self.content = ""

        if name == 'article' :
            print '%d/%d'%(self.count_a,self.count)

    def characters(self, c) :
        self.content = c        

    def endElement(self, name) :
        global arxiv_id, ar_id

        if name == 'article' :
            self.count += 1

        elif name == 'categories' :
           if self.content.find('cs') == 0 :
                arxiv_id.append(ar_id.replace('/',''))
                print arxiv_id[self.count_a]
                self.count_a += 1

        elif name == 'id': 
            ar_id = self.content


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
