import ga2 as ga
import mutations as mut
import random


print '*** Partition Problem ***'

class DiffArr (ga.Individual):
    def __init__(self, *args):
        super(self.__class__, self).__init__(*args)
        self.arr = args[0]
                           

    def __str__(self):
        self.printresult(True)
        return super(self.__class__, self).__str__()
        
            
    def calcx(self):
        sumx = 0
        try:
            for i in xrange(self.count):
                if self[i].val == 0:
                    sumx += self.arr[self[i].id]
                else:
                    sumx -= self.arr[self[i].id]
            return sumx
        except:
            print self[i].id, len(self.arr)
        

    foofx = lambda self, x: x**2

    def randomcreate(self, best=None):
        for i in xrange(len(self.arr)):
            g = self.addgen()
            g.val = 1 #random.randint(0,1)

        self.fitness()

    def printresult(self, short):
        a1, a2 = 0, 0
        for i in xrange(self.count):
            if self[i].val == 0:
                a1 += 1
            else:
                a2 += 1
        print 'Length arr1', a1, 'arr2', a2

        if not short:
            a, b = [], []
            for i in xrange(self.count):
                if self[i].val == 0:
                    a.append(self.arr[self[i].id])
                else:
                    b.append(self.arr[self[i].id])
            print 'Delta Arr ', sum(a) - sum(b), ' Sum Arr1', sum(a) , 'Sum Arr2', sum(b), 
            a.sort(); b.sort()    
            print 'arr 1 ', a[:15]
            print 'arr 2 ', b[:15] 
            
            
arr = [random.randint(0, 5000) for x in xrange(0,1000)]
partitionproblem = ga.Evolution(size = 150, iteration = 20, 
              generatemutation = 30, populationratemutation = 80, ClassIndividual = DiffArr,
              MutationsClasses = [mut.Crossingover, mut.MRand], args = [arr])


partitionproblem.calc()
partitionproblem.population.best.printresult(False)
print "It's more thins setting"
partitionproblem.populationsize = 180
partitionproblem.generatemutation = 0.1
partitionproblem.iteration = 20
partitionproblem.generation()
partitionproblem.calc()
partitionproblem.population.best.printresult(False)

print '*** string searsh ****'

alphabet = list('MSHBqwertyuiopasdfghjklzxcvbnm.,!') + [' ']

def levenshtein_distance(seq_x, seq_y):
    """ compute global or local alignment matrix """

    cam = [0]
    current = [0]

            
    if seq_x < seq_y:
            seq_x, seq_y = seq_y, seq_x 

    lx, ly = len(seq_x), len(seq_y)

    for j in xrange(1, ly+1):
            cam.append(j)
            current.append(0)

    change = lambda a, b:  0 if a == b else 1

    for i in xrange(1, lx+1):
            current[0] = i
            for j in xrange(1, ly+1):
                    cxy = cam[j-1] + change(seq_x[i-1], seq_y[j-1]) 
                    cx_ = current[j-1] + 2
                    c_y = cam[j] + 2

                    current[j] = min([cxy, cx_, c_y])

            cam = [x for x in current]
                    
    return cam[ly]

class Sstting (ga.Individual):
    def __init__(self, *args):
        super(self.__class__, self).__init__(*args)
        self.sword = args[0]
                           

    def __str__(self):
        print self.printresult(True)
        return super(self.__class__, self).__str__()
        
            
    def calcx(self):
        word = ''
        for  s in self.dna:
            word += s.val

        return levenshtein_distance(self.sword, word)
        
    foofx = lambda self, x: 5**x

    def randomcreate(self, best=None):
        n = len(alphabet)
        for i in xrange(len(self.sword)):
            g = self.addgen()
            j = random.randint(0,n-1)
            g.val = alphabet[j]

    def printresult(self, short):
        res = ''
        for s in self.dna:
            res += str(s.val)

        return "\r message: {0}".format(res)


class MChange (mut.Mutation):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = 'Change'
        
    def mutate(self, individual, cnt, population):
        n = len(alphabet)
        for i in xrange(cnt):
            idx = random.randint(0, individual.count-1)
            j = random.randint(0,n-1)
            individual[idx].val = alphabet[j]

class MDelIns (mut.Mutation):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = 'MDelIns'
        
    def mutate(self, individual, cnt, population):
        n = len(alphabet)
        for i in xrange(cnt):
            idx1 = random.randint(0, individual.count-1)
            idx2 = random.randint(0, individual.count-1)
            val = individual[idx1].val    

            for j in xrange(min(idx1, idx2), max(idx1, idx2)):    
                individual[j].val = individual[j+1].val    

            individual[idx2].val = val

class MDel (mut.Mutation):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = 'MDel'
        
    def mutate(self, individual, cnt, population):
        n = len(alphabet)
        idx = random.randint(0, individual.count-1)
        del individual.dna[idx]

class MIns (mut.Mutation):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = 'MIns'
        
    def mutate(self, individual, cnt, population):
        n = len(alphabet)
        g = individual.addgen()
        j = random.randint(0,n-1)
        g.val = alphabet[j]
        individual.dna.append(g)


s = 'Marchelo teaches Savelys evolution biology. Happy Birthday!!!'
ss = ga.Evolution(size = 1000, iteration = 90, 
               generatemutation = 25, populationratemutation = 80, ClassIndividual = Sstting,
               MutationsClasses = [mut.Crossingover, MChange, MDelIns, MDel, MIns], args = [s])

ss.calc()
print "It's more thins setting"
ss.populationsize = 5000
ss.generatemutation = 12
ss.iteration = 40
ss.generation()
ss.calc()

print 1/0
    
    
    
    
    
