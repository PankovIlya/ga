import random, operator

TCrossingOverType = set (['coBest', 'coRandom'])
TMeiosisType = set (['mtRandom', 'mtEqual'])
TMutationType = set (['muRandom', 'muEqual'])
sSortType = set (['dsID', 'dsVal'])
OptimisationType = set (['otMin', 'otMax'])

class Gene (object):
    def __init__(self):
      self._ID = 0 
      self.Val = 0
      
    ID = property(lambda self: self._ID)

class Individual (object):
    def __init__(self, *args):
        self._SortType = 'dsID'
        self.DNA = []
        self._X = 0
        self._Fx = 0
        
    def __getitem__(self, idx):
        self.OrdID 
        return self.DNA[idx]


    def item(self, idx):
        return self.DNA[idx]

    def __setitem__(self, idx, val):
         self.DNA[idx] = val 
    
    def __str__(self):
        return 'X ' + str(self.X) + ' Fx ' + str(self.Fx)
   

    X = property (lambda self: self._X) 

    FooFx = lambda self, x : 'This is Abstract Method'

    GetFx = lambda self: self._Fx

    def SetFx(self, x):
        self._Fx = self.FooFx(x)
    
    Fx = property(GetFx, SetFx)

    Count = property(lambda self: len(self.DNA))

    def CheckSortType(foo):
        def check(self, val):
            if not(val in sSortType):
                raise Exception('Unknown Sort Type', sSortType)
            return foo(self, val)
        return check
        
    @CheckSortType
    def setst(self, val):
      self._SortType = val

    def getst(self):
      return self._SortType

    SortType = property (getst, setst)
  
    cmpid = staticmethod(lambda g1, g2: cmp(g1.ID, g2.ID)) #or cmp(g1.Cour, g2.Cour)
    cmpval = staticmethod(lambda g1, g2: cmp(g1.Val, g2.Val)) #or cmp(g1.Cour, g2.Cour) 
 
    def OrdID(self):
        if SortType != 'dsID': 
            self.DNA.sort(cmp=cmpid)
            SortType = 'dsID'

    def OrdVal(self):
        SortType = 'dsVal'
        self.DNA.sort(cmp=cmpval)

    def AddGen(self):
        g = self.Add()
        self.DNA.append(g)
        g._ID = len(self.DNA)-1
        return g

    def Add(self):
        return Gene()

    def Value(self):
        self._X = self.CalcX()
        self.Fx = self.X
        return self.X
        
    def CalcX(self):
        raise Exception('Absract method, return X')

    def RandomCreate(self):
         raise Exception('Absract method, fill DNA')

    def Copy(self, Best):
        for g in xrange(self.Count):
            self[g].Val = Best[g].Val
        self.Value()
        
            
class Population (object):
    def __init__(self, aSize, bestprotected = True, OptimisationType = 'otMin', ClsInd = None, args = []):
        self.Size = aSize
        self.BestProtected = bestprotected
        self.Args = args
        self.ClsInd = ClsInd
        self.IndList = []
        self.SuccessList = []
        self.Min =  214748364
        self.Max = -214748364
        self.Best = None
        self.SumX = 0
        self.SumFx = 0
        self.SumOptFx = 0.0
        if OptimisationType == 'otMin':
            self.OptFoo = self.OptMin
        else:
            self.OptFoo = self.OptMax

    def decround(fn):
        def decc(self,x):
            return self.cround(fn(self, x))
        return decc

    #@decround
    def OptMin(self, x):
        return 1.0/x if x != 0 else 1.0

    #@decround
    def OptMax(self, x):
        return x 

    def Init(self):
        self.Best = self.Add()
        self.Best.RandomCreate()
        self.Best.Value()
            
    def __getitem__(self, idx):
        return self.IndList[idx]

    def AddInd(self):
        ind = self.Add()
        self.IndList.append(ind)
        return ind
         
    def Add(self):
        return self.ClsInd(*self.Args)

    Count = property(lambda self: len(self.IndList))

    def PrintTest(self):
        print self.Best
        ##        print self.SumX, self.SumFx, self.SumOptFx, self.Best, self.Min, self.Max, self.SumX - self.Min, self.SumX - self.Max,
        print int(round(self.FooSuccessRate(self.OptFoo(self.Best.Fx))*self.Count)) + 1
                 
    #min, max, sum - x, Fx
    def Extreme(self):
        self.Min =  214748364
        self.Max = -214748364
        self.SumX, self.SumFx, self.SumOptFx = 0, 0, 0.0
        #print self.Best
        vBest = self.Best #init best!!!
        for ind in self.IndList:
            if ind.Value() < self.Min:
                self.Min = ind.X    
            if ind.X > self.Max:
                self.Max = ind.X
            if self.Cmp(ind, vBest) == 1: 
                vBest = ind
            self.SumX += ind.X
            self.SumFx += ind.Fx
            #print self.OptFoo(ind.Fx)
            self.SumOptFx += self.OptFoo(ind.Fx)
        #print 'vBest', vBest    
        if self.Cmp(vBest, self.Best) == 1:
            self.Best.Copy(vBest)
        self.PrintTest()
        #print [Ind.X for Ind in self.IndList]

    def Cmp(self, ind1, ind2):
        ofx1, ofx2 = self.OptFoo(ind1.Fx), self.OptFoo(ind2.Fx)
        return cmp(ofx1, ofx2)

    #@decround
    def FooSuccessRate(self, rate):
        if self.SumOptFx == 0:
            return float(1/self.Count)
        else:
            return float(rate/self.SumOptFx)
            

    cround = staticmethod(lambda x: round(x,5))

    def Rate(self):
        self.SuccessList = []
        for ind in self.IndList:
            cnt = int(round(self.FooSuccessRate(self.OptFoo(ind.Fx))*self.Count)) + 1
            self.SuccessList += [ind for i in xrange(cnt)]

##        print 'SuccessList ', len(self.SuccessList)
##        print [Ind.X for Ind in self.SuccessList]
        random.shuffle(self.SuccessList) #!!!

    def Calc(self):
        self.Extreme()
        self.Rate()

    def Sort(self):
        self.IndList.sort(cmp = self.Cmp)

    def Generation(self):
        for i in xrange(self.Size):
            self.AddInd().RandomCreate()

    def Parent(self):
        i = random.randint(0, len(self.SuccessList)-1)
        return self.SuccessList[i]
        

class Mutation (object):
    def Mutate(self, individual, rate):
        raise Exception('Abstract method')


class Mutations (object):
    def __init__(self, populationratemutation, generatemutation, mutationtype):
        self.MutationsList = []
        self.PopRateMutation = populationratemutation
        self.GeneRateMutation = generatemutation
        self.MutationType = mutationtype

    def __getitem__(self, idx):
        return self.MutationsList[idx]
        
    def Add(self, mutation):
        self.MutationsList.append(mutation)

    Count = property(lambda self: len(self.MutationsList))

    def Mutagenesis(self, population):
        CntPopMut = (population.Count * self.PopRateMutation) // 100;
        if self.MutationType == 'muRandom':
            CntPopMut = random.randint(0, CntPopMut-1)

        p = (lambda b: 1 if b else 0)(population.BestProtected)
          
        i = 0
        while i < CntPopMut:
            #select mutation
            idxM =  random.randint(0, self.Count-1)
            #select individ
            idxI = random.randint(0, population.Count - 1 - p) + p 

            if self.MutationType == 'muRandom':
                prm = random.randint(0,self.GeneRateMutation)
            else:
                prm = self.GeneRateMutation

            self[idxM].Mutate(population[idxI], prm)
            i += 1
    
        

class Evolution (object):
    def __init__(self, size = 100, iteration = 25, genratemut = 100,
                 popratemut = 100, mutationtype = 'muRandom',
                 bestprotected = True, CrossingOverType = 'coRandom',
                 ClsInd = None, MutationCls = [], args = []):
        self.PopulationSize = size
        self.Iteration = iteration
        self.GenRateMut = genratemut
        self.PopRateMut = popratemut
        self.MutationType = mutationtype
        self.BestProtected = bestprotected
        self.MutationCls = MutationCls
        self.CrossingOverType = CrossingOverType
        self.ClsInd = ClsInd
        self.Args = args
        self.Populations = []
        self.Mutations = []
        self.Init()
        
        

    def __getitem__(self, idx):
        return self.Populations[idx]

    def Init(self):
        for p in xrange(2):
            population = Population(self.PopulationSize, self.BestProtected, 'otMin', self.ClsInd, self.Args)
            population.Init()
            population.Generation()
            self.Populations.append(population)

        self.Mutations = Mutations(self.PopRateMut, self.GenRateMut, self.MutationType)

        for MCls in self.MutationCls:
            self.Mutations.Add(MCls())

    def Calc(self):
        i = 0
        while i < self.Iteration:
            print 'iteration', i
            self.Anthropogeny(self[0], self[1])
            self.Anthropogeny(self[1], self[0])
            i += 1
            
            
    def Anthropogeny(self, Parents, Children):
        Parents.Calc();
        self.CrossingOver(Parents, Children)
        self.Mutation(Children)

    def CrossingOver(self, Parents, Children):
        if self.BestProtected:
            Children[0].Copy(Parents.Best)
            Children.Best.Copy(Parents.Best)
            k = 1
        else:
            k = 0

        i = k    
        while i < (Parents.Count//2):
            if self.CrossingOverType == 'coRandom':
                vParent1 = Parents.Parent()
            else:
                vParent1 = Parents[0] # Ïîñìîòðåòü, êàê ïîéäåò

            vParent2 = Parents.Parent()

            if vParent1 != vParent2:
                self.Meiosis(vParent1, vParent2, Children[i*2-k], Children[i*2+1-k])
            else:
                Children[i*2-k].Copy(vParent1)
                Children[i*2+1-k].Copy(vParent2)
            i += 1

    def Meiosis(self, Parent1, Parent2, Child1, Child2):
        def Chromosome(Num, Length, cParent1, cParent2):
            k = Num;
            while k < Length:
                self.SetGene(Child1[k], cParent1[k])
                self.SetGene(Child2[k], cParent2[k])
                k += 1

        LenChr = random.randint(0,Child1.Count)
        Chromosome(0, LenChr, Parent1, Parent2)
        Chromosome(LenChr, Child1.Count, Parent2, Parent1)

    def SetGene(self, Gene1, Gene2):
        Gene1._ID = Gene2._ID
        Gene1.Val = Gene2.Val

    def Mutation(self, Population):
        self.Mutations.Mutagenesis(Population)

if __name__ == "__main__":

    class X2 (Individual):
        def CalcX(self):
           return reduce(lambda res, i: res + self[i].Val*2**i, range(self.Count),0)

        FooFx = lambda self, x: x**2

        def RandomCreate(self):
            for i in xrange(32):
                x = random.randint(0,1)
                g = self.AddGen()
                g.Val = x

    class MRand (Mutation):
        def Mutate(self, individual, rate):
            for i in xrange(individual.Count*rate//100):
                idx = random.randint(0, individual.Count-1)
                individual[idx].Val = random.randint(0,1)

    E = Evolution(iteration = 50, ClsInd = X2, MutationCls = [MRand])
    E.Init()
    #E.Calc()

    class DiffArr (Individual):
        def __init__(self, *args):
            Individual.__init__(self)
            self.Arr = args[0]


        def PrintArr(self, short):
            a, b = [], []
            for i in xrange(self.Count):
                if self[i].Val == 0:
                    a.append(self.Arr[self[i].ID])
                else:
                    b.append(self.Arr[self[i].ID])
            if short:
                print 'Arr1', len(a)
                print 'Arr2', len(b)
            else:                
                a.sort()
                b.sort()
                print 'Sum Arr1', sum(a)
                print 'Sum Arr2', sum(b) 
                print 'Delta Arr', sum(a) - sum(b)
                print 'Arr1', a[:10]
                print 'Arr2', b[:10]
                    

        def __str__(self):
            self.PrintArr(True)
            return Individual.__str__(self)
            
                
        def CalcX(self):
            sumx = 0
            for i in xrange(self.Count):
                if self[i].Val == 0:
                    sumx += self.Arr[self[i].ID]
                else:
                    sumx -= self.Arr[self[i].ID]
            return sumx
            

        FooFx = lambda self, x: x**2

        def RandomCreate(self):
            for i in xrange(len(self.Arr)):
                g = self.AddGen()
                g.Val = 1 #random.randint(0,1)

    class MRandChange (Mutation):
        def Mutate(self, individual, rate):
            cnt = individual.Count*rate//100
            for i in xrange(cnt):
                idx1 = random.randint(0, individual.Count-1)
                idx2 = random.randint(0, individual.Count-1)
                x = individual[idx1].Val
                individual[idx1].Val = individual[idx2].Val
                individual[idx2].Val = x


            
    #arr = [x for x in xrange(1,101)] +  [x for x in xrange(10000,10100)] + [x for x in xrange(100000,100100)]
    arr = [random.randint(0, 50000) for x in xrange(0,10000)]
    #arr += [sum(arr)]
    #  mutationtype = 'muRandom', , MRandChange, 
    E = Evolution(size = 100, iteration = 30, mutationtype = 'muStatic',
                  genratemut = 15, popratemut = 60, ClsInd = DiffArr,
                  MutationCls = [MRand], args = [arr])
    E.Init()
    E.Calc()
    E.Populations[1].Best.PrintArr(False) 
    
    
    
