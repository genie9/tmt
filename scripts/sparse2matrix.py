from gensim import matutils as mat
import os, sys, io, re, math
import pandas as p
import numpy as n

def sparse2matrix(inpath1, inpath2, topics_num, file_name) :
    destpath = '/data/mallet_tests/hellinger/tmp_matrice_'+topics_num+'_'+file_name

    with open(inpath1, 'r') as comparator :
        with io.open(inpath2, 'r') as comparable :
            i = 0
            
            for line_tor in comparator :
                print line_tor.split()[:2]
                l_tor = line_tor.split()[2:]
                l_tor = tuple( (tuple (map (int, (i.split(':')))) for i in l_tor))
#                    print l_tor
                len_tor = int(topics_num.split('x')[0])
                mat_tor = mat.sparse2full(doc=l_tor,length=len_tor)

                for line_ble in comparable :
                    print line_ble.split()[:2]
                    l_ble = line_ble.split()[2:]
                    l_ble = tuple( (tuple (map (int, (i.split(':')))) for i in l_ble))
#                    print l_ble
                    len_ble = int(topics_num.split('x')[1])
                    mat_ble = mat.sparse2full(doc=l_ble,length=len_ble)
                    
                    matrix = n.zeros(shape=(len_tor,len_ble))

                    for i in xrange(len_tor) :
                        for j in xrange(len_ble) :
                            matrix[i][j] = pow((math.sqrt(mat_tor[i]) - math.sqrt(mat_tor[j])),2)
                    
                    with open(destpath+'_'+line_tor.split()[1]+'.txt', 'w') as matrixfile :
                        matrixfile.write(str(mat.full2sparse(matrix)))
                    matrixfile.closed
                    print 'word %d done' % i                                        
                    i += 1

        comparator.closed
    comparable.closed
    
    print 'matrixes done'


def main(argv):
    
#    if len(argv) != 3 :
#        print '**Usage: ', argv[0], ' <input path comparator> <topics num> <input path comparable> <topics num> <output file name> '
#        sys.exit()
    
    inpath1 = '/data/mallet_tests/from_mallet/test/full4/full_50_wordcounts.txt' #argv[1]
    inpath2 = '/data/mallet_tests/from_mallet/test/full4/full_200_wordcounts.txt'
    topics_num = '50x200'
    file_name = 'test1' #argv[2]

#    if not os.path.exists(dest_path) :
#        os.makedirs(dest_path)
#
#    if dest_path[len(dest_path)-1] != '/' :
#        dest_path += '/'
    
    sparse2matrix(inpath1, inpath2, topics_num,file_name)
    
    pass


if __name__ == "__main__":
    main(sys.argv)


