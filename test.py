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

n = len(arr)
for i in xrange(n+1):
    print i % n


print arr[0:5]
    

