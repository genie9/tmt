import pandas as pd
from numpy.core import multiarray
import matplotlib.pyplot as plt
import sys


argv = sys.argv

in_file = argv[1]
out_file = argv[2]
topics = int(argv[3])

props = pd.read_csv(in_file, delimiter='\t', \
        names=['num','File']+[str(i) for i in range(topics)], \
        index_col='num', na_values=[''], engine='c')
#print props[0:5]

props.drop('File', axis=1, inplace=True)

summs = props.sum(axis=0, numeric_only=True)
#print summs

summs = summs.sort_values(ascending=False)
#print summs
#print type(summs)

summs.plot.line()
ax = plt.gca()
fig = ax.get_figure()
fig.savefig(out_file+'_plot.png')

summs.to_csv(out_file+'.txt', index=False, header=False)
summs.columns = ['num','count']
#print summs

nums = summs.index.values.tolist()
print nums

with open(out_file+'_nums.txt','w') as f :
    f.write('\n'.join(nums))
f.closed

