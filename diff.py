

with open('/data/mallet_tests/to_mallet/full4/0706.0502.txt') as path1 :
    with open('/data/mallet_tests/to_mallet/full3/0706.0502.txt') as path2 :
        a = path1.read().split()
        b = path2.read().split()
        print a
        print b
        print [i for i in b if i not in a]
    path2.closed
path1.closed
