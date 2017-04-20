import pandas as pd
import matplotlib.pyplot as plt
import sys

in_file = sys.argv[1]
out_file = sys.argv[2]

#f = '/data/pulp/from_mallet/topic_100/secs_v3/secs_100_props.txt'
props = pd.read_csv(in_file, delimiter='\t', names=['num','File']+[str(i) for i in range(100)], index_col='num', na_values=[''], engine='c')
print props[0:5]

props.drop('File', axis=1, inplace=True)

summs = props.sum(axis=0, numeric_only=True)
print summs

summs = summs.sort_values(ascending=False)
#print 'wat'
print summs

summs.plot.line()
ax = plt.gca()
fig = ax.get_figure()
fig.savefig(out_file+'_plot.png')

summs.to_csv(out_file+'.txt', index=False, header=False)

nums = pd.read_csv('/data/pulp/from_mallet/topic_100/secs_v3/props_sum.txt',names=['num','count']) 

nums = nums.num

nums.to_csv(out_file+'_nums.txt',index=False,header=False)

#with open('/data/pulp/from_mallet/topics_100/sacs_v3/props_sum.txt') as w_f :
#    w_f.write(s_summs)
#w_f.closed

