import random, sys, os, re
import pandas as pd
import matplotlib.pyplot as plt
import data

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

    def get_doc_file(self) :
        return self.doc.File.tolist()

    def get_secs_files(self) :
        return self.secs.File.values

    def get_doc_topics(self, num) :
        topics = self.doc.iloc[0,1:].sort_values(ascending=False)
        topics = map(int,topics.index.values[:num])
        return topics
    
#    # how to choose best topics???
#    def get_best_doc_topics(self, num) :
#        topics = self.doc.iloc[0,1:].sort_values(ascending=False)
#        topics = map(int,topics.index.values[:num])
#        return topics
        
    def get_sec_title(self, file_num) :
        t = self.data.titles
        return str(t[t.File==file_num].Title.values).strip('[]')

    def get_sec_topics(self, sec, num) :
        topics = self.secs[self.secs.File==sec].iloc[0,1:].sort_values(ascending=False)
        topics = map(int,topics.index.values[:num])
        return topics
    
#    def get_best_sec_topics(self, num) :
#        topics = self.secs.iloc[0,1:].sort_values(ascending=False)
#        topics = map(int,topics.index.values[:num])
#        return topics
        
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

