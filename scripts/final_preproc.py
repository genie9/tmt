import pandas as pd
import sys, os, io
import subprocess


dest_path = ''
junk = ''
e_file = ''
i = 0

def start(in_path,opt) :
    global i
    i = 0
    
    print 'processing files in {}{}'.format(in_path,opt)

    if not os.path.exists(dest_path+opt) :
        os.makedirs(dest_path+opt)

    try :
        a = os.listdir(in_path+opt)
        map(lambda x : txt_match(in_path,opt,x), a)
    
    except IOError as e :
        print e
        a = subprocess.check_output( \
                ["find", in_path+opt, "-maxdepth", "2", "-mindepth", "2", "-type", "f"])
        map(lambda x : txt_match(x.rsplit('/',1)[0]+'/', opt, x.rsplit('/',1)[1]), a.split())
    return len(a)

def txt_match(in_file, opt, doc) :
    global i, dest_path, junk, e_file
    
    s = pd.Series(open(in_file+opt+doc).read().split())

    s_len = s.size

    s = s[-s.isin(junk)].str.cat(sep=' ')

    s_len = len(s.split())

    if s_len < 50 :
        print 'length %d'%s_len
        with open(e_file, 'a') as e :
            e.write(doc+','+str(s_len)+'\n')
        e.closed
        print '%s added to error file'%doc
        return
    
    i +=  1
    dest_file = dest_path + opt + doc
    
    with io.open(dest_file, 'w', encoding='utf8') as clean_txt :
        clean_txt.write(unicode(s)+'\n')
    clean_txt.closed
    
    if i%100==0 :
        print i

################################################################


def main(argv):
    global dest_path, junk, e_file, i

    if len(argv) != 5 :
        print '**Usage: ', argv[0], '<input path> <output path> <stopwords file> <error file>'
        sys.exit()
    
    in_path = argv[1]
    dest_path = argv[2]
    junk = argv[3]
    e_file = argv[4]

    junk = pd.Series(open(junk).read().split()+['let'])
#    print junk
    if not os.path.exists(dest_path) :
        os.makedirs(dest_path)

    if dest_path[len(dest_path)-1] != '/' :
        dest_path += '/'
    
    with open(e_file, 'a') as e :
        e.write('# added during final processing\n')
    e.closed

    full = start('{}'.format(in_path),'full/')
    j = i
    sect = start('{}'.format(in_path),'sect/')

#    print 'processed {} full articles and {} sections'.format(j,i)
    print 'saved {}/{} full articles'.format(j,full)
    print 'saved {}/{} sections of articles'.format(i,sect)
    pass


if __name__ == "__main__":
    main(sys.argv)
