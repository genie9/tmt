import xml.sax
import sys, io


arx_md = []
arx_path = '/data/arXiv_Src_1504_1702/'

#<?xml version='1.0' standalone='yes'?>
#<arXivSRC>
#  <file>
#    <content_md5sum>cacbfede21d5dfef26f367ec99384546</content_md5sum>
#    <filename>src/arXiv_src_0001_001.tar</filename>
#    <first_item>astro-ph0001001</first_item>
#    <last_item>quant-ph0001119</last_item>
#    <md5sum>949ae880fbaf4649a485a8d9e07f370b</md5sum>
#    <num_items>2364</num_items>
#    <seq_num>1</seq_num>
#    <size>225605507</size>
#    <timestamp>2010-12-23 00:13:59</timestamp>
#    <yymm>0001</yymm>
#  </file>

class metadata_reader(xml.sax.ContentHandler):

    def __init__(self) :
        self.content = None
        self.File = None
        self.count = 0
        self.count_f = 0
        self.count_m = 0

    def startElement(self, name, attrs) :
        self.content = ""

#        if name == 'file' :
#            print '%d/%d'%(self.count_a,self.count)

    def characters(self, c) :
        self.content = c        

    def endElement(self, name) :
        global arx_md, arx_path

        if name == 'file' :
            self.count += 1
            arx_path = '/data/arXiv_Src_1504_1702/'
            print '%d/%d/%d\n'%(self.count_m, self.count_f,self.count)

        elif name == 'filename' :
            arx_path += self.content.split('/',1)[1]
            print arx_path
            self.count_f += 1

        elif name == 'md5sum': 
            arx_md.append(self.content+'  '+arx_path)
            print arx_md[self.count_m]
            self.count_m += 1
            

def main(argv):
    if len(argv) != 3 :
        print '**Usage ', argv[0], ': metadata file, output file.'
        sys.exit()

    parser = xml.sax.make_parser()
#    parser.satFeature(xml.sax.handler.feature_namespacs, 0)
    parser.setContentHandler(metadata_reader())
    parser.parse(argv[1])

    with open(argv[2], 'w') as a_file :
        a_file.write('\n'.join(arx_md))

    pass

if __name__ == "__main__":
    main(sys.argv)
