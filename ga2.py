import random, operator, math

coRandom = 0
coBest = 1
CrossingoverType = set ([coRandom, coBest])

muRandom = 0
muStatic = 1
MutationType = set ([muRandom, muStatic])

dsID = 0
dsVal = 1
cmp_id = lambda g1, g2: cmp(g1.id, g2.id) #or cmp(g1.Cour, g2.Cour)
cmp_val = lambda g1, g2: cmp(g1.val, g2.val) #or cmp(g1.Cour, g2.Cour) 
SortType = {dsID:cmp_id, dsVal:cmp_val}

otMin = 0
otMax = 1
optmin = lambda x: 1.0/(x+1.0)
optmax = lambda x: x
OptimisationType = {otMin:optmin, otMax:optmax}


class Gene (object):
    def __init__(self):
      self._id = 0 
      self.val = 0
      
    id = property(lambda self: self._id)

class Individual (object):
    def __init__(self, *args):
        self._sorttype = dsID
        self.dna = []
        self._x = 0
        self._fx = 0
        self._args = args
        
    def __getitem__(self, idx):
        return self.dna[idx]

    def __setitem__(self, idx, val):
         self.dna[idx] = val 
    
    def __str__(self):
        return 'x ' + str(self.x) + ' fx ' + str(self.fx)

    def __getslice__(self, n, m):
        self.ordid()
        dna = []
        for itm in self.dna[n:m]:
            gene = Gene()
            gene._id, gene.val = itm.id, itm.val
            dna += [gene]
        return dna

    x = property (lambda self: self._x) 

    foofx = lambda self, x : 'This is Abstract Method'

    getfx = lambda self: self._fx

    def setfx(self, x):
        self._fx = self.foofx(x)
    
    fx = property(getfx, setfx)

    count = property(lambda self: len(self.dna))

    def checksorttype(foo):
        def check(self, val):
            if not(val in SortType):
                raise Exception('Unknown csort type', SortType)
            return foo(self, val)
        return check
        
    @checksorttype
    def setst(self, val):
      self._sorttype = val

    def getst(self):
      return self._sorttype

    sorttype = property (getst, setst)
  
    def ordid(self):
        if self.sorttype != dsID:
            self.sorttype = dsID
            self.dna.sort(cmp = SortType[self.sorttype])
            

    def ordval(self):
        if self.sorttype != dsVal:
            self.sorttype = dsVal
            self.dna.sort(cmp = SortType[self.sorttype])

    def addgen(self):
        g = Gene()
        self.add(g)
        g._id = self.count-1
        return g

    def add(self, gene):
        self.dna.append(gene)

    def fitness(self):
        self._x = self.calcx()
        self.fx = self.x
        return self.fx
        
    def calcx(self):
        raise Exception('Absract method, return x')

    def randomcreate(self):
         raise Exception('Absract method, fill DNA')

    def clone(self):
        clone = self.__class__(*self._args)
        clone.dna = self[0:]
        clone.fitness()
        return clone
        
            
class Population (object):
    def __init__(self, bestprotected = True, opt_type = otMin,
                 ClsInd = None, args = [], calc_fitness = True,
                 rate_procent = 0.1, best_population_rate = 0.08):
        self.bestprotected = bestprotected
        self.args = args
        self.optimisationtype = opt_type
        self.ClsInd = ClsInd
        self.calc_fitness = calc_fitness
        self.success_list = []
        self.individuals = []
        self.min =  214748364
        self.max = -214748364
        self.best = None
        self.sumx = 0
        self.sumfx = 0
        self.sumoptfx = 0.0
        self.optfoo = OptimisationType[opt_type]
        self.rate_procent = rate_procent
        self.best_population_rate = best_population_rate
        self.best_population_idx = 0

    def clone(self):
        children = self.__class__(self.bestprotected, self.optimisationtype, self.ClsInd, self.args)
        children.min = self.min
        children.max = self.max
        children.best = self.best.clone()
        children.individuals += [self.best.clone()]

        return children

  
    def init(self):
        self.best = self.conceiving()
        self.add(self.best)
        self.best.randomcreate()
        self.best.fitness()
        
            
    def __getitem__(self, idx):
        return self.individuals[idx]

    def conceiving(self):
        ind = self.ClsInd(*self.args)
        return ind
         
    def add(self, ind):
        return self.individuals.append(ind) 

    count = property(lambda self: len(self.individuals))

                   
    #min, max, sum - x, fx
    def extreme(self):

        self.sumx, self.sumfx, self.sumoptfx = 0, 0, 0.0
        vbest = self.best

        for ind in self.individuals:
            if self.calc_fitness:
                ind.fitness()
            if ind.fx < self.min:
                self.min = ind.x    
            if ind.fx > self.max:
                self.max = ind.fx
            if self.selection(self.best, ind) == 1: 
                self.best = ind
            self.sumx += ind.x
            self.sumfx += ind.fx
                
            self.sumoptfx += self.optfoo(ind.fx)

        if self.selection(self.best, vbest) == 1: 
            self.best = vbest.clone()

        #print [i.fx for i in self.individuals]  


    def selection(self, ind1, ind2):
        ofx1, ofx2 = self.optfoo(ind1.fx), self.optfoo(ind2.fx)
        if self.optimisationtype == otMin:
            return cmp(ofx2, ofx1)
        else:
            return cmp(ofx1, ofx2)

    def rang(self, group):
        group.sort(cmp = self.selection)       
     
    def foosuccessrate(self, rate):
        if self.sumoptfx == 0:
            return float(1/self.count)
        else:
            return float(rate/self.sumoptfx)
            

    cround = staticmethod(lambda x: round(x,5))

    def rate(self):
        def find(val):
            for i in xrange(self.count):
                if self[i].fx > val:
                    return i-1
            return self.count - 1
 
        self.csort()
        val = self.best.fx + ((self.max-self.best.fx)*self.rate_procent)
        cnt = find(val)

        if cnt < self.count*self.best_population_rate:
            cnt = int(self.count*self.best_population_rate)
            
        self.best_population_idx = cnt


    def calc(self):
        self.extreme()
        self.rate()

    def csort(self):  
        self.individuals.sort(cmp = self.selection)

    def generation(self, size):
        for _ in xrange(self.count, size):
            ind = self.conceiving()
            ind.randomcreate()
            ind.fitness()
            self.individuals.append(ind)
        self.best_population_idx = self.count - 1  
            

    def parent(self):
        i = random.randint(0, self.best_population_idx)
        return self[i]
        

class Mutation (object):
    def mutate(self, individual, cnt):
        raise Exception('Abstract method')


class Mutations (object):
    def __init__(self):
        self.mutationslist = []
        

    def __getitem__(self, idx):
        return self.mutationslist[idx]
        
    def add(self, mutation):
        self.mutationslist.append(mutation)

    count = property(lambda self: len(self.mutationslist))

    def mutagenesis(self, population, mutationtype, populationratemutation, generatemutation):

        if self.count == 0:
            return
        
        cnt_pop_mut = (population.count * populationratemutation) // 100;
                
        for _ in xrange(cnt_pop_mut):
            #select mutation
            idx_m =  random.randint(0, self.count-1)
            #select individ
            idx_i = random.randint(0, population.count - 1) 

            cnt = int(((population[idx_i].count-1)*generatemutation)//100) + 1
            if mutationtype == muRandom:
                cnt = random.randint(1, cnt) 
            
            self[idx_m].mutate(population[idx_i], cnt)

    
        

class Evolution (object):
    def __init__(self, size = 100, iteration = 25, generatemutation = 100,
                 populationratemutation = 100, mutationtype = muRandom,
                 bestprotected = True, crossingovertype = coRandom,
                 ClassIndividual = None, MutationsClass = [], args = [],
                 printlocalresult = True):
        self.populationsize = size
        self.iteration = iteration
        self.generatemutation = generatemutation
        self.populationratemutation = populationratemutation
        self.mutationtype = mutationtype
        self.bestprotected = bestprotected
        self.crossingovertype = crossingovertype
        self.printlocalresult = printlocalresult
        self.MutationCls = MutationsClass
        self.ClsInd = ClassIndividual
        self.args = args
        self.population = None
        self.mutations = []
        self.init()
        self.child_count = 2
        

    def init(self):
        self.population = Population(self.bestprotected, otMin, self.ClsInd, self.args)
        self.population.init()
        self.generation()
        self.mutations = Mutations()

        for mCls in self.MutationCls:
            self.mutations.add(mCls())

        self.population.calc()

    def generation(self):
        self.population.generation(self.populationsize)

    def calc(self):
        i = 0
        for i in xrange(self.iteration):
            self.anthropogeny()
            if self.printlocalresult:
                print 'population', i, ' best ', self.population.best
                        
            
    def anthropogeny(self):
        self.population = self.crossingover(self.population)
        self.mutation()
        self.population.calc()

    def crossingover(self, parents):

        children = parents.clone()
   
        for _ in xrange(parents.count//2):
            if self.crossingovertype == coRandom:
                vparent1 = parents.parent()
            else:
                vparent1 = parents.best() # test

            i = 0
            vparent2 = vparent1
            while vparent2 == vparent1 and i < 100:
                vparent2 = parents.parent()
                i += 1

            if i == 100:
                parents.best_population_idx
        
            for child in self.fertilisation(vparent1, vparent2):
                children.add(child)    
                
        return children


    def fertilisation(self, parent1, parent2):

        children = []
        
        for _ in xrange(self.child_count):
            children.append(self.meiosis(self.population.conceiving(), parent1, parent2))
            children.append(self.meiosis(self.population.conceiving(), parent2, parent1))

        children += [parent1.clone(), parent2.clone()] 
        self.population.rang(children)
        #print [child.fx for child in children]

        return children[:2]

    def meiosis(self, child, parent1, parent2):

        len_chr = random.randint(0, parent1.count)

        child.dna = parent1[:len_chr] + parent2[len_chr:]
        child.fitness()

        return child


    def mutation(self):
        self.mutations.mutagenesis(self.population, self.mutationtype, self.populationratemutation, self.generatemutation)

    def printbest(self):
        print self.population.best

if __name__ == "__main__":

    print '*** Min f(x) = x^2 ***'

    class X2 (Individual):
        def calcx(self):
            return reduce(lambda res, i: res + self[i].val*2**i, range(0, self.count),0)
            
        foofx = lambda self, x: x**2

        def randomcreate(self):
            for i in xrange(32):
                x = random.randint(0,1)
                g = self.addgen()
                g.val = x

    class MRand (Mutation):
        def mutate(self, individual, cnt):
            for i in xrange(cnt):
                idx = random.randint(0, individual.count-1)
                individual[idx].val = random.randint(0,1)



    min_x2 = Evolution(iteration = 20, mutationtype = muRandom,
                      generatemutation = 30, populationratemutation = 80,
                      ClassIndividual = X2,
                      MutationsClass = [MRand], printlocalresult = True)
    min_x2.init()
    min_x2.calc()

    print '*** Partition Problem ***'

    class DiffArr (Individual):
        def __init__(self, *args):
            Individual.__init__(self, *args)
            self.arr = args[0]
                               

        def __str__(self):
            self.printresult(True)
            return Individual.__str__(self)
            
                
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

        def randomcreate(self):
            for i in xrange(len(self.arr)):
                g = self.addgen()
                g.val = 1 #random.randint(0,1)

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
                
                
    arr = [random.randint(0, 50000) for x in xrange(0,10000)]
    partitionproblem = Evolution(size = 150, iteration = 20, mutationtype = muRandom,
                  generatemutation = 30, populationratemutation = 80, ClassIndividual = DiffArr,
                  MutationsClass = [MRand], args = [arr])

    partitionproblem.init()
    partitionproblem.calc()
    partitionproblem.population.best.printresult(False)
    print "It's more thins setting"
    partitionproblem.populationsize = 180
    partitionproblem.generatemutation = 0.1
    partitionproblem.iteration = 20
    partitionproblem.generation()
    partitionproblem.calc()
    partitionproblem.population.best.printresult(False)
    
    
    
    
    
