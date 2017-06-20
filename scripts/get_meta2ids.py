import xml.sax
import sys, io, os
import re
import time, datetime
import requests


arxiv_id = []

class metadata_reader(xml.sax.ContentHandler):

    def __init__(self) :
        self.content = None
        self.article = None
        self.count = 1 

    def startElement(self, name, attrs) :
        self.content = ""

        if name == 'header' :
            if self.count%100 == 0 :
                print self.count

    def characters(self, c) :
        self.content = c        

    def endElement(self, name) :
        global arxiv_id

        if name == 'header' :
            self.count += 1

        elif name == 'identifier': 
#            print self.content
            arxiv_id.append(self.content.split(':')[-1].replace('/',''))



def download(parser, start_date, until_date, setspec, max_tries=10):
    global arxiv_id

    # Download constants
    resume_re = re.compile(r".*<resumptionToken.*?>(.*?)</resumptionToken>.*")
    url = "http://export.arxiv.org/oai2"


    params = {"verb": "ListIdentifiers", "metadataPrefix": "arXiv", 'from': start_date, 'until': until_date, 'set': setspec}

    print params
    
    failures = 0
    
    while True:
        # Send the request.
        r = requests.get(url, params)
        print r.url

        code = r.status_code
        print code

        # Asked to retry
        if code == 503:
            to = int(r.headers["retry-after"])
            print "Got 503. Retrying after {0:d} seconds.".format(to)

            time.sleep(to)
            failures += 1
            if failures >= max_tries:
                logging.warn("Failed too many times...")
                break

        elif code == 200:
            failures = 0

            # Give the response to a parser.
            content = r.text

            xml.sax.parseString(content, metadata_reader())
#            print arxiv_id
            
            # Look for a resumption token.
            token = resume_re.search(content)
            print token

            if token is None:
                break   
            token = token.groups()[0]

            # If there isn't one, we're all done.
            if token == "":
                print "All done."
                break

            print "Resumption token: {0}.".format(token)
    
            # If there is a resumption token, rebuild the request.
            params = {"verb": "ListIdentifiers", "resumptionToken": token}

            # Pause so as not to get banned.
            to = 20
            print "Sleeping for {0:d} seconds so as not to get banned.".format(to)
            time.sleep(to)

        else:
#            print  'Wha happen?'
            r.raise_for_status()


def main(argv):
    global arxiv_id
    
    if len(argv) != 5 :
        print '**Usage: {} <category> <date from> <date until> <ids file>.'.format(argv[0])
        sys.exit()
  
    arxiv_set = argv[1]
    start = datetime.datetime.strptime(argv[2], '%y%m%d').strftime('%Y-%m-%d')
    until = datetime.datetime.strptime(argv[3], '%y%m%d').strftime('%Y-%m-%d')
    ids = argv[4]

    try:
        os.makedirs(ids.rsplit('/',1)[0])
    except os.error:
        pass
    
    parser = xml.sax.make_parser()
    parser.setContentHandler(metadata_reader())
    
    download(parser, start, until, arxiv_set)

#    print 'array ',arxiv_id
    with open(ids, 'w') as f :
        f.write('\n'.join(arxiv_id))
    f.closed
    
    pass


if __name__ == "__main__":
    main(sys.argv)
