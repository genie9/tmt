import xml.etree.ElementTree as ET
import xml.sax
import sys, io
import xml.dom.minidom


found = []
articles = None
doc_list = None
xml_article = None

class metadata_reader(xml.sax.ContentHandler):
    global articles, xml_article
    article = None
    to_tree = False

    def __init__(self) :
        self.content = None
        self.article = None
        self.count   = 0
        self.a_count = 0

    def startElement(self, name, attrs) :

        self.content = ""

        if name == 'article' :
            self.a_count += 1
            self.article = add_xml_el(articles,name)

    def characters(self, c) :
        self.content = c        

    def endElement(self, name) :
        if name == 'article' :
            if self.to_tree :
                self.count += 1
            else : 
                articles.remove(self.article)
                
            print '%d/%d'%(self.a_count,self.count)
        
        elif name == 'id'       :
            if check_id(self.content) : 
                add_xml_el(self.article,name,self.content)
                self.to_tree = True
            else: 
                self.to_tree = False
        elif name == 'title'    : 
            if self.to_tree: add_xml_el(self.article,name,self.content)
        elif name == 'author'   : 
            if self.to_tree: add_xml_el(self.article,name,self.content)
        elif name == 'abstract' : 
            if self.to_tree: add_xml_el(self.article,name,self.content)
        elif name == 'venue'    : 
            if self.to_tree: add_xml_el(self.article,name,self.content)
        elif name == 'url'      : 
            if self.to_tree: add_xml_el(self.article,name,self.content)
        elif name == 'categories':
            if self.to_tree: add_xml_el(self.article,name,self.content)
        elif name == 'created'  : 
            if self.to_tree: add_xml_el(self.article,name,self.content)
        elif name == 'updated'  : 
            if self.to_tree: add_xml_el(self.article,name,self.content)
        
        else : pass


def add_xml_el(root, el, text='') :
    element = ET.SubElement(root, el)
    element.text = text
    return element


def check_id(arxv) :
    global found, doc_list

    if '/' in arxv :
        arxv = arxv.replace('/', '')
    if arxv in doc_list :
        found.append(arxv)
        return True
    return False      
    
    
def write(f, data) :
    with open(f, 'a') as new_meta :    
        new_meta.write(data)
    new_meta.closed


def main(argv):
    global articles, doc_list, found
 
    if len(argv) != 4 :
        print '**Usage ', argv[0], ': metadata file, output file, doc list file'
        sys.exit()

    new_arxiv = argv[2]

    articles = ET.Element("articles")
    
    with open(argv[3], 'r') as docs :
        doc_list = [i.split(',')[0] for i in docs.read().split('\n')]
    docs.closed

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    parser.setContentHandler(metadata_reader())
    parser.parse(argv[1])

    tree = ET.ElementTree(articles)
    tree.write(new_arxiv,encoding='UTF-8',xml_declaration=True)
    
    m = xml.dom.minidom.parse(new_arxiv)

    with open(new_arxiv.split('.xml')[0]+'_pretty.xml', 'w') as new_meta :
        new_meta.write(m.toprettyxml(indent='\t').encode('UTF-8'))
    new_meta.closed
   
    print 'done'
    
    print [i for i in doc_list if i not in found] 
    
    pass


if __name__ == "__main__":
    main(sys.argv)
