import sys,os
import pandas as pd


d = {}
tbl = []
wc = {}

count_2 = 0
count_3 = 0

def do_count(s) :
    print s #nonii.keys()[nonii.values().index(s)]
    counted = (n.count(s) for n in as_num)
    counted = [i for i in counted if i > 0]
    
    docs = len(counted)
    print docs
    
    doc_cov = (float(docs)/float(35162))*100#35162
    print doc_cov

    freq = sum(counted)
    print freq

    per_doc = 0
    if freq > 0 :
        per_doc = freq/docs
    print per_doc
#    sys.exit()
    return [docs, doc_cov, freq, per_doc]


def up_date(i) :
    d[i] = d.setdefault(i,0)+1


def do_count2(l,m) : 
    global count_2
    if count_2 == 0: 
#        print count
#        [up_date(i) for i in l]
        map(up_date, l)
        count_2 = 1

    def double_action(x) :
        d[x] = d.setdefault(x,0)+1
        l.add(x)
    
#    [double_action(i) for i in m]
    map(double_action, m)
    return l


def do_count1(x) :
    s = set(x)
    tbl.append({i:x.count(i) for i in s})
#    print tbl
    return s

def do_count3(d) : 
    global count_3
    if count_3 == 0: 
        wc = d
        count_3 = 1
    def up_date2(w,c) :
        wc[w] = wc.get(w)+c
    
    def new(w,c) :
        wc[w] = c
    
    ( up_date2(w,c) if wc.has_key(w) else new(w,c) for w,c in d.items() )
    
    print wc


#######################################################################################

#nonii = [line.split(',')[0] for line in open('/data/mallet_tests/word_dist.csv')]
#
#nonii = pd.Series(nonii)
#
#nonii = {v: k for k, v in nonii.to_dict().iteritems()}
##print nonii
#with open('/data/mallet_tests/tmp.txt','w') as f :
#    f.write(str(nonii))
#    f.write(str(nonii.keys()))
#f.closed

path = '/data/mallet_tests/to_mallet/bigrams/full_stem_5/'

files = os.listdir(path)
size = len(files)
#opened = map(lambda x: open(path+x), files)
opened = (open(path+f) for f in files)

#read = map(lambda x: x.read().split(), opened)
read = (f.read().split() for f in opened)

#as_num = [[nonii.get(k) for k in r] for r in red]

## without word count ############
uutta = map(set, read)
redu = reduce(do_count2, list(uutta))
##################################

#uutta = (set(i) for i in read)
#print uutta
#sys.exit()

## with word count ################
#sets = map(do_count1, read)
#print 'sets done'
#
#[do_count_3(dic) for dic in tbl]
#print 'wc done'
#print  wc
#sys.exit()
#
#redu = reduce(do_count2, sets)
#sys.exit()
###################################

#print redu
#print d 
#with open('/data/mallet_tests/tmp2.txt','w') as f :
#    f.write(str(d))
##    f.write(str(nonii.keys()))
#f.closed
#sys.exit()

#df = pd.DataFrame( (do_count2(v) for v in nonii.values()), index=nonii.keys(), columns=['docs', 'doc_cov', 'freq', 'per_doc'])

############ uncomment after testing #######################
df_1 = pd.DataFrame(d,index=['word','doc_freq'])
#df_2 = pd.DataFrame(tbl,index=['word','worddoc_freq'])
df_1 = df_1.T
print df_1
df_1['doc_cov'] = df_1.apply(lambda row : float(int(row['doc_freq']))/float(size)*100, axis=1)
df_1.sort_values(by='doc_cov',inplace =True)
print df_1
df_1.to_csv('/data/mallet_tests/word_bigrams_dist_v4.txt')
