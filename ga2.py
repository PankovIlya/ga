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
cmin = lambda x1, x2: cmp(x2, x1)
cmax = lambda x1, x2: cmp(x1, x2)
OptimisationType = {otMin:optmin, otMax:optmax}
CompareType = {otMin:cmin, otMax:cmax}


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
    def __init__(self, populationsize = 100, bestprotected = True, opt_type = otMin,
                 ClsInd = None, args = [], calc_fitness = True,
                 rate_procent = 0.25, best_population_rate = 0.15):
        self.populationsize = populationsize 
        self.bestprotected = bestprotected
        self.args = args
        self.optimisationtype = opt_type
        self.ClsInd = ClsInd
        self.calc_fitness = calc_fitness
        self.success_list = []
        self.individuals = []
        self.min = float('inf')
        self.max = -float('inf')
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

    def __setitem__(self, idx, val):
        self.individuals[idx] = val

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
            if self.selection(vbest, ind) == 1: 
                vbest = ind
            self.sumx += ind.x
            self.sumfx += ind.fx
                
            self.sumoptfx += self.optfoo(ind.fx)

        if self.selection(self.best, vbest) == 1: 
            self.best = vbest.clone()

        #print [i.fx for i in self.individuals]  


    def selection(self, ind1, ind2):
        ofx1, ofx2 = self.optfoo(ind1.fx), self.optfoo(ind2.fx)
        return CompareType[self.optimisationtype](ofx1, ofx2)


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
        elif cnt >= self.populationsize:
            cnt = self.populationsize-1
            
        self.best_population_idx = cnt


    def calc(self):
        self.extreme()
        self.rate()
        self.individuals = self.individuals[:self.populationsize]

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
    def __init__(self):
        self.rate = 0.0
        self.weight = 0
        self.name = ""
        self.advance = 0
        self.total = 0

    def mutate(self, individual, cnt, population):
        raise Exception('Abstract method')


class Mutations (object):
    def __init__(self, childcount = 2):
        self.mutations = []
        self.all_total = 0
        self.all_advance = 0
        self.srate = 0
        self.childcount = childcount
        self.min_rate = 0.4

    def get_by_name(self, name):
        for mut in self.mutations:
            if mut.name == name:
                return mut
        return None

    def __getitem__(self, idx):
        return self.mutations[idx]
        
    def add(self, mutation):
        self.mutations.append(mutation)
        

    def __str__(self):
        for mut in self.mutations:
            print mut.name, mut.weight, mut.rate, mut.advance, mut.total
        return 'all_advance ' + str(self.all_advance) + ' all_total ' + str(self.all_total)

    def calc_info(self):

        all_w = 0
        for mut in self.mutations:
            if mut.total == 0:
                mut.weight = 100.0
            else:
                mut.weight = mut.advance*100.0/mut.total
            all_w += mut.weight

        if all_w == 0:
            return
            
        k = 1.0
        for mut in self.mutations:
            mut.rate = mut.weight*k*1.0/all_w
            if mut.rate < self.min_rate:
                mut.rate = self.min_rate
                k -= mut.rate
                all_w -= mut.weight

        self.srate = 0
        for mut in self.mutations:
            self.srate += mut.rate
            mut.rate = self.srate
                
       
        
    def init(self):
        def check():
            for mut in self.mutations:
                if mut.rate == 0:
                    return False
            return True

        if not check():
            val = 1.0/self.count
            for idx in xrange(1, self.count):
                self[idx-1].rate = idx*val
                

            self[-1].rate = 1
                
    count = property(lambda self: len(self.mutations))

    def get_mutation(self):
        val_m = random.random()*self.srate
        #print [mut.rate for mut in self.mutations]
        for mut in self.mutations:
            if val_m < mut.rate:
                return mut
        

    def mutagenesis(self, population, mutationtype, populationratemutation, generatemutation):
        
        if self.count == 0:
            return
                       
        for idx in xrange(population.count):
            #select mutation
            mutation = self.get_mutation()
            
            if isinstance(mutation, Crossingover):
                cnt = self.childcount
            else:
                cnt = int(((population[idx].count-1)*generatemutation)//100) + 1

                if mutationtype == muRandom:
                    cnt = random.randint(1, cnt)
                
            mutation.total += 1
            self.all_total += 1

            fx = population[idx].fx

            res = mutation.mutate(population[idx], cnt, population)

            if  CompareType[population.optimisationtype](population[idx].fx, fx) == 1: 
                mutation.advance += 1
                self.all_advance += 1
            elif res:
                mutation.advance += res
                self.all_advance += res
                mutation.total += res - 1
                self.all_total += res - 1

        self.calc_info()

class Crossingover (Mutation):
    def __init__(self):
            Mutation.__init__(self)
            self.name = 'Crossingover'
            self.childcount = 0
            self.population = None

    def after_mutate(self, children, res, population):
        pass

    def mutate(self, individual, cnt, parents):
        res = 0
        self.child_count = cnt
        self.population = parents

        vparent1 = parents.parent()

        i = 0
        vparent2 = vparent1
        while vparent2 == vparent1 and i < 100:
            vparent2 = parents.parent()
            i += 1

        if i == 100:
            return res
            print '!!!!!!!!!!!!!!!!!!!!! warning !!! no parent for Crossingover ', parents.best_population_idx
    
        children = self.fertilisation(vparent1, vparent2)

        for child in children:
            parents.add(child)
            #print child.fx, vparent1.fx,  vparent2.fx
            #print parents.selection(vparent1, child), parents.selection(vparent2, child)
            if parents.selection(vparent1, child) == 1 \
                or  parents.selection(vparent2, child) == 1:
                res += 1

        self.after_mutate(children, res, parents)

        return res

         
 
    def fertilisation(self, parent1, parent2):

        children = []
        
        for _ in xrange(self.child_count):
            children.append(self.meiosis(self.population.conceiving(), parent1, parent2))
            children.append(self.meiosis(self.population.conceiving(), parent2, parent1))

        self.population.rang(children)
        #print [child.fx for child in children]

        return children[:2]

    def meiosis(self, child, parent1, parent2):

        len_chr = random.randint(0, parent1.count)

        child.dna = parent1[:len_chr] + parent2[len_chr:]
        child.fitness()

        return child

        

class Evolution (object):
    def __init__(self, size = 100, iteration = 20, generatemutation = 100,
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
        self.child_count = 1
        

    def init(self):
        self.population = Population(self.populationsize, self.bestprotected, otMin, self.ClsInd, self.args)
        self.population.init()
        self.generation()
        self.mutations = Mutations()

        for mCls in self.MutationCls:
            self.mutations.add(mCls())

        self.mutations.init()
        #print self.mutations
        

        self.population.calc()

    def generation(self):
        self.population.generation(self.populationsize)

    def calc(self):
        i = 0
        for i in xrange(self.iteration):
            self.anthropogeny()
            if self.printlocalresult:
                print "population {0}  best {1}".format(i, self.population.best)
                #print self.population.best
                        
            
    def anthropogeny(self):
        self.mutation()
        self.population.calc()
    

    def mutation(self):
        self.mutations.mutagenesis(self.population, self.mutationtype, self.populationratemutation, self.generatemutation)
        print self.mutations

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

            self.fitness()

    class MRand (Mutation):
        def __init__(self):
            Mutation.__init__(self)
            self.name = 'Random'
        
        def mutate(self, individual, cnt, population):
            for i in xrange(cnt):
                idx = random.randint(0, individual.count-1)
                individual[idx].val = random.randint(0,1)

            individual.fitness()



    min_x2 = Evolution(size = 100, iteration = 25, mutationtype = muRandom,
                      generatemutation = 30, populationratemutation = 80,
                      ClassIndividual = X2,
                      MutationsClass = [Crossingover, MRand], printlocalresult = True)
    min_x2.init()
    min_x2.calc()

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

    class Sstting (Individual):
        def __init__(self, *args):
            Individual.__init__(self, *args)
            self.sword = args[0]
                               

        def __str__(self):
            return self.printresult(True)
            return Individual.__str__(self)
            
                
        def calcx(self):
            word = ''
            for  s in self.dna:
                word += s.val

            return levenshtein_distance(self.sword, word)
            
        foofx = lambda self, x: 5**x

        def randomcreate(self):
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


    class MChange (Mutation):
        def __init__(self):
            Mutation.__init__(self)
            self.name = 'Change'
            
        def mutate(self, individual, cnt, population):
            n = len(alphabet)
            for i in xrange(cnt):
                idx = random.randint(0, individual.count-1)
                j = random.randint(0,n-1)
                individual[idx].val = alphabet[j]

    class MDelIns (Mutation):
        def __init__(self):
            Mutation.__init__(self)
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

    class MDel (Mutation):
        def __init__(self):
            Mutation.__init__(self)
            self.name = 'MDel'
            
        def mutate(self, individual, cnt, population):
            n = len(alphabet)
            idx = random.randint(0, individual.count-1)
            del individual.dna[idx]

    class MIns (Mutation):
        def __init__(self):
            Mutation.__init__(self)
            self.name = 'MIns'
            
        def mutate(self, individual, cnt, population):
            n = len(alphabet)
            g = individual.addgen()
            j = random.randint(0,n-1)
            g.val = alphabet[j]
            individual.dna.append(g)


    s = 'Marchelo teaches Savelys evolution biology. Happy Birthday!!!'
    ss = Evolution(size = 1000, iteration = 90, mutationtype = muRandom,
                   generatemutation = 25, populationratemutation = 80, ClassIndividual = Sstting,
                   MutationsClass = [Crossingover, MChange, MDelIns, MDel, MIns], args = [s])

    ss.init()
    ss.calc()
    print "It's more thins setting"
    ss.populationsize = 5000
    ss.generatemutation = 12
    ss.iteration = 40
    ss.generation()
    ss.calc()

    print 1/0
   
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
    partitionproblem = Evolution(size = 150, iteration = 20, mutationtype = muRandom,
                  generatemutation = 30, populationratemutation = 80, ClassIndividual = DiffArr,
                  MutationsClass = [Crossingover, MRand], args = [arr])

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
    
    
    
    
    
