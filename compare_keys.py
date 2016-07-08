



keys_1 = '/data/mallet_tests/from_mallet/thursday_keys.txt'
keys_2 = '/data/mallet_tests/from_mallet/monday_keys.txt'

with open(keys_1) as list_sec :
    with open(keys_2) as list_art :
#        comp = []
        sec_matrix = [line.split().sort() for line in list_sec]
        art_matrix = [line.split().sort() for line in list_art]
        for i in range(50) :
            for j in range(2:22) :
                sec_matrix[j,i] 
                    for i in range(2,22) :
                    if s[i] == a[i] :
                        comp[i] = uppercase(s[i]) 
                    else              
    list_art.closed
list_sec.closed
