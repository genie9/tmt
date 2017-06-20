from nltk.stem import SnowballStemmer
import sys

stemmer = SnowballStemmer('english')

argv = sys.argv

with open(argv[1], 'r') as keys_file :
    new_keys = []
    for l in keys_file :
        num,p,row = l.split('\t')
        tmp = ('%s\t%s\t'%(num,p))
        # non stemmed keys
        row = row.split()
        # stemmed keys
        row_stem = [stemmer.stem(i) for i in row]
        # unique stemmed keys
        row_set = set(row_stem)
        # indeces of unique keys
        row_ind = [row_stem.index(next(i for i in row_stem if i==k)) for k in row_set]
        row_ind.sort()
        # unique non stemmed keys
        tmp += ' '.join([row[i] for i in row_ind])
        new_keys.append(tmp)        
    with open(argv[2], 'w') as k_f :
        k_f.write('\n'.join(l for l in new_keys))
    k_f.closed
keys_file.closed
