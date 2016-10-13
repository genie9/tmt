import random, sys, os, re
import pandas as pd
import matplotlib.pyplot as plt


class UI(object) :

    topic_100_keys = '/data/mallet_tests/from_mallet/topics_100/bigrams/full_5_100_keys.txt'
    topic_100_dist = '/data/mallet_tests/from_mallet/topics_100/bigrams/full_5_100_compostion.txt'
    comp_full = '/data/mallet_tests/from_mallet/topics_100/full_2/full2_50_compostion.txt'
    comp_sect = '/data/mallet_tests/from_mallet/topics_100/sections_2/sections2_50_compostion.txt'
    full_plot = '/data/mallet_tests/from_mallet/plots/tests/'#old/'

    def __init__(self, doc_file, n_docs, topic_num, n_topics) :
        self.n_docs = int(n_docs)
        self.doc_file = doc_file
        self.files = os.listdir(self.doc_file)
        self.data = Data(topic_num)
        self.n_topics = int(n_topics)
    
    def helpme(self) :
        print '''Use commands:
    help    - prints this message,
    pickdoc - lets u choose document and shows it's section's IDs,
    docs    - prints documents under examination,
    secs    - prints sections of curent doc,
    picksec - lets u choose section file,
    exit    - end program
     '''
    
    def pick_docs(self) :
        return (open(self.doc_file+self.files[random.randrange(len(self.files))]) for f in xrange(self.n_docs))

    def nextdoc(self) :        
        doc_num = raw_input('Enter article number: ')
        doc = Doc(doc_num, self.data) 
            
        print doc.doc.File.tolist()
        secs = doc.secs.File.tolist()
        print secs
        return [doc,secs]

    def nextsec(self) :        
        sec_num = raw_input('Enter section number: ')
        sec = doc.secs[](doc_num, self.data) 
            
        print doc.doc.File.tolist()
        secs = doc.secs.File.tolist()
        print secs
        return [doc,secs]

    def run(self) :
        docs = '\n'.join([i.name for i in self.pick_docs()])
        print docs
       
        i = 0 
        doc = ''
        help()
        while True :
            command = raw_input('what to do?') 

            if command == 'help' : helpme(); break
            elif command == 'docs' : print docs
            elif command == 'pickdoc' :  doc = nextdoc()[0];
            elif command == 'secs' :
                if doc == '' :
                    print 'document not selected'
                    break
                print ['%s %s\n'%(i,doc.sect_title(i)) for i in doc[1]]
            elif command == 'picksec' : 
            elif command == 'exit' : sys.exit();
            elif command == '' : break

            
            doc_num = raw_input('Enter article number: ')
            doc = Doc(doc_num, self.data) 
            
            print doc.doc.File.tolist()
            print doc.secs.File.tolist()

            topic_list = doc.best_topics(self.n_topics)
            print 'top %d topics are '%self.n_topics, topic_list
            while True :
                if raw_input() == 'nextdoc' :
                    print docs
                    break
                topic_num = int(raw_input('Enter topic number: '))
                print self.data.full_topic_keys(topic_num)
            i += 1

            

class Data(object) :
    root            = '/data/mallet_tests/from_mallet/topics_'
    comp_full_path  = '/bigrams/full_5_100_compostion.txt'
    keys_full_path  = '/bigrams/full_5_100_keys.txt'
    comp_sec_path   = '/bigrams/sec_5_100_compostion.txt'
    keys_sec_path   = '/bigrams/sec_5_100_keys.txt'
    sec_title_file  = '/data/mallet_tests/support/sect_100316_doc_title.txt'


    # needs at least to know number of topics. Then can find file by it's self. 
    # Or must be some kind of a system which chooses compostion file.
    def __init__(self, topic_num) :
        self.topic_num = int(topic_num)

        self.full_comp_file = self.root + topic_num + self.comp_full_path
        self.full_keys_file = self.root + topic_num + self.keys_full_path
        self.sec_comp_file  = self.root + topic_num + self.comp_sec_path
        self.sec_keys_file  = self.root + topic_num + self.keys_sec_path

        # returns pandas dataframes of chosen mallet compostion files
        self.full_topics    = self.do_df(self.full_comp_file)
        self.sec_topics     = self.do_df(self.sec_comp_file)
        # returns pandas dataframes of chosen mallet keys files
        self.full_keys      = self.do_keys(self.full_keys_file)
        self.sec_keys       = self.do_keys(self.sec_keys_file)

        # returns pandas dataframe of all documents sections titles
        self.titles         = self.sec_titles()

    def do_df(self, comp_file) :
        df = pd.read_csv(comp_file, sep='\t', names=['File']+[str(i) for i in range(self.topic_num)])
        df.File = df.File.str[5:]
        df.File = df.File.str.split('/').str[-1].str[:-4]
        print 'dataframe created'
        return df

    def do_keys(self, keys_file) :     
        df = pd.read_csv(keys_file, sep='\t', names=['topic','num','key_w'], engine='c',dtype={'key_w':object})
        df.drop('num',axis=1,inplace=True)
        print 'keys created'
        return df
    # 
    def full_topic_keys(self, topic_list) :
        if type(topic_list) != list :
            topic_list = [topic_list]
        k = self.full_keys
        return [k[k['topic'].isin(topic_list)].get_value(topic,'key_w') for topic in topic_list]

    # 
    def sec_topic_keys(self, topic_list) :
        #(for i in list_topics)
        k = self.sec_keys
        return k[k['topic'].isin(topic_list)]
    
    def sec_titles(self) :
        df = pd.read_csv(self.sec_title_file, sep=',', names=['File','Title'])
        return df

    
#
#    def full_topic_key(topic) :
#        #(for i in list_topics)
#        k = self.full_keys
#        return k[k['topic']==topic]
#
#    # 
#    def sec_topic_key(topic) :
#        #(for i in list_topics)
#        k = self.sec_keys
#        return k[k['topic']==topic]

    

class Doc(object) :
    
    def __init__(self, file_num, data) :
        self.file_num = file_num
        sec_pat = re.compile('^%s_'%file_num)
        full_pat = re.compile('^%s$'%file_num)

        self.data = data
        
        # returns pandas dataframe over chosen file
        self.doc = self.doc_dist(self.data.full_topics, full_pat)
        # returns pandas dataframe over chosen file's sections 
        self.secs = self.doc_dist(self.data.sec_topics, sec_pat)
        
        
    # returns pandas dataframe of chosen file/files
    def doc_dist(self, df, pat) : 
        return df[df.File.str.match(pat)==True]

    def get_topics(self, num) :
        topics = self.doc.iloc[0,1:].sort_values(ascending=False)
        topics = map(int,topics.index.values)
        return topics
    
    # how to choose best topics???
    def best_topics(self, num) :
        topics = self.doc.iloc[0,1:].sort_values(ascending=False)
        topics = map(int,topics.index.values[:num])
        return topics
        
    def get_sectitle(self, file_num) :
        t = self.data.titles
        return t[t.File==file_num].Title

    def get_plot(self, dist) :
        return 0


def main(argv) :
    if len(argv) != 5 :
        print '**Usage: ', argv[0], 'doc_file, n_docs, topic_num, n_topics'
        sys.exit()
    
    ui = UI(argv[1],argv[2],argv[3],argv[4])
    ui.run()


if __name__ == "__main__":
    main(sys.argv)

