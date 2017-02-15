import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys, os
from subprocess import check_output
from numpy.random import choice as rnd



################################################################################
def fig1(data) :
    fig1 = plt.figure(1, figsize=(64,16))
    i = 1
    for l in data :
        for h in l.split() :
            plt.plot(i, float(h), 'ro')
        i += 1

    fig1.savefig('/data/pulp/plots/dist/hel_v1.png')

################################################################################
def fig2(data) :
    fig2 = plt.figure(2, figsize=(16,16))

    data = map(lambda l: np.mean(map(float, l.split())), data)

    plt.boxplot(data, showmeans=True)

    ax = plt.gca()
    plt.minorticks_on()
    ax.yaxis.grid(True, linestyle='-', which='major', color='grey', alpha=0.5)
    ax.yaxis.grid(True, linestyle='--', which='minor', color='lightgrey', alpha=0.5)

    plt.title("Average distance between article and it's sections")
    fig2.savefig('/data/pulp/plots/dist/hel_full_avg_sec_box.png')

################################################################################
def combobox(data, x_labels, f_name, caption) :
    fig3 = plt.figure(3, figsize=(16,16))

    float_data = []
    for d in data:
        with open(d) as d_file :
            dat = d_file.read().split('\n')
            print dat[:10]
            float_data.append([float(i) for i in dat if isfloat(i)])
        d_file.closed

    plt.boxplot(float_data, showmeans=True, labels=x_labels)

    ax = plt.gca()
    plt.minorticks_on()
    ax.yaxis.grid(True, linestyle='-', which='major', color='grey', alpha=0.5)
    ax.yaxis.grid(True, linestyle='--', which='minor', color='lightgrey', alpha=0.5)

#    plt.title("Average distance between article and it's first and last sections")
    plt.title(caption)
    fig3.savefig(f_name)

################################################################################
def fig4(data) :
#    print data
    fig4 = plt.figure(4, figsize=(16,16))

    data2 = map(float, data)

    plt.boxplot(data2, showmeans=True)

    ax = plt.gca()
#    plt.minorticks_on()
    ax.yaxis.grid(True, linestyle='-', which='major', color='grey', alpha=0.5)
    ax.yaxis.grid(True, linestyle='--', which='minor', color='lightgrey', alpha=0.5)

    plt.title('Distance between all "conclusion"-sections of corpus')
    fig4.savefig('/data/pulp/plots/dist/hel_last_box.png')

################################################################################
def fig5(data) :
    fig = plt.figure(1, figsize=(16,16))
    data = [map(float, l.split()[1:-1]) for l in data if len(l.split()[1:-1]) > 0]
    data = map(np.mean, data)

    plt.boxplot(data, showmeans=True)

    ax = plt.gca()
#    plt.minorticks_on()
    ax.yaxis.grid(True, linestyle='-', which='major', color='grey', alpha=0.5)
    ax.yaxis.grid(True, linestyle='--', which='minor', color='lightgrey', alpha=0.5)

    plt.title("Average distance between article and it's 'middle' sections")
    fig.savefig('/data/pulp/plots/dist/hel_middle_box.png')

################################################################################
def basicbox(data, caption, f_name) :
    with open(data, 'r') as d_file :
        data = d_file.read().split('\n')
        data = [float(i)  for i in data if isfloat(i)]
        print 'data is read '
        print type(data)
    d_file.closed

    fig = plt.figure(1, figsize=(16,16))

#    data = map(float, data)
    print 'plotting............'
    plt.boxplot(data, showmeans=True)

    ax = plt.gca()
#    plt.minorticks_on()
    ax.yaxis.grid(True, linestyle='-', which='major', color='grey', alpha=0.5)
    ax.yaxis.grid(True, linestyle='--', which='minor', color='lightgrey', alpha=0.5)

    plt.title(caption)
    fig.savefig(f_name)

################################################################################

def sample_plot(data, caption, f_name) :
    lc = int(check_output(['wc', '-l', data]).split()[0])
#    print lc
    sample = list(rnd(lc, lc/5, replace=False))
    sample.sort()
#    print sample
    with open(data, 'r') as d_file :
        new_data = []
        n = 0
        i_sample = 0
        n_sample = sample[i_sample]
        while True :
            if n == n_sample :
                line = d_file.readline()
                if not line : break
                print line 
                new_data.append(float(line))
                i_sample += 1
                if i_sample >= len(sample) : break
                n_sample = sample[i_sample]
            n += 1     

    d_file.close

#    data = map(float, data)
#    data = pd.Series(data)
#    data = rnd(data, 1000000000, replace=False)
    
    print '%d samples ommited randomly from dataset.\nConverting to float' % len(new_data)

#    data = [float(i)  for i in new_data if isfloat(i)]
#    print len(data)       
    print 'plotting.....'
    
    fig = plt.figure(1, figsize=(16,16))
    plt.boxplot(new_data, showmeans=True)

    ax = plt.gca()
#    plt.minorticks_on()
    ax.yaxis.grid(True, linestyle='-', which='major', color='grey', alpha=0.5)
    ax.yaxis.grid(True, linestyle='--', which='minor', color='lightgrey', alpha=0.5)

    plt.title(caption)
    fig.savefig(f_name)

################################################################################

def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False 


def main(argv) :

    
    ladata = argv[1:-2]
    data = ladata[:len(ladata)/2]
    print data
    labels = ladata[len(ladata)/2:]
    print labels
    f_name = argv[-2]
    print f_name
    caption = argv[-1]
    print caption

#    basicbox(data, caption, f_name)
    combobox(data,labels,f_name,caption)

    pass


if __name__ == "__main__":
    main(sys.argv)
    
