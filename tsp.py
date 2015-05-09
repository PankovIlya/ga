import ga, vertexs, random

class Way (ga.Individual):

    def __init__(self, *args):
        ga.Individual.__init__(self, *args)
        self.back = 1.05
        self.vertexs = args[0]
                   
    def __str__(self):
##        for g in self.dna:
##            print g.id, g.val
        return ga.Individual.__str__(self)


    def printbest(self):
        for g in self.dna:
            print g.id, g.val

    def optmin(self, x):
        return 1.0/(x-2000)
        
            
    def renum(self):
        self.ordval()
        for i in xrange(self.count):
            self.itemv(i).val = i
            
    def calcx(self):
        self.renum()
        sumx = 0
        for i in xrange(self.count-1):
            sumx += self.vertexs.distance[self.itemv(i).id][self.itemv(i+1).id]
        sumx += self.vertexs.distance[self.itemv(self.count-1).id][self.itemv(0).id]
        return sumx
    
    foofx = lambda self, x: x

    def randomcreate(self):
        cnt = self.vertexs.count
        if cnt < 2:
            raise Exception('City count < 2!')
        for i in xrange(cnt):
            g = self.addgen()
            g.val = random.randint(i,cnt-1)
        self.renum()
       

class ExchangeCity2(ga.Mutation):
    def mutate(self, individual, cnt):
        def change(idx1, idx2):
            idc = individual.itemv(idx2)._id
            individual.itemv(idx2)._id = individual.itemv(idx1)._id
            individual.itemv(idx1)._id = idc
            
        fx = individual.fx
        for _ in xrange(cnt):
            idx1 = random.randint(0, individual.count-1)
            idx2 = random.randint(0, individual.count-1)
            change(idx1, idx2)

        if individual.fitness()*individual.back < fx:
            CrossFide().mutate(individual, cnt)

class RandomCity2(ga.Mutation):
    def mutate(self, individual, cnt):
        individual.renum()
        for _ in xrange(cnt):
            val = random.randint(0, individual.count-1)
            new_val = random.randint(0, individual.count-1)
            if val < new_val:
                k = 1
            else:
                k = -1
            for i in xrange(val+k, new_val, k):
                individual.itemv(i).val += -k
                    
            individual.itemv(val).val = new_val
        CrossFide().mutate(individual, cnt)

class CrossFide(ga.Mutation):
    def mutate(self, individual, cnt):
        def change(idx1, idx2):
            idc = individual.itemv(idx2)._id
            individual.itemv(idx2)._id = individual.itemv(idx1)._id
            individual.itemv(idx1)._id = idc
            
        start = random.randint(0, individual.count - cnt - 1)
        for i in xrange(0, individual.count - 3):
            for j in xrange(start+2, individual.count - 1):
                if individual.vertexs.intersection(individual.itemv(i).id, individual.itemv(i+1).id, individual.itemv(j).id, individual.itemv(j+1).id):
                    fx = individual.fx
                    change(i+1, j)
                    if individual.fitness() > fx:
                        change(i+1, j)
                        individual.fitness()

                    

class Gready(ga.Mutation):
    def mutate(self, individual, cnt):
       # print 'mutate'
        individual.renum()
##        for i in xrange(individual.count):
##            print individual.itemv(i).id, individual.itemv(i).val
        #for i in xrange(cnt):
        j = random.randint(0, individual.count-2)
        id1 = individual.itemv(j).id
        id2 = individual.itemv(j+1).id
        idm = individual.vertexs.near(id1)
##        print j, id1, id2, idm
##        print individual[id1].val, individual[id2].val, individual[idm].val 
##        print idm, individual.vertexs.distance[id1][idm], individual.vertexs.distance[id1]
##        print individual[id1].val, individual[id2].val, individual[idm].val
        val = individual[id2].val
        individual[id2].val = individual[idm].val
        individual[idm].val = val
        


class TSP( object ):
    def __init__(self, iteration, lenfoo):
        self.vertexs = vertexs.Vertexs(lenfoo)
        self.tspga = None
        self.iteration = iteration

    def calc(self):
        self.tspga = ga.Evolution(size = 1000, iteration = self.iteration, mutationtype = 'muRandom',
                                  generatemutation = 10, populationratemutation = 80,
                                  #lassIndividual = Way,MutationsClass = [RandomCity, Gready, ExchangeCity, RandomCity2, ExchangeCity2],
                                  ClassIndividual = Way,MutationsClass = [RandomCity2, ExchangeCity2],
                                  args = [self.vertexs])
        self.tspga.init()
        #print self.tspga.populations[0][0]
        #self.tspga.populations[0][0][0].val
        #self.tspga.populations[0][0].ordid()
        #p]rint self.tspga.populations[0][0]
        self.tspga.calc()
        for g in self.tspga.populations[1][0].dna:
            print g.id, g.val
        #self.tspga.populations[0][0].ordid()
        #print self.tspga.populations[0][0]
        
    def load(self, filename):
        f = open(filename)
        data = json.load(f)
        cities = data["cities"]
        for c in cities:
            v = self.vertexs.add()
            v.lon, v.lat = c[1], c[0]
        f.close()
        self.vertexs.calcmatrix()

if __name__ == "__main__":
    import json, math
    foostraightlen = lambda v1, v2: int(math.pow(math.pow((v1.lon - v2.lon),2) +
                                                  math.pow((v1.lat - v2.lat),2), 0.5))
    tsp = TSP(2000, foostraightlen)
    tsp.load('testt.json')
    #print tsp.vertexs.vertexlist
    #print tsp.vertexs.distance[1][9]

    tsp.calc()


    
        
        








        
