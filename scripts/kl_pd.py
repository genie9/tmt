from scipy.stats import entropy
import numpy as np
import pandas as pd
import sys, re

def main(argv) :
    p_comp = argv[1]
    q_comp = argv[2]

    df_full = pd.read_csv(p_comp, sep='\t', names=['num','File']+[str(i) for i in range(100)])
    df_full.set_index('num', inplace=True)
    df_full.File = df_full.File.str[5:]
    df_full.File = df_full.File.str.split('/').str[-1].str[:-4]
    df_full = df_full.iloc[:5]
#    print df_full

    df_sec= pd.read_csv(q_comp, sep='\t', names=['num','File']+[str(i) for i in range(100)])
    df_sec.set_index('num', inplace=True)
    df_sec.File = df_sec.File.str[5:]
    df_sec.File = df_sec.File.str.split('/').str[-1].str[:-4]
#    print df_sec
#    print 'val ',df_sec.iloc[0][1:].values
#    sys.exit()
#    for p_i in df_full.itertuples():
#        print p_i[1] 
#        list(p_i[2:])
#        
#        for q_i in df_sec[df_sec.File.str.match(re.compile('^%s_'%p_i[1]))==True].iloc[:].values.tolist() :
#            print q_i[1:]
    q = [[entropy(map(float, list(p_i[2:])), map(float, q_i[1:])) for p_i in df_full.itertuples()]  for q_i in df_sec[df_sec.File.str.match(re.compile('^%s_'%p_i[1]))==True].iloc[:].values.tolist() ]
    print q
    sys.exit()
#    q = df_q.iloc[2:].index.values

    sec_pat = re.compile('^%s_'%file_num)
    df_q = df_sec[df.File.str.match(pat)==True]
    q = df_q.iloc[2:].index.values
    

    i = 0
    kl_a = []

    for p_i in p :
        if len(p_i) > 1 :
            file_num = p_i.split()[1].split('/')[-1].split('.txt')[0]
            print 'i %d ja file %s'%(i,file_num)

            
            i += 1
            kl = []
            to_del = []

            for q_i in q :   
                if len(q_i) > 1 :
                    sec_num = q_i.split()[1].split('/')[-1].split('_')[0]

                    if file_num == sec_num :
                        kl.append(entropy(map(float, p_i.split()[2:]), map(float, q_i.split()[2:])))                     
                        to_del.append(q_i)

            kl_a.append(kl)
            q = [q_k for q_k in q if q_k not in to_del]
 
#    kl_a = [[entropy(map(float, p_i.split()[2:]), map(float, q_i.split()[2:])) if len(q_i) > 1 and q_i.split()[1].split('/')[-1].split('_')[0] == p_i.split()[1].split('/')[-1].split('.txt')[0] else q.remove(q_i) for q_i in q] if len(p_i) > 1 for p_i in p]
        
#    kl_k = [entropy(map(float, p_i.split()[2:]), map(float, q_i.split()[2:])) if len(q_i) > 1 and q_i.split()[1].split('/')[-1].split('_')[0] == file_num else q.remove(q_i) for q_i in q]
 
    with open('/data/mallet_tests/support/kl.txt', 'w') as kl :
        kl.write(' '.join(['\n'.join(kl_a)]) )
    kl.closed

if __name__ == "__main__":
    main(sys.argv)

