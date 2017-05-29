from subprocess import call
from os import system as s
import sys, os


def cat_copy(line) :
    line =  line.strip()
    arx_id, path = line.split(',')

    if path.rfind('.xml') == -1 :
        do_cat = 'cat '+path+'/*.xml >> '+path_cs + arx_id+'.xml'
        s(do_cat)
        print '{} catenated'.format(arx_id)
    else :
        do_cp = 'cp ' + path + ' ' + path_cs
        s(do_cp)
        print '{} copied'.format(arx_id)


argv = sys.argv
if len(argv) != 2 :
    print '**Usage ', argv[0], ': <work folder>.'
    sys.exit()

root = argv[1]

path_cs = "{}arXiv_raw/".format(root)

try:
    os.makedirs(path_cs)
except os.error:
    pass

with open("{}paths.csv".format(root), 'r') as f :
    map(cat_copy, f.readlines())
f.closed
