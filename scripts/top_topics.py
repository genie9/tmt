import pandas as pd
import matplotlib.pyplot as plt
import sys

f = '/data/pulp/from_mallet/topic_100/secs_v3/secs_100_props.txt'
props = pd.read_csv(f, delimiter='\t', names=['num','File']+[str(i) for i in range(100)], index_col='num', na_values=[''], engine='c')
print props[0:5]

props.drop('File', axis=1, inplace=True)
summs = props.sum(axis=0)
print type(summs)
s_summs = summs.sort_values(ascending=False)
#print 'wat'
print s_summs

s_summs.plot.line()
ax = plt.gca()
fig = ax.get_figure()
fig.savefig('/data/pulp/from_mallet/topic_100/secs_v3/props_sum_plot.png')

s_summs.to_csv('/data/pulp/from_mallet/topic_100/secs_v3/props_sum.txt')

#with open('/data/pulp/from_mallet/topics_100/sacs_v3/props_sum.txt') as w_f :
#    w_f.write(s_summs)
#w_f.closed

