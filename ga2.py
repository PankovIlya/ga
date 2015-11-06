import random, operator, math
import mutations as mut
import const


class Gene (object):
    def __init__(self):
      self._id = 0 
      self.val = 0
      
    id = property(lambda self: self._id)

class Individual (object):
    def __init__(self, *args):
        self._sorttype = const.dsID
        self.dna = []
        self._x = 0
        self._fx = 0
        self._args = args
        self.sorted = False
        
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
            if not(val in const.SortType):
                raise Exception('Unknown csort type', const.SortType)
            return foo(self, val)
        return check
        
    @checksorttype
    def setst(self, val):
      self._sorttype = val

    def getst(self):
      return self._sorttype

    sorttype = property (getst, setst)
  
    def ordid(self):
        if self.sorted:
            self.sorttype = const.dsID
            self.dna.sort(cmp = const.SortType[self.sorttype])
            

    def ordval(self):
        if self.sorted:
            self.sorttype = const.dsVal
            self.dna.sort(cmp = const.SortType[self.sorttype])

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

    def randomcreate(self, v_opt=True):
         raise Exception('Absract method, fill DNA') #NotImpl

    def clone(self):
        clone = self.__class__(*self._args)
        clone.dna = self[0:]
        clone.fitness()
        return clone
        
            
class Population (object):
    def __init__(self, populationsize = 100, bestprotected = True, opt_type = const.otMin,
                 ClsInd = None, args = [], calc_fitness = True,
                 rate_procent = 0.25, best_population_rate = 0.25):
        self.populationsize = populationsize 
        self.bestprotected = bestprotected
        self.args = args
        self.optimisationtype = opt_type
        self.ClsInd = ClsInd
        self.calc_fitness = calc_fitness
        self.success_list = []
        self.population = []
        self.min = float('inf')
        self.max = -float('inf')
        self.best = None
        self.sumx = 0
        self.sumfx = 0
        self.sumoptfx = 0.0
        self.optfoo = const.OptimisationType[opt_type]
        self.rate_procent = rate_procent
        self.best_population_rate = best_population_rate
        self.best_population_idx = 0
        self.elite = []

    def clone(self):
        children = self.__class__(self.bestprotected, self.optimisationtype, self.ClsInd, self.args)
        children.min = self.min
        children.max = self.max
        children.best = self.best.clone()
        children.population += [self.best.clone()]

        return children
  
    def init(self):
        self.best = self.conceiving()
        self.add(self.best)
        self.best.randomcreate()
        self.best.fitness()
        self.after_best_create(self.best)
        self.elite = {}

    def after_best_create(self, best):
        pass        
            
    def __getitem__(self, idx):
        return self.population[idx]

    def __setitem__(self, idx, val):
        self.population[idx] = val

    def __getslice__(self, n, m):
        return self.population[n:m]

    def conceiving(self):
        ind = self.ClsInd(*self.args)
        return ind
         
    def add(self, ind):
        return self.population.append(ind) 

    count = property(lambda self: len(self.population))

    def __getslice__(self, n, m):
        return self.population[n:m]
    
    #min, max, sum - x, fx
    def extreme(self):

        self.sumx, self.sumfx, self.sumoptfx = 0, 0, 0.0
        vbest = self.best

        for ind in self.population:
            if self.calc_fitness:
                ind.fitness()
            if ind.fx < self.min:
                self.min = ind.x    
            if ind.fx > self.max:
                self.max = ind.fx
            if self.selection(vbest, ind) == 1: 
                vbest = ind
            self.sumx += ind.x
            self.sumfx += ind.fx
                
            self.sumoptfx += self.optfoo(ind.fx)

        if self.selection(self.best, vbest) == 1: 
            self.best = vbest.clone()
            self.elite[self.best.fx] = self.best

            
        #print [i.fx for i in self.individuals]  


    def selection(self, ind1, ind2):
        ofx1, ofx2 = self.optfoo(ind1.fx), self.optfoo(ind2.fx)
        return const.CompareType[self.optimisationtype](ofx1, ofx2)


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
        self.repetition()
        self.csort()
        #self.repetition(True)
        val = self.best.fx + ((self.max-self.best.fx)*self.rate_procent)
        cnt = find(val)

        #print [ind.fx for ind in self.population]
        
        
        if cnt < self.count*self.best_population_rate:
            cnt = int(self.count*self.best_population_rate)
        elif cnt >= self.populationsize:
            cnt = self.populationsize-1

        self.best_population_idx = cnt

        self.elite = [self.best.clone()]
        clones = {}
        for ind in self[:cnt]:
            if not clones.get(ind.fx, None):
                clones[ind.fx] = ind        

        self.elite += clones.values()


    def repetition(self, ast = False):
        unique = {}
        for ind in self.population:
            unique[ind.fx] = ind         

        new = [self.rand_ind() for _ in xrange(self.count - len(unique))]

        self.population = unique.values() + new

   
    def calc(self):
        self.extreme()
        self.rate()
        self.population = [self.best.clone()] + self.population[:self.populationsize-1]
        

    def csort(self):  
        self.population.sort(cmp = self.selection)

    def generation(self, size):
        for _ in xrange(self.count, size):
            ind = self.conceiving()
            ind.randomcreate()
            ind.fitness()
            self.population.append(ind)
        self.best_population_idx = self.count - 1  
        
    def rand_ind(self):
        ind = self.conceiving()
        ind.randomcreate(v_opt = False)
        ind.fitness()
        return ind      

    
    def parent(self):
<<<<<<< HEAD
        cnt = len(self.elite) - 1
        i = random.randint(0, cnt)
        return self.elite[i]
=======
        elite = self.elite.values()
        i = random.randint(0, len(elite)-1)
        return self[i]
>>>>>>> master
        
class Evolution (object):
    def __init__(self, size = 100, iteration = 20, generatemutation = 100,
                 populationratemutation = 100, mutationtype = const.muRandom,
                 bestprotected = True, crossingovertype = const.coRandom,
                 ClassIndividual = None, MutationsClasses = [], args = [],
                 child_count = 2, printlocalresult = True, ratestatic = False,
<<<<<<< HEAD
                 optimization_type = const.otMin, kfactor = float('inf'), tt_num = 1):
=======
                 optimization_type = const.otMin, kfactor = float('inf'), tt_num = 0):
>>>>>>> master

        self.populationsize = size
        self.iteration = iteration
        self.generatemutation = generatemutation
        self.populationratemutation = populationratemutation
        self.mutationtype = mutationtype
        self.bestprotected = bestprotected
        self.crossingovertype = crossingovertype
        self.printlocalresult = printlocalresult
        self.MutationCls = MutationsClasses
        self.ClsInd = ClassIndividual
        self.args = args
        self.population = None
        self.mutations = []
        self.child_count = child_count
        self.optimization_type = optimization_type 
        self.ratestatic = ratestatic
        self.kfactor = kfactor
        self.tt_num = tt_num
        self.init()

    def init(self):
        self.population = Population(self.populationsize, self.bestprotected, self.optimization_type, self.ClsInd, self.args)
        self.population.init()
        self.generation()
        self.mutations = mut.Mutations(self.ratestatic)

        for mCls in self.MutationCls:
            self.mutations.add(mCls())

        self.mutations.init()
        print self.mutations
        

        self.population.calc()

    def generation(self):
        self.population.generation(self.populationsize)

    def calc(self):
        i = 0
        for i in xrange(1, self.iteration):
            if not (i % self.kfactor):
                self.disaster()
            self.anthropogeny()
            if self.printlocalresult:
<<<<<<< HEAD
                print "experiment {3} population {0} count{1}  best {2}".format(i, self.population.count, self.population.best, self.tt_num)
                #top = [x.fx for x in self.population]
                #top.sort()
                #print top

=======
                print "ex {3} population {0} count {1}  best {2}".format(i, self.population.count, self.population.best, self.tt_num)
>>>>>>> master
                #print self.population.best
                        
            
    def anthropogeny(self):
        self.mutation()
        self.population.calc()
        
    

    def mutation(self):
        self.mutations.mutagenesis(self.population, self.mutationtype, self.populationratemutation, self.generatemutation)
        print self.mutations

    def printbest(self):
        print self.population.best

    def disaster(self):
        #pass
        self.population.population = [self.population.best.clone()]
        self.generation()
        

if __name__ == "__main__":

    print '*** min f(x) = x^2 ***'

    class X2 (Individual):
        def calcx(self):
            return reduce(lambda res, i: res + self[i].val*2**i, range(0, self.count),0)
            
        foofx = lambda self, x: x**2

        def randomcreate(self, best=None):
            for i in xrange(32):
                x = random.randint(0,1)
                g = self.addgen()
                g.val = x

            self.fitness()


    min_x2 = Evolution(size = 100, iteration = 25, generatemutation = 30,
                       populationratemutation = 80, ClassIndividual = X2,
                       MutationsClasses = [mut.Crossingover, mut.MRand], printlocalresult = True)
    min_x2.calc()

   
