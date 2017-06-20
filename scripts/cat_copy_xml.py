from subprocess import call
from os import system as s
import sys, os


def cat_copy(line) :
    line =  line.strip()
    arx_id, path = line.split(',')

    if path.rfind('.xml') == -1 :
        do_cat = 'cat '+path+'/*.xml >> '+a_dir + arx_id+'.xml'
        s(do_cat)
        print '{} catenated'.format(arx_id)
    else :
        do_cp = 'cp ' + path + ' ' + a_dir
        s(do_cp)
        print '{} copied'.format(arx_id)


argv = sys.argv
if len(argv) != 3 :
    print '**Usage ', argv[0], ": <'paths' file> <path to store xml files>."
    sys.exit()

paths = argv[1]
a_dir = argv[2]

try:
    os.makedirs(a_dir)
except os.error:
    pass

with open(paths, 'r') as f :
    map(cat_copy, f.readlines())
f.closed
