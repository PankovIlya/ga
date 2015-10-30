import random
import const

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
    def __init__(self, ratestatic, childcount = 4):
        self.mutations = []
        self.all_total = 0
        self.all_advance = 0
        self.srate = 0
        self.childcount = childcount
        self.min_rate = 0.2
        self.ratestatic = ratestatic


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
        self.srate = 1
        self.mutations.sort(key = lambda mut: mut.rate)
                
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

                if mutationtype == const.muRandom:
                    cnt = random.randint(1, cnt)
                
            mutation.total += 1
            self.all_total += 1

            fx = population[idx].fx

            res = mutation.mutate(population[idx], cnt, population)

            if  const.CompareType[population.optimisationtype](population[idx].fx, fx) == 1: 
                mutation.advance += 1
                self.all_advance += 1
            elif res:
                mutation.advance += res
                self.all_advance += res
                mutation.total += res - 1
                self.all_total += res - 1

        if not self.ratestatic:
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

        #vparent1 = parents.parent()
        #vparent1 = parents.best
        vparent1 = individual
        
        i = 0
        fx1, fx2 = vparent1.fx, vparent1.fx      
        while fx1 == fx2 and i < 70:
            vparent2 = parents.parent()
            fx2 = vparent2.fx
            i += 1

        if i == 70:
            return res
            print '!!!!!!!!!!!!!!!!!!!!! warning !!! no parent for Crossingover ', parents.best_population_idx
    
        children = self.amphimixis(vparent1, vparent2)

        for child in children:
            #print child.fx, vparent1.fx,  vparent2.fx
            #print parents.selection(vparent1, child), parents.selection(vparent2, child)
            if parents.selection(vparent1, child) == 1 \
                and parents.selection(vparent2, child) != 0:
                res += 1
                parents.add(child)

        self.after_mutate(children, res, parents)

        return res

         
 
    def amphimixis(self, parent1, parent2):

        children = []
        
        for _ in xrange(self.child_count):
            len_chr = random.randint(1, parent1.count)
            children.append(self.meiosis(self.population.conceiving(), len_chr, parent1, parent2))
            children.append(self.meiosis(self.population.conceiving(), len_chr, parent2, parent1))

        #print [child.fx for child in children]
        clones = {}
        for child in children:
            if not clones.get(child.fx, None):
                clones[child.fx] = child

        children = clones.values()
        self.population.rang(children)
        
        return children

    def meiosis(self, child, len_chr, parent1, parent2):
        child.dna = parent1[:len_chr] + parent2[len_chr:]
        child.fitness()

        return child

class MRand (Mutation):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = 'Random'
    
    def mutate(self, individual, cnt, population):
        for i in xrange(cnt):
            idx = random.randint(0, individual.count-1)
            individual[idx].val = random.randint(0,1)

        individual.fitness()

