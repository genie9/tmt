import re, sys,os
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


def find_junk(tbl, junk_file, doc_freq, word_freq, doc_cov) :
#    tbl = pd.read_csv(words_file, sep=',', header=0, names=['word','doc_freq','word_freq','doc_cov'])
    junk = tbl[(tbl['doc_freq']<doc_freq) | (tbl['word_freq']<word_freq) | (tbl['doc_cov']>doc_cov)] 
    
    print junk.shape
    print junk.index.values
    
    with open(junk_file, 'w') as f :
        f.write(junk.index.values)    
    f.closed

#######################################################################################

def main(argv) :
    if len(argv) != 7 :
        print  '**Usage ', argv[0], "<input path> <output path for sorted corpus table> <junk file> <junkword document coverage less then [num]> <junkword count less then [num]> <junkword document coverage more then [%]>"
        sys.exit()

    in_path = argv[1]
    dest_path_doc = argv[2]
    junk_file = argv[3]
    doc_freq = argv[4]
    word_freq = argv[5]
    doc_cov = argv[6]
    
    files = os.listdir(in_path)
    size = len(files)
    
    opened = (open(in_path+f) for f in files)
    read = (f.read().split() for f in opened)
    print 'reading done'

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
    # save files: sorted by doc coverage percent, sorted by word count in corpus

    df_1 = pd.DataFrame(d,index=['doc_freq'])
    df_2 = pd.DataFrame(wc,index=['word_freq'])

    df = pd.merge(df_1.T, df_2.T,left_index=True, right_index=True )

    df['doc_cov'] = df.apply(lambda row : float(int(row['doc_freq']))/float(size)*100, axis=1)

    df.sort_values(by='doc_freq',inplace =True)
    df.to_csv(dest_path_doc)

#    df.sort_values(by='word_freq',inplace =True)
#    df.to_csv(dest_path_word)

    find_junk(df, junk_file, int(doc_freq), int(word_freq), int(doc_cov))
    pass


if __name__ == "__main__":
    main(sys.argv)
