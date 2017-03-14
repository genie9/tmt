from scipy.stats import entropy
import numpy as np
import pandas as pd
import sys, re
    
 
def count_secs(q_prop) :
    max = 0
    min = 1000
    c = ''
    count = []

    q = pd.read_csv(q_prop, sep='.txt\t',names=['file','dist'],engine='python')
    
    q.drop('dist',axis=1,inplace=True)
    q['file'] = q['file'].apply(lambda x : x.split('/')[-1].split('_')[0])
    print q

    result_gp = q.groupby('file')
    
    print 'data ready, calculating sections'

    for n,g in result_gp :
        print n
        print g
        l = len(g)
        c = str(n)+','+str(l)
        if l < min : min = l
        if l > max : max = l
        count.append(c)

    print 'max %d, min %d'%(max,min)

    with open('/data/pulp/support/sec_count.txt', 'w') as secs :
        a = '\n'.join(map(str, count))
        print a
        secs.write(a) 
    secs.closed

    df = pd.read_csv('/data/pulp/support/sec_count.txt', names=['f','c'])
    df.sort_values(by='c', inplace=True)
    df.to_csv('/data/pulp/support/sec_count_sorted.txt',index=False,header=False)


def main(argv) :
    count_secs(argv[1])

    pass


if __name__ == "__main__":
    main(sys.argv)
    
