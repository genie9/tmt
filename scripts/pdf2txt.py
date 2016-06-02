#!/usr/bin/python

print """Hello, CaSCo!
It's a nice day."""

# iterator
ilist = [1,2,3,4,5]
ilist = [x+1 for x in ilist]

for i in ilist:
	print(i)

print "printit"
print(next(iter(ilist)))
print(len(ilist))

print "generator"
glist = (1,2,3,4,5)
glist = (i*2 for i in glist)

for i in glist:
	print(i)

def testgen(n):
	count, g = 0, 1
	while True:
		if(count > n):
			return
		yield g
		g += count
		count += 1

tg = testgen(6) 
	
for g in tg:
	print(g)

print(tg)
# not working
# print(glist[0])
# print(len(glist))


