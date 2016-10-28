import random, sys, os, re
import pandas as pd
import matplotlib.pyplot as plt
import data
import document as d


class UI(object) :

    topic_100_keys = '/data/mallet_tests/from_mallet/topics_100/bigrams/full_5_100_keys.txt'
    topic_100_dist = '/data/mallet_tests/from_mallet/topics_100/bigrams/full_5_100_compostion.txt'
    comp_full = '/data/mallet_tests/from_mallet/topics_100/full_2/full2_50_compostion.txt'
    comp_sect = '/data/mallet_tests/from_mallet/topics_100/sections_2/sections2_50_compostion.txt'
    full_plot = '/data/mallet_tests/from_mallet/plots/tests/'#old/'

    def __init__(self, doc_file, n_docs, topic_num, n_topics) :
        # for choosing files for testing
        self.n_docs = int(n_docs)
        self.doc_file = doc_file
        self.files = os.listdir(self.doc_file)

        # actual data
        self.data = data.Data(topic_num)
        self.n_topics = int(n_topics)
    
    def helpme(self) :
        print '''Use commands:
    help    - print this message,
    pickdoc - choose document and show it's section's IDs,
    docs    - print documents under examination,
    secs    - print sections of curent chosen document,
    topics  - show topics of current document and choose one,
    dockeys - show top words from current document's topic
    picksec - choose section file,
    sectop  - choose topics of current section,
    seckeys - show top words from current section's topic
    exit    - end program
     '''
    
    def pick_docs(self) :
        return (open(self.doc_file+self.files[random.randrange(len(self.files))]) for f in xrange(self.n_docs))

    def nextdoc(self,doc_num) :        
        doc = d.Doc(doc_num, self.data) 
        return doc

#NOT WORKING!!!
#    def nextsec(self, doc,sec_num) :        
#        sec = doc.get_sec(sec_num)
#        title = doc.sec_title(sec)
#        return [sec,title]


    def run(self) :
        docs = '\n'.join([i.name for i in self.pick_docs()])
        print docs
       
        doc = ''
        sec_num = ''
        self.helpme()
        while True :
            command = raw_input('what to do?') 

            if command == 'help' : 
                self.helpme()
                continue
            elif command == 'docs' : 
                print docs
                continue
            elif command == 'pickdoc' :  
                doc_num = raw_input('Enter article number: ')
                doc = self.nextdoc(doc_num)
                print doc.get_doc_file()
                print doc.get_secs_files()
                continue
            elif command == 'secs' :
                if doc == '' :
                    print 'document not selected'
                    continue                  
                print '\n'.join(['%s %s'%(i, doc.get_sec_title(i)) for i in doc.get_secs_files()])
                continue
            elif command == 'picksec' : 
                sec_num = raw_input('Enter section number: ')
#                self.nextsec(doc,sec_num)
                print '%s %s'%(sec_num, doc.get_sec_title(sec_num))
                continue
            elif command == 'topics' : 
                doc_topic_list = doc.get_doc_topics(self.n_topics)
                print 'top %d topics are '%self.n_topics, doc_topic_list
                continue
            elif command == 'sectop' : 
                sec_topic_list = doc.get_sec_topics(sec_num, self.n_topics)
                print 'top %d topics are '%self.n_topics, sec_topic_list
                continue
            elif command == 'dockeys' : 
                topic_num = int(raw_input('Enter topic number: '))
                print 'top words for topic %d are: '%topic_num, self.data.full_topic_keys(topic_num)
                continue
            elif command == 'seckeys' : 
                topic_num = int(raw_input('Enter topic number: '))
                print 'top words for topic %d are: '%topic_num, self.data.sec_topic_keys(topic_num)
                continue
            elif command == 'exit' : sys.exit();
            else : continue          
            
            while True :
                if raw_input() == 'nextdoc' :
                    print docs
                    break

            


def main(argv) :
    if len(argv) != 5 :
        print '**Usage: ', argv[0], 'doc_file, n_docs, topic_num, n_topics'
        sys.exit()
    
    ui = UI(argv[1],argv[2],argv[3],argv[4])
    ui.run()


if __name__ == "__main__":
    main(sys.argv)

