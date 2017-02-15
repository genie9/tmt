from scipy.stats import entropy
import numpy as np
import sys, re

def main(argv) :
    p_comp = argv[1]
    q_comp = argv[2]

    p = ''
    q = ''

    with open(p_comp, 'r') as p_file : 
        p = p_file.read().split('\n')
    p_file.close
    
    with open(q_comp, 'r') as q_file : 
        q = q_file.read().split('\n')
    q_file.close

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
        kl.write('\n'.join([' '.join([str(kl_s) for kl_s in kl_l]) for kl_l in kl_a]))
    kl.closed

if __name__ == "__main__":
    main(sys.argv)

