import time
import urllib2
import datetime
from itertools import ifilter
from collections import Counter, defaultdict
import matplotlib.pylab as plt
import pandas as pd
import xml.etree.ElementTree as ET


pd.set_option('mode.chained_assignment','warn')

OAI = "{http://www.openarchives.org/OAI/2.0/}"
ARXIV = "{http://arxiv.org/OAI/arXiv/}"

def harvest():
    df = pd.DataFrame(columns=("created", "id"))
    base_url = "http://export.arxiv.org/oai2?verb=ListIdentifiers&set=cs&"
    url = (base_url +
           "from=2007-04-01&until=2015-12-31&" +
           "metadataPrefix=oai_dc")
    
    while True:
        print "fetching", url
        try:
            response = urllib2.urlopen(url)
            
        except urllib2.HTTPError, e:
            if e.code == 503:
                to = int(e.hdrs.get("retry-after", 30))
                print "Got 503. Retrying after {0:d} seconds.".format(to)

                time.sleep(to)
                continue
                
            else:
                raise
            
        xml = response.read()

        root = ET.fromstring(xml)

        for record in root.find(OAI+'ListIdentifiers').findall(OAI+"header"):
            arxiv_id = record.find(OAI+'identifier')
            dateed = info.find(ARXIV+"datestamp").text
            created = datetime.datetime.strptime(created, "%Y-%m-%d")

            # if there is more than one DOI use the first one
            # often the second one (if it exists at all) refers
            # to an eratum or similar
#            doi = info.find(ARXIV+"doi")
#            if doi is not None:
#                doi = doi.text.split()[0]
                
            contents = {'id': arxiv_id.text[4:],
                        'created': created,
                        }

            df = df.append(contents, ignore_index=True)

        # The list of articles returned by the API comes in chunks of
        # 1000 articles. The presence of a resumptionToken tells us that
        # there is more to be fetched.
        token = root.find(OAI+'ListIdentifiers').find(OAI+"resumptionToken")
        if token is None or token.text is None:
            break

        else:
            url = base_url + "resumptionToken=%s"%(token.text)
            
    return df

def main(argv):
    if len(argv) != 2 :
        print '**Usage ', argv[0], ': metadata file.'
        sys.exit()

    in_path = argv[1]
    dest_path = argv[2]

    if not os.path.exists(dest_path) :
        os.makedirs(dest_path)

    if dest_path[len(dest_path)-1] != '/' :
        dest_path += '/'
    
    for f in os.listdir(in_path) :
        xml_open(in_path+f, dest_path)
    
    pass

if __name__ == "__main__":
    main(sys.argv)

