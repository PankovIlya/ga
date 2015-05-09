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

print arr[0:5]
    

