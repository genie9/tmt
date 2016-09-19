import pandas as pd
import matplotlib.pyplot as plt
import sys, os, re


comp_full = '/data/mallet_tests/from_mallet/topics_50/full2/full2_50_compostion.txt'
comp_sect = '/data/mallet_tests/from_mallet/topics_50/sections2/sections2_50_compostion.txt'
full_plot = '/data/mallet_tests/from_mallet/plots/tests/'#old/'


def do_df(path) :
    df = pd.read_csv(path, delimiter='\t', names=['File']+[str(i) for i in range(50)], na_values=[''], engine='c')
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

def do_sections_chart(df) :
    df.File = df.File.str.split('_').str[1]
    print df.File[0:10]
#    gp = df.loc[df.File=='1']
    gp_i = df[df.File=='0'].index.tolist()
#    print gp_i
    gp_i = [int(i)-1 for i in gp_i if i>0]
#    print gp_i
    gp = df.ix[gp_i]
    print gp
#    gp.reindex([i for i in xrange(35161)])
#    print gp['0']
#    sys.exit()
    
    for t in xrange(50) :
        gp_t = gp[str(t)]
        print 'nyt forrissa'
        print gp_t
        gp_t.plot(figsize=(32,16),kind='line',grid=True)
        plt.savefig('/data/mallet_tests/from_mallet/plots/tests/sec_last_topic_%s.png' %t )
        plt.xticks([r for r in xrange(len(gp_t.keys()))],gp_t.keys())
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
#            ytiks = [k/10 for k in xrange(10)]
#            plt.yticks([k for k in ytiks], ytiks)
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
#    df_full = do_df(comp_full)
#    
#    if chart == 'docs' :
#        df_sect = do_df(comp_sect)
#        do_doc_charts(df_full,df_sect)
#    elif chart == 'topics' :
#        do_topics_charts(df_full)
#    else :
    df_sect = do_df(comp_sect)
#    do_doc_charts(df_full,df_sect)

#    do_topics_charts(df_full)
    do_sections_chart(df_sect)
    pass


if __name__ == "__main__":
    main(sys.argv)

