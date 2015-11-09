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
    def __init__(self, ratestatic, childcount = 2):
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

            fxo = population[idx].fx

            ind = mutation.mutate(population[idx], cnt, population)

            if  ind and const.CompareType[population.optimisationtype](ind.fitness(), fxo) == 1:
                population[idx] = ind 
                mutation.advance += 1
                self.all_advance += 1

        if not self.ratestatic:
            self.calc_info()

class Crossingover (Mutation):
    def __init__(self):
            Mutation.__init__(self)
            self.name = 'Crossingover'
            self.childcount = 1
            self.population = None

    def after_mutate(self, child, res, population):
        pass

    def mutate(self, individual, cnt, parents):
        fx = individual.fx
        self.population = parents

        #vparent1 = parents.parent()
        #vparent2 = parents.best
        vparent1 = individual
        
        i = 0
        vparent2 = vparent1
        while vparent2.fx == vparent1.fx and i < 100:
            vparent2 = parents.parent()
            i += 1

        if i == 100:
            return fx
            print '!!!!!!!!!!!!!!!!!!!!! warning !!! no parent for Crossingover ', parents.best_population_idx
    
        children = self.fertilisation(vparent1, vparent2)

        for child in children:
            self.after_mutate(child, cnt, parents)
            if parents.selection(vparent1, child) == 1 and parents.selection(vparent2, child) != 0:
                #parents.add(child)
                return child
                #fx = child.fx
                
                

        return None

         
 
    def fertilisation(self, parent1, parent2):

        children = []
        
        for _ in xrange(self.childcount):
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

class MRand (Mutation):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = 'Random'
    
    def mutate(self, ind, cnt, population):
        individual = ind.clone()
        for i in xrange(cnt):
            idx = random.randint(0, individual.count-1)
            individual[idx].val = random.randint(0,1)

        return individual

