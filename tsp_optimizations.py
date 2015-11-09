import mutations as mut
import vertexs
import random as rand


class CrossingoverTSP (mut.Crossingover):
    def __init__(self):
            super(self.__class__, self).__init__()
            self.rate = 0.25
    def after_mutate(self, child, res, population):
        CrossFide().mutate(child, 0, population)     

class ExchangeCity(mut.Mutation):
    def __init__(self):
            super(self.__class__, self).__init__()
            self.name = 'ExchangeCity'
            self.rate = 0.5
            
    def mutate(self, individual, cnt, population):
        ind = individual.clone()


        def change(idx1, idx2):
            ind[idx2]._id, ind[idx1]._id = ind[idx1]._id, ind[idx2]._id
            
                
        fx = individual.fitness()
        
        idx1 = rand.randint(0, ind.count-1)
        idx2 = idx1
        while idx1 == idx2:
            idx2 = rand.randint(0, ind.count-1)
        change(idx1, idx2)

        if ind.fitness() < fx*individual.back:
            CrossFide().mutate(ind, -1, population)

        #if ind.fx < fx:
        #    population.add(ind)

        return ind



class MoveCity(mut.Mutation):
    def __init__(self):
            super(self.__class__, self).__init__()
            self.name = 'MoveCity'
            self.rate = 0.75
   
    def mutate(self, individual, cnt, population):
        ind = individual.clone()
                
        fx = individual.fitness()

        idx1 = rand.randint(0, ind.count-1)
        idx2 = idx1
        while idx1 == idx2:
            idx2 = rand.randint(0, ind.count-1)

        idx1, idx2 = min(idx1, idx2), max(idx1, idx2)
        id1 = ind[idx1]

        ind.dna = ind.dna[:idx1] + ind.dna[idx1+1:idx2+1] + [id1] + ind.dna[idx2+1:] 

        ind.renum2()

        if ind.fitness() < fx*individual.back:
            CrossFide().mutate(ind, -1, population)

        #if ind.fx < fx:
        #    population.add(ind)

        return ind


class CrossFide(mut.Mutation):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.name = 'CrossFide'
        self.rate = 1.0

    def mutate(self, individual, cnt, population):
        def change(idx1, idx2):
            individual[idx2]._id, individual[idx1]._id = individual[idx1]._id, individual[idx2]._id
            
        #start = random.randint(0, individual.count - cnt - 1)
        res, i = True, 0
        individual.fitness()
        
        while i < individual.count - 2:
            j = i + 2
            while j < individual.count:
                if individual.vertexs.intersection(individual[i].id,
                                                   individual[i+1].id,
                                                   individual[j].id,
                                                   individual[(j+1) % individual.count].id):
                    fx = individual.fitness()
                    change(i+1, j)
                    if individual.fitness() > fx:
                        change(i+1, j)
#                        individual._fx = fx
                    
                        old = individual.wslice(None,None)
                        base = individual.wslice(None,None)
                        lst = base[i+1 : j+1]
                        individual.dna = base[:i+1] + lst[::-1] + base[j+1:]
                        individual.renum2()
                        individual.fitness()
                        if individual.fitness() > fx:
                            #print 'aaa', individual.fx
                            individual.dna = old
                            individual.fitness()
                            #print 'hey', individual.fitness()
                j += 1
            i +=1

        return individual.fitness()
        #1/0
                    

class Gready(mut.Mutation):
    def __init__(self):
            super(self.__class__, self).__init__()
            self.name = 'Gready'
            self.rate = 1
            
    def mutate(self, ind, cnt, population):
        individual = ind.clone()
        fx = ind.fitness()

        cities = {}
        
        def changeid(idx1, idx2):
            individual[idx2]._id, individual[idx1]._id = individual[idx1]._id, individual[idx2]._id

      
        def changeval(idx1, idx2):
            cities[idx1][0], cities[idx2][0] = cities[idx2][0], cities[idx1][0]

 
        if cnt == -1:
            idx1, idx2 = 0, individual.count -1
        else:   
            idx1 = rand.randint(0, individual.count-2)
            idx2 = rand.randint(idx1+2, min(idx1+9, individual.count))
      
        reserve = {}
        for city in individual.dna[:idx1]:
            reserve[city.id] = city.val


        target = {}
        for city in individual.dna[idx1+1:idx2]:
            target[city.id] = city.val

 

        i = individual.count*2
        for city in individual.dna[idx2:]:
            reserve[city.id] = i
            i += 1

        
        local_min = {}    
        city_id, num  = individual.dna[idx1].id, idx1 
        local_min[city_id] = num

  
        while target:
            num += 1
            near_city_id = individual.vertexs.near(city_id, local_min)
            
            if near_city_id >= 0:
                city_id = near_city_id
                if target.get(city_id, -1) >= 0:
                    del target[city_id]
                elif reserve.get(city_id, -1) >= 0:
                    del reserve[city_id]
                local_min[city_id] = num
            else:
                 raise Exception('bug') 
      
        i = 0
        for city in reserve:
            individual.dna[i]._id = city
            individual.dna[i].val = reserve[city]
            i += 1            

        for city in local_min:
            individual.dna[i]._id = city
            individual.dna[i].val = local_min[city]
            i += 1

        #print "result",  individual.fitness(), fx

        if individual.fitness() < fx*ind.back:
           CrossFide().mutate(individual, cnt, population)

        return individual

        
