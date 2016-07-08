import pandas as pd
from pandas import read_csv
# Force matplotlib to not use any Xwindows backend.
#matplotlib.use('Agg')
from bs4 import BeautifulSoup as soup
import math, io

path = '/data/mallet_tests/from_mallet/thursday_compostion.txt'

mega_list = pd.read_csv(path, delimiter='\t', names=['#','File']+[str(i) for i in range(50)], na_values=[''])
#mega_list['File'] = mega_list.File.str[mega_list.File.str.rfind('/')+1::]
file_list = mega_list.File
file_list = file_list.str[file_list.str.rfind('/')+1::]
mega_list = mega_list.drop(['#','File'], axis=1)
print mega_list.iloc[1:5,]
print mega_list.shape

with io.open('/data/mallet_tests/from_mallet/thursday_table.html', 'w', encoding='utf-8') as tbl :
#    ht = mega_list.to_html()
#    print 'data frame to HTML: done'
#    tbl.write(ht)
    s = soup(mega_list.to_html(), 'lxml')
    print 'HTML to soup: done'

#    j = 0
#    for tr in s.findAll('tr') :
#    i = 0
    for cell in s.findAll('td') :
#            if i != 0 and i != 1 :
#                k = cell.string
                #print cell
            k = str(255-int(float(cell.string)*255))
            cell['style'] = 'background-color: rgb(255,'+k+','+k+')'
#                print 'cell colored: k = ', k
#            i += 1
#            print 'col #', i
#        j += 1
#        print 'row #', j
#        tr.decompose()
    ht = unicode(s.prettify('utf8'))
    tbl.write(ht)
tbl.closed
