import pandas as pd
from pandas import read_csv
# Force matplotlib to not use any Xwindows backend.
#matplotlib.use('Agg')
from bs4 import BeautifulSoup as soup
import math, io, re, sys, os
import subprocess as sh
from os import system as sym


def title(html_soup) :
    tbody = html_soup.find('tbody')
    for tr in tbody('tr') :
        th = tr.th.string
        i = -1 
        for td in tr.findAll('td') :
            if i > -1 :
                text = 'topic # '+str(i)+', article id '+th
                td['title'] = text
            i += 1
    return html_soup
  

def color_cells(html_soup) :
    for td in html_soup.findAll('td') :
        k = td.string
        k = str(255-int(float(td.string)*255))
        td['style'] = 'background-color: rgb(255,'+k+','+k+')'
    return html_soup


def tr2th(html_soup) :
    tbody = html_soup.find('tbody')
    for tr in tbody.findAll('tr') :
        td = tr.find('td')    
        new = html_soup.new_tag('th')
        new.string = td.string
        td.replace_with(new)
    return html_soup


#path = '/data/mallet_tests/from_mallet/thursday_compostion.txt'
def df2html(input_path, dest_path) :
    mega_list = pd.read_csv(input_path, delimiter='\t', names=['year','File']+[str(i) for i in range(50)], na_values=[''], engine='c')
    mega_list.File= mega_list.File.str[5:]
#    print mega_list.iloc[0:7, 0:4]

    wc = mega_list.File.apply(lambda x : os.popen("wc -w < "+str(x)).read())
    mega_list.insert(loc=2, column='wc', value=wc)
    mega_list.wc = mega_list.wc.str[:-1]

    mega_list.File = mega_list.File.str.split('/').str[-1].str[:-4]
#    mega_list.sort_values('File',inplace=False)
#    print mega_list.iloc[0:7, 0:4]

    mega_list.year = mega_list.File.apply(lambda x : re.search("(\d\d)", str(x)).group(0))
    mega_list.set_index(mega_list.File, inplace=True)
#    print mega_list.iloc[0:7, 0:4]

    years = mega_list.year.unique()
    for y in years :
        with io.open(dest_path+'_'+y+'.html', 'w', encoding='utf-8') as tbl :
            df = mega_list[mega_list.year==y]
            df.drop(['year','File'], inplace=True, axis=1)
            print 'year ', y, 'shape ', df.shape
#            print df.iloc[0:7, 0:4]

            html_soup = soup(df.to_html(), 'lxml')
            print 'HTML to soup: done'
    
            tr2th(html_soup)        
            tbl.write(unicode(color_cells(title(html_soup)).prettify('utf8')))
        tbl.closed
    return 'done transforming'


def main(argv):
    if len(argv) != 3 :
        print '**Usage: ', argv[0], ' <input path> <output path>'
        sys.exit()

    in_path = argv[1]
    dest_path = argv[2]

#    if not os.path.exists(dest_path) :
#        os.makedirs(dest_path)

#    if dest_path[len(dest_path)-1] != '/' :
#        dest_path += '/'

    out = df2html(in_path, dest_path)

    print out
    pass


if __name__ == "__main__":
    main(sys.argv)

