import math

class A:
    def __init__(self):
        self.a = 1

    def clone(self):
        return self.__class__()


d = {5:4, 4:5}
del d[5]
print 'ddd', d


    
b = A()
b.a = 5

c = b.clone()
print b.a, c.a

arr = [1,2,3,4,5]
print 'arr', arr[4:6]

for i in xrange(0, len(arr) - 2):
    for j in xrange(i+2, len(arr)):
        print arr[i], arr[i+1], arr[j], arr[(j+1) % len(arr)]

for idx in xrange(len(arr)):
    arr += [idx]

print arr
           
print "save"


