import pandas as pd
import matplotlib.pyplot as plt
import sys, os, re


comp_full = '/data/mallet_tests/from_mallet/topics_50/full2/full2_50_compostion.txt'
comp_sect = '/data/mallet_tests/from_mallet/topics_50/sections2/sections2_50_compostion.txt'
full_plot = '/data/mallet_tests/from_mallet/plots/new/'
f = open('/data/mallet_tests/from_mallet/topics_50/new_order.txt')
topics = [int(i.split()[1]) for i in f]
print topics
#sys.exit()

def do_df(path,names) :
#    df = pd.read_csv(path, delimiter='\t', names=['File']+[str(i) for i in range(50)], na_values=[''], engine='c')
    df = pd.read_csv(path, delimiter='\t', names=['File']+names, na_values=[''], engine='c')
    df.File= df.File.str[5:]
    df.File = df.File.str.split('/').str[-1].str[:-4]
    print 'dataframe created'
    return df

def do_doc_charts(df_full, df_sect) :
    for i in xrange(len(df_full.index)) :
        if i%1000==0 :
            print i
            dfi = df_full.iloc[i] 
            article = dfi.File
            dfi.drop('File', inplace=True)
            
            dfs = df_sect.loc[df_sect.File.str.find(article) != -1]
            dfs.drop('File',axis=1,inplace=True)
#            cols = list(dfs.columns.values)
#            dfs.plot(figsize=(32,16),kind='bar',grid=True)
#            #plt.xticks([r for r in xrange(len(cols))],cols)
#            plt.savefig(os.path.join(full_plot,article+'_sect.png'))
            for s in xrange(len(dfs.index)) :
                print s
                dfs_s = dfs.iloc[s]
                dfs_s = dfs_s.astype(float)
                dfs_s.plot(figsize=(32,16),grid=True,label=s)
                   
                plt.xticks([r for r in xrange(len(dfs_s.keys()))],dfs_s.keys())
                plt.savefig(os.path.join(full_plot,article+'_sect.png'))
            
            plt.close()

            dfi = dfi.astype(float)
            dfi.plot(figsize=(32,16),kind='bar',grid=True,color='pink')
            plt.xticks([k for k in xrange(len(dfi.keys()))],dfi.keys())
            plt.savefig(os.path.join(full_plot,article+'.png'))
            plt.close()


def do_topics_charts(df_full) :
    df_full = df_full.set_index('File').T

    for i in xrange(len(df_full.index)) :
            print i
            dfi = df_full.iloc[i] 
            #article = dfi.File
            #dfi.drop('File', inplace=True)
            print dfi
    #        sys.exit()

            dfi = dfi.astype(float)
            dfi.plot(figsize=(64,16),grid=True)
            plt.xticks([k for k in xrange(len(dfi.keys()))],dfi.keys())
            plt.yticks([k/10 for k in xrange(10)])
    #        mpl.ticker.AutoMinorLocator(n=None)
    #        plt.tick_params(labelright=True)
    #
    #        df.iloc[i].plot(figsize=(32,16),kind=kind,fontsize=10,rot=90,grid=True,logy=True)
            plt.savefig(os.path.join(full_plot,'topic_'+str(i)+'.png'))
            plt.close()


def main(argv):
#    if len(argv) != 2 :
#        print '**Usage: ', argv[0], '<docs | topics>'
#        sys.exit()
#    
#    chart = argv[1]
#
    df_full = do_df(comp_full,topics)
    print df_full.iloc[:2]
#    sys.exit()
    df_full.sort_index(axis=1,inplace=True,sort_remaining=False)
    print df_full.iloc[:2]
    sys.exit()
#    
#    if chart == 'docs' :
#        df_sect = do_df(comp_sect)
#        do_doc_charts(df_full,df_sect)
#    elif chart == 'topics' :
#        do_topics_charts(df_full)
#    else :
    df_sect = do_df(comp_sect,[str(i) for i in range(50)])
    do_doc_charts(df_full,df_sect)
    do_topics_charts(df_full)
    pass


if __name__ == "__main__":
    main(sys.argv)

