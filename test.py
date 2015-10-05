import math

class A:
    def __init__(self):
        self.a = 1

    def clone(self):
        return self.__class__()


    
b = A()
b.a = 5

c = b.clone()
print b.a, c.a

arr = [1,2,3,4,5]

for i in xrange(0, len(arr) - 2):
    for j in xrange(i+2, len(arr)):
        print arr[i], arr[i+1], arr[j], arr[(j+1) % len(arr)]

for idx in xrange(len(arr)):
    arr += [idx]

print arr
           
print "save"

lst = [1,2,3,4]
print lst[None:None]
