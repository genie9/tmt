import pandas as pd
import matplotlib.pyplot as plt

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
        return [k[k['topic'].isin(topic_list)].get_value(topic,'key_w') for topic in topic_list]

    
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

    
