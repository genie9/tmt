import random, sys, os, re
import pandas as pd
import matplotlib.pyplot as plt


class UI(object) :

    topic_100_keys = '/data/mallet_tests/from_mallet/topics_100/bigrams/full_5_100_keys.txt'
    topic_100_dist = '/data/mallet_tests/from_mallet/topics_100/bigrams/full_5_100_compostion.txt'
    comp_full = '/data/mallet_tests/from_mallet/topics_100/full_2/full2_50_compostion.txt'
    comp_sect = '/data/mallet_tests/from_mallet/topics_100/sections_2/sections2_50_compostion.txt'
    full_plot = '/data/mallet_tests/from_mallet/plots/tests/'#old/'

    def __init__(self, doc_num, doc_file) :
        self.doc_num = doc_num
        self.doc_file = doc_file
        self.files = os.listdir(self.doc_file)
        data = Data(topic_num)
    
    def pick_docs(self) :
        return (open(self.doc_file+self.files[random.randrange(len(self.files))]) for f in xrange(self.doc_num))

    def run(self) :
        docs = '\n'.join([i for i in self.pick_docs()])
        print docs
        
        while i < 20 :
            doc_num = raw_input('Enter article number: ')
            doc = Doc(doc_num, data) 
            print doc
            topic_list = doc.topics()
            print topic_list
            while true :
                if raw_input() == 'nextdoc' :
                    print docs
                    continue
                topic_num = raw_input('Enter topic number: ')
                print data.keys(topic_num)


            

class Data(object) :
    root            = '/data/mallet_tests/from_mallet/topics_'
    comp_full_path  = '/bigrams/full_5_100_compostion.txt'
    keys_full_path  = '/bigrams/full_5_100_keys.txt'
    comp_sec_path   = '/bigrams/sec_5_100_compostion.txt'
    keys_sec_path   = '/bigrams/sec_5_100_keys.txt'

    # needs at least to know number of topics and full or sections. Then can find file by it's self. Or must be some kind of a system which chooses compostion file.
    def __init__(self, topic_num) :
        self.topic_num = int(topic_num)

        self.full_comp_file = root + topic_num + comp_full_path
        self.full_keys_file = root + topic_num + keys_full_path
        self.sec_comp_file  = root + topic_num + comp_sec_path
        self.sec_keys_file  = root + topic_num + keys_sec_path

        # returns pandas Series of chosen files
        self.full_topics    = self.do_df(self.full_comp_file)
        self.sec_topics     = self.do_df(self.sec_comp_file)
        self.full_keys      = self.do_keys(self.full_keys_file)
        self.sec_keys       = self.do_keys(self.sec_keys_file)

    def do_df(self, comp_file) :
        df = pd.read_csv(comp_file, sep='\t', names=['File']+[str(i) for i in range(self.topic_num)], na_values=[''], engine='c')
        df.File= df.File.str[5:]
        df.File = df.File.str.split('/').str[-1].str[:-4]
        print 'dataframe created'
        return df

    def do_keys(self, keys_file) :     
        df = pd.read_csv(keys_file, sep='\t', names=['topic','num','keys'], engine='c')
        df.drop('num',axis=1,inplace=True)
        print 'keys created'
        return df

    

class Doc(object) :

    def __init__(self, file_num, data) :
        self.file_num = file_num
        self.data = data
        doc_dist = doc_dist(self.data.full_topics)

    # returns pandas Series of chosen file
    def doc_dist(self, df) :
        return self.df[self.file_num]

    # how to choose best topics???
    def best_topics(self, num) :
        s = choose_file(self.file_num)
        
    # 
    def doc_keys(list_topics) :
        #(for i in list_topics)


def main(argv) :
    if len(argv) != 2 :
        print '**Usage: ', argv[0], 'topic_num'
        sys.exit()
    
    ui = UI(argv[1])
    ui.run()


if __name__ == "__main__":
    main(sys.argv)

