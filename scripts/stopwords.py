import re, sys


def stopwords(inpath, destpath) :
    r = '([0-9]+:[1-3]|$)'
    with open(inpath, 'r') as data :
        with open(destpath, 'w') as stopwords :
            for line in data :
                l = line.split()
                if len(l) == 3 :
                    s = l[2]
                    if len(re.sub(r,'',s)) == 0 :
                        stopwords.write(l[1]+'\n')
        stopwords.closed
    data.closed


def main(argv) :
    if len(argv) != 3 :
        print '**Usage ', argv[0], '<word list file> <output file>'
        sys.exit()

    in_file = argv[1]
    dest_file = argv[2]

    stopwords(in_file, dest_file)
    
    pass

if __name__ == "__main__":
    main(sys.argv)
