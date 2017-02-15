from scipy.stats import entropy
import numpy as np
import pandas as pd
import sys, re
from scipy.linalg import norm
from scipy.spatial.distance import euclidean
import time


_SQRT2 = np.sqrt(2)     # sqrt(2) with default precision np.float64


def hellinger1(p, q):
    return norm(np.sqrt(p) - np.sqrt(q)) / _SQRT2


def hellinger2(p, q):
    return euclidean(np.sqrt(p), np.sqrt(q)) / _SQRT2


def hellinger3(p, q):
    hel = np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2)) / _SQRT2
    return hel


def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False


def hel_full2full(p_prop) :
    print 'hel_full2full'
    with open(p_prop, 'r') as p_file : 
        p = p_file.read().split('\t')
    p_file.close
    
    p = [float(i)  for i in p if isfloat(i)]
    print p
    hel_a = map(lambda i : map(lambda j : hellinger3(p[i], p[j]), xrange(i+1,len(p)-1)), xrange(0,len(p)-2))
    print hel_a
#    sys.exit()    
#    with open('/data/pulp/support/dist_plots/hel_full2full.txt', 'w') as hel :
    with open('/data/pulp/test/full2full_test.txt', 'w') as hel :
        hel.write(','.join([','.join(map(str, hel_l)) for hel_l in hel_a]))
#','.join([','.join(map(str, n)) for n in a])
    hel.closed
  


def hel_full2sec(p,q) :
    i = 0
    hel_a = []
    
    for p_i in p :
        if len(p_i) > 1 :
            file_num = p_i.split()[1].split('/')[-1].split('.txt')[0]
            print 'i %d ja file %s'%(i,file_num)
            
            i += 1
            hel = []
            to_del = []
    
            for q_i in q :   
                if len(q_i) > 1 :
                    sec_num = q_i.split()[1].split('/')[-1].split('_')[0]
                    print 'i %d ja file %s'%(i,file_num)
    
                    if file_num == sec_num :
                        hel.append(hellinger3(map(float, p_i.split()[2:]), map(float, q_i.split()[2:])))                     
                        to_del.append(q_i)
    
            hel_a.append(hel)
            q = [q_k for q_k in q if q_k not in to_del]
    
    with open('/data/pulp/support/dist_plots/hel.txt', 'w') as hel :
        hel.write('\n'.join([' '.join([str(hel_s) for hel_s in hel_l]) for hel_l in hel_a]))
    hel.closed
    
    
def hel_sec_last(q_prop,t) :
    print 'hel_secs_last'
    a = time.clock()
    q = pd.read_csv(q_prop, sep='.txt\t',names=['file','dist'],engine='python')
    
    q['dist'] = q.dist.str.split('\t')
    q['file'] = q['file'].apply(lambda x : x.split('/')[-1])
    
    t = [i.split(',')[0]  for i in t if i.find('conclusion') != -1]
    print len(t)

    q_c = q[q['file'].isin(t)==True].dist
    q_c = q_c.apply(lambda x : (map(float,x))).tolist()
    q_len = len(q_c)
    print q_len
    
#    hel_c = map(lambda i : map(lambda j : hellinger3(q_c[i], q_c[j]), xrange(i+1,len(q_c)-1)), xrange(0,len(q_c)-2))
    
    with open('/data/pulp/support/dist_plots/hel_concl.txt', 'w') as hel :

        def hel_and_save(i,j) :
            hel_s = hellinger3(q_c[i], q_c[j])
            hel.write(str(hel_s)+'\n') 
            print 'hel(%d, %d)'%(i,j)
    
        map(lambda i : map(lambda j : hel_and_save(i,j), xrange(i+1,q_len-1)), xrange(0,q_len-2))
        b = time.clock()
        print 'time elapsed %f'%(b-a)
#        hel.write(' '.join([' '.join([str(hel_s) for hel_s in hel_l]) for hel_l in hel_c]))
    hel.closed
    
    
def hel_sec_first(q_prop,t) :
    print 'hel_sec_first'

    q = pd.read_csv(q_prop, sep='.txt\t',names=['file','dist'],engine='python')
    
    q['dist'] = q.dist.str.split('\t')
    q['file'] = q['file'].apply(lambda x : x.split('/')[-1])
    
    t = [i.split(',')[0]  for i in t if i.find('introduction') != -1]
    print len(t)
    
    q_c = q[q['file'].isin(t)==True].dist
    q_c = q_c.apply(lambda x : (map(float,x))).tolist()
    q_len = len(q_c)
    print q_len
    
    with open('/data/pulp/support/dist_plots/hel_intro.txt', 'w') as hel :
        def hel_and_save(i,j) :
            hel_s = hellinger3(q_c[i], q_c[j])
            hel.write(str(hel_s)+'\n') 
            print 'hel(%d, %d)'%(i,j)
    
        a = time.clock()
        print a
        map(lambda i : map(lambda j : hel_and_save(i,j), xrange(i+1,q_len-1)), xrange(0,q_len-2))
        b = time.clock()
        print b-a
    hel.closed
    
    
def hel_sec_abstr(q_prop,t) :

    q = pd.read_csv(q_prop, sep='.txt\t',names=['file','dist'],engine='python')

    q['dist'] = q.dist.str.split('\t')
    q['file'] = q['file'].apply(lambda x : x.split('/')[-1])

    t = [i.split(',')[0]  for i in t if i.find('abstr') != -1]
    print len(t)

    q_c = q[q['file'].isin(t)==True].dist
    q_c = q_c.apply(lambda x : (map(float,x))).tolist()
    q_len = len(q_c)
    print q_len
    
    print 'data ready, beginning hellinger distance calculations'

    with open('/data/pulp/support/dist_plots/hel_abstr.txt', 'w') as hel :
        def hel_and_save(i,j) :
            hel_s = hellinger3(q_c[i], q_c[j])
            hel.write(str(hel_s)+'\n') 
            print 'hel(%d, %d)'%(i,j)

        a = time.clock()
        print a
        map(lambda i : map(lambda j : hel_and_save(i,j), xrange(i+1,q_len-1)), xrange(0,q_len-2))
        b = time.clock()
        print b-a
    hel.closed


def hel_full2abstr(p_prop,q_prop,t) :
    i = 0
    hel_a = []

    p = pd.read_csv(p_prop, sep='.txt\t',names=['file','p_dist'],engine='python')
    q = pd.read_csv(q_prop, sep='.txt\t',names=['file','q_dist'],engine='python')

    p['p_dist'] = p.p_dist.str.split('\t')
    p['file'] = p['file'].apply(lambda x : x.split('/')[-1])
    p['file'] = p['file'].apply(lambda x : x+'_0')
    
    q['q_dist'] = q.q_dist.str.split('\t')
    q['file'] = q['file'].apply(lambda x : x.split('/')[-1])

    t = [i.split(',')[0]  for i in t if i.find('abstr') != -1]
    print len(t)

    p = p[p['file'].isin(t)==True].sort_values('file')
    q = q[q['file'].isin(t)==True].sort_values('file')
    
    result = pd.merge(left=p, right=q, on='file')
    p_c = result.p_dist.apply(lambda x : (map(float,x))).tolist()
    p_len = len(p_c)
    q_c = result.q_dist.apply(lambda x : (map(float,x))).tolist()
    q_len = len(q_c)
    
    print 'data ready, beginning hellinger distance calculations'

    with open('/data/pulp/support/dist_plots/hel_full2abstr.txt', 'w') as hel :
        def hel_and_save(i) :
            hel_s = hellinger3(p_c[i], q_c[i])
            hel.write(str(hel_s)+'\n') 
            print 'hel(%d)'%(i)

        a = time.clock()
        map(lambda i : hel_and_save(i), xrange(p_len))
        b = time.clock()
        print b-a
    hel.closed
    
    print 'full_len %d abstr_len %d'%(p_len,q_len)


def hel_full2intro(p_prop,q_prop,t) :
    p = pd.read_csv(p_prop, sep='.txt\t',names=['file','p_dist'],engine='python')
    q = pd.read_csv(q_prop, sep='.txt\t',names=['file','q_dist'],engine='python')

    p['p_dist'] = p.p_dist.str.split('\t')
    p['file'] = p['file'].apply(lambda x : x.split('/')[-1])
    
    q['q_dist'] = q.q_dist.str.split('\t')
    q['file'] = q['file'].apply(lambda x : x.split('/')[-1])

    print p[:5]
    print q[:5]
    
    t = [i.split(',')[0]  for i in t if i.find('intro') != -1]
    print len(t)

    q = q[q['file'].isin(t)==True].sort_values('file')
    q['file'] = q['file'].apply(lambda x : x.split('_')[0])

    t = [i.split('_')[0]  for i in t ]
    p = p[p['file'].isin(t)==True].sort_values('file')
    print p[:5]
    print q[:5]
    
    result = pd.merge(left=p, right=q, on='file')
    print result[:10]
    p_c = result.p_dist.apply(lambda x : (map(float,x))).tolist()
    p_len = len(p_c)
    print p_len
    q_c = result.q_dist.apply(lambda x : (map(float,x))).tolist()
    q_len = len(q_c)
    print q_len
#    sys.exit()
    
    print 'data ready, beginning hellinger distance calculations'

    with open('/data/pulp/support/dist_plots/hel_full2intro.txt', 'w') as hel :
        def hel_and_save(i) :
            hel_s = hellinger3(p_c[i], q_c[i])
            hel.write(str(hel_s)+'\n') 
#            print 'hel(%d)'%(i)

        a = time.clock()
        print a
        map(lambda i : hel_and_save(i), xrange(p_len))
        b = time.clock()
        print b-a
    hel.closed
    
    print 'titles %d full_len %d intro_len %d'%(len(t),p_len,q_len)


def hel_full2concl(p_prop,q_prop,t) :
    p = pd.read_csv(p_prop, sep='.txt\t',names=['file','p_dist'],engine='python')
    q = pd.read_csv(q_prop, sep='.txt\t',names=['file','q_dist'],engine='python')

    p['p_dist'] = p.p_dist.str.split('\t')
    p['file'] = p['file'].apply(lambda x : x.split('/')[-1])
    
    q['q_dist'] = q.q_dist.str.split('\t')
    q['file'] = q['file'].apply(lambda x : x.split('/')[-1])

    t = [i.split(',')[0]  for i in t if i.find('conclusion') != -1]
    print len(t)

    q = q[q['file'].isin(t)==True].sort_values('file')
    q['file'] = q['file'].apply(lambda x : x.split('_')[0])

    t = [i.split('_')[0]  for i in t ]
    p = p[p['file'].isin(t)==True].sort_values('file')
    
    result = pd.merge(left=p, right=q, on='file')
    p_c = result.p_dist.apply(lambda x : (map(float,x))).tolist()
    p_len = len(p_c)
    q_c = result.q_dist.apply(lambda x : (map(float,x))).tolist()
    q_len = len(q_c)
    
    print 'data ready, beginning hellinger distance calculations'

    with open('/data/pulp/support/dist_plots/hel_full2concl.txt', 'w') as hel :
        def hel_and_save(i) :
            hel_s = hellinger3(p_c[i], q_c[i])
            hel.write(str(hel_s)+'\n') 
            print 'hel(%d)'%(i)

        a = time.clock()
        print a
        map(lambda i : hel_and_save(i), xrange(p_len))
        b = time.clock()
        print 'time elapsed %f'%b-a
    hel.closed
    
    print 'titles %d full_len %d concl_len %d'%(len(t), len(p), len(q))


def hel_full2mid(p_prop,q_prop,t) :
    p = pd.read_csv(p_prop, sep='.txt\t',names=['file','p_dist'],engine='python')
    q = pd.read_csv(q_prop, sep='.txt\t',names=['file','q_dist'],engine='python')

    p['p_dist'] = p.p_dist.str.split('\t')
    p['file'] = p['file'].apply(lambda x : x.split('/')[-1])
    
    q['q_dist'] = q.q_dist.str.split('\t')
    q['file'] = q['file'].apply(lambda x : x.split('/')[-1])
    
    t = [i.split(',')[0]  for i in t if all([i.find('conclusion') == -1, i.find('introduction') == -1, i.find('abstr') == -1])]
    print len(t)

    q = q[q['file'].isin(t)==True].sort_values('file')

    q['file'] = q['file'].apply(lambda x : x.split('_')[0])
    
    result = pd.merge(left=p, right=q, on='file')
    result_gp = result.groupby('file')
    
    print 'data ready, beginning hellinger distance calculations'
    a = time.clock()
    i = 0
    hel_a = []
    for n,g in result_gp :
        i += 1
        print n
        print g
        print type(g)
        p = g.p_dist.apply(lambda x : (map(float,x))).tolist()
        print p
        q = g.q_dist.apply(lambda x : (map(float,x))).tolist()
        print q
        hel = map(lambda i: hellinger3(p[i], q[i]), xrange(len(p)))
        print hel
        hel = sum(hel)/len(hel)
        print '%d hel %f'%(i,hel)
        hel_a.append(hel)
 
    b = time.clock()
    print 'time %f'%(b-a)

    with open('/data/pulp/support/dist_plots/hel_full2mid.txt', 'w') as hel :
        hel.write('\n'.join(map(str, hel_a))) 
    hel.closed
    
def hel_fullabstr2full(p_prop,q_prop) :
    p = pd.read_csv(p_prop, sep='.txt\t',names=['file','p_dist'],engine='python')
    q = pd.read_csv(q_prop, sep='_\d*\t',names=['file','q_dist'],engine='python')
    
    p['p_dist'] = p.p_dist.str.split('\t')
    p['file'] = p['file'].apply(lambda x : x.split('/')[-1])
    
    q['q_dist'] = q.q_dist.str.split('\t')
    q['file'] = q['file'].apply(lambda x : x.split('\t')[-1])

    result = p.merge(q, how='right',  on='file')
    print result[-250:-220]
    p_c = result.p_dist.apply(lambda x : (map(float,x))).tolist()
#    p_c = result.p_dist.tolist()
    p_len = len(p_c)
    q_c = result.q_dist.apply(lambda x : (map(float,x))).tolist()
#    q_c = result.q_dist.tolist()
    q_len = len(q_c)
    
    print 'data ready, beginning hellinger distance calculations'

    with open('/data/pulp/support/dist_plots/hel_fullabstr2full.txt', 'w') as hel :
        def hel_and_save(i) :
#            hel_s = hellinger3([float(x) for x in p_c[i] if isfloat(x)], [float(x) for x in q_c[i] if isfloat(x)])
            hel_s = hellinger3(map(float,p_c[i]), map(float,q_c[i]))
            hel.write(str(hel_s)+'\n')
            print 'hel(%d)'%(i)

        a = time.clock()
        print a
        map(lambda i : hel_and_save(i), xrange(p_len))
        b = time.clock()
        print 'time elapsed %f'%(b-a)
    hel.closed
    
    print 'full_len %d abstr_len %d'%(len(p), len(q))
    

def hel_abstr2intro(q_prop,t,sect) :
    i = 0
    hel_a = []

    q = pd.read_csv(q_prop, sep='.txt\t',names=['file','dist'],engine='python')
    
    q['dist'] = q.dist.str.split('\t')
    q['file'] = q['file'].apply(lambda x : x.split('/')[-1])

    t_a = [i.split(',')[0]  for i in t if i.find('abstr') != -1]
    t_i = [i.split(',')[0]  for i in t if i.find(sect) != -1]
    print t_a[0:5]
    print t_i[0:5]
    print 'abstracts %d %s %d'%(len(t_a), sect, len(t_i))

    q_a = q[q['file'].isin(t_a)==True].sort_values('file')
    q_i = q[q['file'].isin(t_i)==True].sort_values('file')
    print q_a[0:5]
    print q_i[0:5]

    q_a['file'] = q_a['file'].apply(lambda x : x.split('_')[0])
    print q_a[0:5]
    q_i['file'] = q_i['file'].apply(lambda x : x.split('_')[0])
    print q_i[0:5]
    
    result = pd.merge(left=q_a, right=q_i, how='inner', on='file', suffixes=('_a', '_i'))
    print result[0:5]
    abstr = result.dist_a.apply(lambda x : (map(float,x))).tolist()
    a_len = len(abstr)
    intro = result.dist_i.apply(lambda x : (map(float,x))).tolist()
    i_len = len(intro)
    r_len = len(result)
    
    print 'data ready, calculating hellinger distance'

    with open('/data/pulp/support/dist_plots/hel_abstr2'+sect+'.txt', 'w') as hel :
        def hel_and_save(i) :
            hel_s = hellinger3(abstr[i], intro[i])
            hel.write(str(hel_s)+'\n')
            print 'hel(%d)'%(i)

        a = time.clock()
        map(lambda i : hel_and_save(i), xrange(r_len))
        b = time.clock()
        print b-a
    hel.closed
    
    print '%s_len %d abstr_len %d result_len %d'%(sect,i_len, a_len, r_len)

     
def hel_abstr2mid(q_prop,t) :
    ind = 0
    hel_a = []

    q = pd.read_csv(q_prop, sep='.txt\t',names=['file','dist'],engine='python')
    
    q['dist'] = q.dist.str.split('\t')
    q['file'] = q['file'].apply(lambda x : x.split('/')[-1])

    t_a = [i.split(',')[0]  for i in t if i.find('abstr') != -1]
    t_m = [i.split(',')[0]  for i in t[1:] if all([i.find('conclusion') == -1, i.find('introduction') == -1, i.find('abstr') == -1])]
    print t_a[0:5]
    print t_m[0:5]
    print 'abstracts %d mids %d'%(len(t_a),len(t_m))

    q_a = q[q['file'].isin(t_a)==True].sort_values('file')
    q_m = q[q['file'].isin(t_m)==True].sort_values('file')
    print q_a[0:5]
    print q_m[0:5]

    q_a['file'] = q_a['file'].apply(lambda x : x.split('_')[0])
    print q_a[0:5]
    q_m['file'] = q_m['file'].apply(lambda x : x.split('_')[0])
    print q_m[0:5]
    
    result = pd.merge(left=q_a, right=q_m, how='inner', on='file', suffixes=('_a', '_m'))
    print result[0:25]
#    abstr = result.dist_a.apply(lambda x : (map(float,x))).tolist()
#    a_len = len(abstr)
#    intro = result.dist_i.apply(lambda x : (map(float,x))).tolist()
#    i_len = len(intro)
#    r_len = len(result)
#    
#    print 'data ready, calculating hellinger distance'
#
#    with open('/data/pulp/support/dist_plots/hel_abstr2'+sect+'.txt', 'w') as hel :
#        def hel_and_save(i) :
#            hel_s = hellinger3(abstr[i], intro[i])
#            hel.write(str(hel_s)+'\n')
#            print 'hel(%d)'%(i)
#
#        a = time.clock()
#        map(lambda i : hel_and_save(i), xrange(r_len))
#        b = time.clock()
#        print b-a
#    hel.closed
#    
#    print '%s_len %d abstr_len %d result_len %d'%(sect,i_len, a_len, r_len)

    result_gp = result.groupby('file')
    
    print 'data ready, calculating hellinger distance'

    a = time.clock()

    for n,g in result_gp :
        ind += 1 
        print n
        print g
        print len(g)
        abstr = g.dist_a.apply(lambda x : (map(float,x))).tolist()
        print 'abstr len %d'%len(abstr)
        print abstr
        mid = g.dist_m.apply(lambda x : (map(float,x))).tolist()
        print 'mid len %d'%len(mid)
        print mid
        hel = map(lambda i: hellinger3(abstr[i], mid[i]), xrange(len(g)))
        print hel
        hel = sum(hel)/len(hel)
        print '%d hel %f'%(ind,hel)
        hel_a.append(hel)
 
    b = time.clock()
    print 'time %f'%(b-a)

    with open('/data/pulp/support/dist_plots/hel_abstr2mid.txt', 'w') as hel :
        hel.write('\n'.join(map(str, hel_a))) 
    hel.closed

def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False


def main(argv) :
    with open('/data/pulp/support/section_titles.txt', 'r') as title_file : 
        t = title_file.read().lower().split('\n')
    title_file.close
    
    # doc-topic proportion files of articles and sections
    p_prop = argv[1]
    q_prop = argv[2]

#    q_comp = argv[1]

#    p = ''
#    q = ''
#
#    with open(p_prop, 'r') as p_file : 
#        p = p_file.read().split('\n')
#    p_file.close
#    
#    with open(q_prop, 'r') as q_file : 
#        q = q_file.read().split('\n')
#    q_file.close

#    hel_full2sec(p,q)

#    hel_sec_last(q_prop, t)
#    hel_sec_first(q_prop, t)
#    hel_sec_abstr(q_prop, t)
#    hel_full2abstr(p_prop, q_prop, t)
#    hel_full2intro(p_prop, q_prop, t)
#    hel_full2concl(p_prop, q_prop, t)
#    hel_full2mid(p_prop, q_prop, t)
#    hel_full2full(p_prop)
#    hel_full2mid(p_prop,q_prop,t)
#    hel_fullabstr2full(p_prop,q_prop)
#    hel_abstr2intro(p_prop,t,'concl')
    hel_abstr2mid(p_prop,t)

    pass


if __name__ == "__main__":
    main(sys.argv)
    
