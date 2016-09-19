import pandas as pd



path = '/data/mallet_tests/from_mallet/topics_50/full2/full2_50_weights.txt'

with open(path) as f :
#    print f.name
    t = [i.split('\t') for i in f if i.split('\t')[0] == '0']
#    for i in f :
#        while i.split('\t')[0] == '0' :
#            print i
#            t.append(i)
    df = pd.DataFrame(t,columns=['topic','word','weight'])
#    print df
    df.weight = pd.to_numeric(df.weight)
    df.sort_values('weight',axis=0,ascending=False,inplace=True)
#    print df     
    with open('/data/mallet_tests/from_mallet/topics_50/full2/weight_exmp.txt','w') as w :
        w.write(df.to_string(col_space=5,index=False))
    w.closed
f.closed

