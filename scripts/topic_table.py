import pandas as pd
from pandas import read_csv
# Force matplotlib to not use any Xwindows backend.
#matplotlib.use('Agg')
from bs4 import BeautifulSoup as soup
import math, io, re, sys, os, gc
import subprocess as sh
from os import system as sym



def process(html_soup) :
    tbody = html_soup.find('tbody')
    print 'body found'
    trs = tbody.findAll('tr')
    print 'tr-tags found'
    for tr in trs :
        th = tr.th.string
        print 'document name ', th
        td2th(tr, html_soup.new_tag('th'))
        print 'wordcount cell bolded'
        tds = tr.findAll('td')
        print 'cells found'
        title(th, tds)
        print 'hoovering created'
        color_cells(tds)      
        print 'cells colored'    
    return html_soup

def title(th, tds) :
    i = 0
    for td in tds :
        text = 'topic # '+str(i)+', article id '+ th
        td['title'] = text
        i += 1

def td2th(tr, new_tag) :
    td = tr.find('td')    
    new_tag.string = td.string
    td.replace_with(new_tag)
    return tr

def color_cells(tds) :
    for td in tds :
        k = str(255-int(float(td.string)*255))
        td['style'] = 'background-color: rgb(255,'+k+','+k+')' 
        

#def title(html_soup) :
#    tbody = html_soup.find('tbody')
#    for tr in tbody('tr') :
#        th = tr.th.string
#        i = 0 
#        for td in tr.findAll('td') :
##            if i > -1 :
#            text = 'topic # '+str(i)+', article id '+th
#            td['title'] = text
#            i += 1
#    return html_soup
  

#def color_cells(html_soup) :
#    for td in html_soup.findAll('td') :
#        k = td.string
#        k = str(255-int(float(td.string)*255))
#        td['style'] = 'background-color: rgb(255,'+k+','+k+')'
#    return html_soup


#def td2th(html_soup) :
#    tbody = html_soup.find('tbody')
#    for tr in tbody.findAll('tr') :
#        td = tr.find('td')    
#        new = html_soup.new_tag('th')
#        new.string = td.string
#        td.replace_with(new)
#    return html_soup


#path = '/data/mallet_tests/from_mallet/thursday_compostion.txt'
def df2html(input_path, dest_path, topics) :
    mega_list = pd.read_csv(input_path, delimiter='\t', names=['year','File']+[str(i) for i in range(topics)], na_values=[''], engine='c')
    mega_list.File= mega_list.File.str[5:]
#    print mega_list.iloc[0:7, 0:4]
    print 'dataframe created'

    wc = mega_list.File.apply(lambda x : len(open(str(x),'r').read().split()))
    mega_list.insert(loc=2, column='wc', value=wc)
#    mega_list.wc = mega_list.wc.str[:-1]
    print 'word count done'

    mega_list.File = mega_list.File.str.split('/').str[-1].str[:-4]
#    mega_list.sort_values('File',inplace=False)
#    print mega_list.iloc[0:7, 0:4]

    mega_list.year = mega_list.File.apply(lambda x : re.search("(\d\d)", str(x)).group(0))
    mega_list.set_index(mega_list.File, inplace=True)
#    print mega_list.iloc[0:7, 0:4]
    print 'years added'

    years = mega_list.year.unique()
    for y in years :
        df = mega_list[mega_list.year==y]
        df.drop(['year','File'], inplace=True, axis=1)
        print 'year ', y, 'shape ', df.shape
#            print df.iloc[0:7, 0:4]
    
        html = df.to_html()
        html = soup(html, 'lxml')
        print 'HTML to soup: done'

        html = process(html) 

        with io.open(dest_path+'_'+y+'.html', 'w', encoding='utf-8') as tbl :
            print 'writting to file'+tbl.name
            html = html.prettify('utf8')
            html = unicode(html)
            tbl.write(html)
        tbl.closed
        gc.collect()
        print 'done'
    return 'done transforming'


def main(argv):
    if len(argv) != 4 :
        print '**Usage: ', argv[0], ' <input path> <output path> <num of topics>'
        sys.exit()

    in_path = argv[1]
    dest_path = argv[2]
    topics = int(argv[3])

    if not os.path.exists(dest_path) :
        os.makedirs(dest_path)

#    if dest_path[len(dest_path)-1] != '/' :
#        dest_path += '/'

    out = df2html(in_path, dest_path, topics)

    print out
    pass


if __name__ == "__main__":
    main(sys.argv)

