import pandas as pd
import sys, os, io
import subprocess


i = 0
def txt_match(in_file, doc, dest_path, junk) :
    global i

    s = pd.Series(open(in_file+doc).read().split())

    s_len = s.size

    if s_len < 10 :
        print '%s is a error file'%doc
        print 'length %d'%s_len
        return

    s = s[-s.isin(junk)].str.cat(sep=' ')

    s_len = len(s.split())

    if s_len < 10 :
        print 'length %d'%s_len
        with open('/data/mallet_tests/support/errorfiles_last.txt', 'a') as e_file :
            e_file.write(doc+','+str(s_len)+'\n')
        e_file.closed
        print '%s added to error file'%doc
        return
    
    i +=  1
    dest_file = dest_path + doc

    with io.open(dest_file, 'w', encoding='utf8') as clean_txt :
        print 'saving to ', clean_txt.name
        clean_txt.write(unicode(s)+'\n')
    clean_txt.closed
    
    print i

################################################################


def main(argv):
    
    if len(argv) != 4 :
        print '**Usage: ', argv[0], '<input path> <output path> <stopwords file>'
        sys.exit()
    
    in_path = argv[1]
    dest_path = argv[2]
    junk_file = argv[3]

    junk = pd.Series(open(junk_file).read().split()+['let'])

    if not os.path.exists(dest_path) :
        os.makedirs(dest_path)

    if dest_path[len(dest_path)-1] != '/' :
        dest_path += '/'
    
            
    try :
        a = os.listdir(in_path)

        map(lambda x : txt_match(in_path, x, dest_path, junk), a)
    
    except IOError as e :
        a = subprocess.check_output(["find", in_path, "-maxdepth", "2", "-mindepth", "2", "-type", "f"])
        
        map(lambda x : txt_match(x.rsplit('/',1)[0]+'/', x.rsplit('/',1)[1], dest_path, junk), a.split())
    pass


if __name__ == "__main__":
    main(sys.argv)
