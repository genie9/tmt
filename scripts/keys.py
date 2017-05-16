from nltk.stem import SnowballStemmer
import sys
stemmer = SnowballStemmer('english')

with open('/data/pulp/from_mallet/topic_100/secs_nonstem/secs_nonstem_100_keys.txt', 'r') as keys_file :
    new_keys = []
#    keys = keys_file.read()
    for l in keys_file :
#        print l
#        sys.exit()
        num,p,row = l.split('\t')
        tmp = ('%s\t%s\t'%(num,p))
        row = row.split()
        print 'row of non stemmed keys'
        print row
        row_stem = [stemmer.stem(i) for i in row]
        print 'row of stemmed keys'
        print row_stem
        row_set = set(row_stem)
        print 'row of unique stemmed keys'
        print row_set
        row_ind = [row_stem.index(next(i for i in row_stem if i==k)) for k in row_set]
        row_ind.sort()
        print 'row of indeces of unique keys'
        print row_ind
        tmp += ' '.join([row[i] for i in row_ind])
        print 'row of unique non stemmed keys'
        print tmp
        new_keys.append(tmp)        
    with open('/data/pulp/from_mallet/topic_100/secs_nonstem/secs_nonstem_100_keys_uniq.txt', 'w') as k_f :
        k_f.write('\n'.join(l for l in new_keys))
    k_f.closed
keys_file.closed
