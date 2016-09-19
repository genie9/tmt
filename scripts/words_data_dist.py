import string, sys, os
import pandas as p
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

article_files = '/data/mallet_tests/to_mallet/full4/'
words2topic_file = '/data/mallet_tests/from_mallet/test/full4/full_50_wordcounts.txt'
word_dist_file = '/data/mallet_tests/word_dist.csv'
junkwordz_file = '/data/mallet_tests/junkwords3.txt'
wordz_dist_plot = '/data/mallet_tests/wordz.png'
wordz2file_plot = '/data/mallet_tests/summz.png'

# plotting distribution of words through all data
# junk word list deprecated

def word_sum_dict(words2topic_file) :
    to_file = {}

    with open(words2topic_file, 'r') as w_file :
        # calculate all appereance of each word
        for line in w_file: 
            word =  line.split()[1]
            pairs = (i for i in line.split()[2:])
            summa = sum([int(string.split(n, ':')[1]) for n in pairs])
            to_file[word] = summa
    w_file.closed

    return to_file

def do_texts(article_files) :
#    files = (open(i) for i in os.listdir(article_files))
    return (open(os.path.join(article_files,doc)).read() for doc in os.listdir(article_files))

def do_sets(texts) :
    return (sorted(set(text.split())) for text in texts)

def do_series(sets, cols) :
    return (cols.isin(i) for i in sets)

def plot_dist(series, to_file,kind) :
    # plot word distribution
    plt.xticks([i*100 for i in xrange(len(series))], series)
    mpl.ticker.AutoMinorLocator(n=None)
    plt.tick_params(labelright=True)
    
    series.plot(figsize=(128,16),kind=kind,fontsize=9,rot=90,grid=True,logy=True)
    plt.savefig(to_file)
    return 'plot created to destination %s' % to_file

word_dict = word_sum_dict(words2topic_file)

# dataframe for word appereance in file true/false
cols = p.Series(sorted(word_dict.keys()))
print cols

df_summs = p.DataFrame(do_series(do_sets(do_texts(article_files)),cols),columns=cols)
print df_summs

df_summs = 100*df_summs/df_summs.sum()#axis=0)

#    df_summs = df_summs.apply(lambda x : x*100/len(df.index))
df_summs.sort_values(inplace=True)
print df_summs
    
plot_dist(df_summs, wordz2file_plot,bar)
    
sys.exit()

# sort appereance in increasing order and save to file 
ser = p.Series(word_dict)
ser = ser.sort_values()
#    print ser 
ser.to_csv(word_dist_file)

# find words which appear under 6 times (testing) and save to file
#junk = [key for key, val in word_dict.items() if val < 6]
ser_head = ser.groupby(ser.between(1,5)).get_group(True)    
print ser_head
ser_head.to_csv(junkwordz_file)
plot_dist(ser, wordz_dist_plot,line)

    

#ser = p.Series.from_csv('/data/mallet_tests/word_dist.csv')
#ser = ser.sort_values()
#print ser
#plt.xticks([i*100 for i in xrange(len(ser))], ser)
#mpl.ticker.AutoMinorLocator(n=None)
#plt.tick_params(labelright=True)
#ser.plot(figsize=(128,16),fontsize=9,rot=90,grid=True,logy=True)


#plt.savefig('wordz.png')index=c
