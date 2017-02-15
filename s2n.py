a=open('/data/mallet_tests/support/hel_intro.txt')

i = 0
d = ''
c = []
while True :
    b = a.read(1)
    if not b : 
        print 'EOF'
        break
    if b == ' ':
        c.append(d)
        i += 1
        print i
#        print d
        d = ''
    else : d += b

a.closed

with open('/data/mallet_tests/support/hel_intro_lines.txt','w') as a :
    a.write('\n'.join(c))
a.closed
