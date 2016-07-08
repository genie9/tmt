from subprocess import call
from os import system as sys
import json


path_cs = "/data/mallet_tests/arXiv_cs/"

with open("/home/evly/tmt/bigdata/file_matrix.json", 'r') as j_data :
    data = json.loads(j_data.read())
    for item in data :
        path_dir = item.get('path')+'/' 
        print 'path ', path_dir
        num = item.get('id')
        if path_dir.rfind('.xml/') == -1 :
            do_cat = 'cat ' + path_dir+ '*.xml >> ' + path_cs + num + ".xml"
            print 'id ', num, ' catenated'
            sys(do_cat)
        else :
#            path_dir = path_dir[:-1] 
            do_cp = 'cp ' + path_dir[:-1] + ' ' + path_cs
            sys(do_cp)
            print 'id ', num, ' copied'
j_data.closed
