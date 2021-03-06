import sys,os
import pandas as pd


d = {}
tbl = []
wc = {}

count_2 = 0
count_3 = 0


# append to table(tbl) dictionary of unique words and their counts per document
# create set of document words
def do_count1(x) :
    s = set(x)
    tbl.append({i:x.count(i) for i in s})
#    print tbl
    return s


# update dictionary(wc) with words and their count of document (d is a dictionary)
def do_count2(d) : 
    global count_2
    global wc
    if count_2 == 0: 
        wc = d
        count_2 = 1
    def up_date_wc(w,c) :
        wc[w] = wc.get(w)+c
    
    def new(w,c) :
        wc[w] = c
    
    [ up_date_wc(w,c) if wc.has_key(w) else new(w,c) for w,c in d.items() ]
    

# input to dictionary d which has words and number of documents their appeared in
def up_date(i) :
    d[i] = d.setdefault(i,0)+1

# update dictionary d with words from set l
# return set l udated with words from set m 
def do_count3(l,m) : 
    global count_3
    if count_3 == 0: 
        map(up_date, l)
        count_3 = 1

    def double_action(x) :
        d[x] = d.setdefault(x,0)+1
        l.add(x)
    
    map(double_action, m)
    return l

#######################################################################################

def main(argv):

    if len(argv) != 4 :
        print '**Usage: ', argv[0], '<working directory> <preprocessed article directory> \
                <corpus file>'
        sys.exit()

    root = argv[1]
    preproc = argv[2]
    dest = argv[3]

    files = os.listdir(preproc)
    size = len(files)
    
    opened = (open(preproc+f) for f in files)
    read = (f.read().split() for f in opened)

    # create table of dictionaries with word count for each document 
    sets = map(do_count1, read)
    print 'sets done'

    # create dictionary of words and their count in corpus
    [do_count2(dic) for dic in tbl]
    print 'wc done'
    
    # create dictionary of words with number of documents they appeared in
    redu = reduce(do_count3, sets)

    # create data frames from dictionaries d and w
    # merge to same dataframe and do analysis
    # save files: sorted by doc coverage percent

    df_1 = pd.DataFrame(d,index=['doc_freq'])
    df_2 = pd.DataFrame(wc,index=['word_freq'])

    df = pd.merge(df_1.T, df_2.T,left_index=True, right_index=True )

    df['doc_cov'] = df.apply(lambda row : float(int(row['doc_freq']))/float(size)*100, axis=1)

    df.sort_values(by='doc_freq',inplace =True)
    df.index.name = 'word'
    df.to_csv(dest)

    pass


if __name__ == "__main__":
    main(sys.argv)
