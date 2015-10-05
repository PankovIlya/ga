import ga2 as ga, vertexs, random

from PIL import Image
from PIL import ImageDraw

class Way (ga.Individual):

    def __init__(self, *args):
        ga.Individual.__init__(self, *args)
        self.back = 1.05
        self.vertexs = args[0]
                   
    def __str__(self):
##        for g in self.dna:
##            print g.id, g.val
        return ga.Individual.__str__(self)

    def wslice(self, n, m):
        dna = []
        for itm in self.dna[n:m]:
            gene = ga.Gene()
            gene._id, gene.val = itm.id, itm.val
            dna += [gene]
        return dna


    def printbest(self):
        for g in self.dna:
            print g.id, g.val

            
    def renum(self):
        self.ordval()
        for i in xrange(self.count):
            self[i].val = i

    def renum2(self):
        for i in xrange(self.count):
            self[i].val = i
            
    def calcx(self):
        self.renum()
        sumx = 0
        for i in xrange(self.count-1):
            sumx += self.vertexs.distance[self[i].id][self[i+1].id]
        sumx += self.vertexs.distance[self[-1].id][self[0].id]
        return sumx
    
    foofx = lambda self, x: x

    def randomcreate(self, best=None):
        best = None
        if best:
            self.dna = best.clone().dna
        else:
            cnt = self.vertexs.count
            if cnt < 2:
                raise Exception('City count < 2!')
            for i in xrange(cnt):
                g = self.addgen()

            random.shuffle(self.dna)

            for i in xrange(cnt):
                self[i].val = i 

        self.fitness()
        Gready().mutate(self, -1, None)
        #CrossFide().mutate(self, -1, None)
                

class ExchangeCity(ga.Mutation):
    def __init__(self):
            ga.Mutation.__init__(self)
            self.name = 'ExchangeCity'
            self.rate = 1
            
    def mutate(self, individual, cnt, population):
        def change(idx1, idx2):
            individual[idx2]._id, individual[idx1]._id = individual[idx1]._id, individual[idx2]._id
            
        fx = individual.fx
        for _ in xrange(cnt):
            idx1 = random.randint(0, individual.count-1)
            idx2 = random.randint(0, individual.count-1)
            change(idx1, idx2)

        if individual.fitness() < fx*individual.back:
            CrossFide().mutate(individual, cnt, population)


class MoveCity(ga.Mutation):
    def __init__(self):
            ga.Mutation.__init__(self)
            self.name = 'MoveCity'
            self.rate = 0.4
   
    def mutate(self, individual, cnt, population):
        fx = individual.fx
        for _ in xrange(cnt):
            idx1 = random.randint(0, individual.count-1)
            idx2 = random.randint(0, individual.count-1)

            if idx1 <= idx2:
                k = -1
            else:
                k = 1

            id2 = individual[idx2]._id

            for i in xrange(idx2, idx1, k):
                individual[i]._id = individual[i+k]._id
                    
            individual[idx1]._id = id2

        if individual.fitness() < fx*individual.back:
            CrossFide().mutate(individual, cnt, population)


class CrossFide(ga.Mutation):
    def mutate(self, individual, cnt, population):
        def change(idx1, idx2):
            individual[idx2]._id, individual[idx1]._id = individual[idx1]._id, individual[idx2]._id
            
        #start = random.randint(0, individual.count - cnt - 1)
        res, i = True, 0

        if cnt == -1:
            i = 0
            n = individual.count
        else:
            i = random.randint(0, individual.count-1)
            n = random.randint(i+1, individual.count)

        
        while i < n:
            j = (i + 1) % (individual.count)
            k =  (j + 1) % (individual.count)
            while k < individual.count:
                l =  (k + 1) % (individual.count)
                if individual.vertexs.intersection(individual[i].id,
                                                   individual[j].id,
                                                   individual[k].id,
                                                   individual[l].id):
                    fx, x = individual.fx, individual.x
                    change(j, k)    
                    if individual.fitness() > fx*1.02:
                        change(j, k)
                        old = individual.wslice(None, None)
                        base = individual.wslice(None, None)
                        if j > l:
                            lst = base[j:] + base[:l]
                            individual.dna = base[l:j] + lst[::-1]
                        else:   
                            lst = base[j : l]
                            individual.dna = base[:j] + lst[::-1] + base[l:]
                        
                        individual.renum2()
                        if individual.fitness() > fx*1.05:
                            individual.dna = old
                            individual.fitness()
                k += 1
            i +=1
                    

class Gready(ga.Mutation):
    def __init__(self):
            ga.Mutation.__init__(self)
            self.name = 'Gready'
            self.rate = 0.7
            
    def mutate(self, individual, cnt, population):
        cities = {}
        
        def changeid(idx1, idx2):
            individual[idx2]._id, individual[idx1]._id = individual[idx1]._id, individual[idx2]._id

      
        def changeval(idx1, idx2):
            cities[idx1][0], cities[idx2][0] = cities[idx2][0], cities[idx1][0]

        #print [[g.id, g.val]  for g in individual.dna]

        if cnt == -1:
            idx1, idx2 = 0, individual.count -1
        else:   
            idx1 = random.randint(0, individual.count-2)
            idx2 = random.randint(idx1+1, individual.count-1)

        fx = individual.fitness()

        for c in individual.dna:
            cities[c.id] = [c.val,0]
            
        for idx in xrange(idx1, idx2):
            city_id = individual[idx].id
            next_id = individual[idx+1].id
            cities[city_id][1] = 1
            near_city_id = individual.vertexs.near(city_id, cities)
            if near_city_id > 0:
                cities[near_city_id] = [idx+1, 1]
                idx2 = cities[near_city_id][0]
                #print city_id, near_city_id, idx2
                cities[next_id][0] = idx2
                changeid(idx+1, idx2)
                #print [[g.id, g.val]  for g in individual.dna]
                #print [[idx, cities[idx]] for idx in xrange(len(cities))]
            
        
        #print "result", individual.fitness(), fx
        if individual.fitness() < fx*individual.back:
            CrossFide().mutate(individual, cnt, population)

class CrossingoverTSP (ga.Crossingover):
    def __init__(self):
            ga.Crossingover.__init__(self)
            self.rate = 0.10
    def after_mutate(self, children, res, population):
        for child in children:
            CrossFide().mutate(child, 0, population)   

class TSP( object ):
    def __init__(self, iteration, lenfoo):
        self.vertexs = vertexs.Vertexs(lenfoo)
        self.tspga = None
        self.iteration = iteration

    def after_best_create(self, best):
        CrossFide().mutate(best, 0, None)

    def calc(self):
        self.tspga = ga.Evolution(size = 180, iteration = self.iteration, mutationtype = ga.muRandom,
                                  generatemutation = 20, populationratemutation = 90,
                                  ClassIndividual = Way, MutationsClass = [CrossingoverTSP, ExchangeCity, MoveCity, Gready], #MoveCity
                                  args = [self.vertexs])

        self.tspga.after_best_create = self.after_best_create
        self.tspga.init()
        self.tspga.calc()
        best = self.tspga.population.best
        best.ordval()
        self.setimage(best)
        self.save(best)

    def setimage(self, best):
        im = Image.new("RGB", (512, 512), "white")
        draw = ImageDraw.Draw(im)
        for i in xrange(best.count-1):
            #draw.text(i, (self.vertexs[best[i].id].lon, self.vertexs[best[i].id].lat-2), 'black')
            draw.ellipse((self.vertexs[best[i].id].lon-2, self.vertexs[best[i].id].lat-2,
                          self.vertexs[best[i].id].lon+2, self.vertexs[best[i].id].lat+2),
                          (0,0,0))

            draw.line((self.vertexs[best[i].id].lon, self.vertexs[best[i].id].lat,
                       self.vertexs[best[i+1].id].lon, self.vertexs[best[i+1].id].lat),(0,0,0))

        draw.ellipse((self.vertexs[best[-1].id].lon-2, self.vertexs[best[-1].id].lat-2,
                      self.vertexs[best[-1].id].lon+2, self.vertexs[best[-1].id].lat+2),
                      (0,0,0))

        draw.line((self.vertexs[best[-1].id].lon, self.vertexs[best[-1].id].lat,
                   self.vertexs[best[0].id].lon, self.vertexs[best[0].id].lat), (0,0,0))

        im.save("result.bmp", "BMP")


    def save(self, best):
        data = [(self.vertexs[c.id].lon, self.vertexs[c.id].lat) for c in best.dna]
        data = {"cities" : data}
        with open('result.json', 'w') as outfile:
            json.dump(data, outfile)
   
        
    def load(self, filename):
        f = open(filename)
        data = json.load(f)
        cities = data["cities"]
        for c in cities:
            v = self.vertexs.add()
            v.lon, v.lat = c[0], c[1]
        f.close()
        self.vertexs.calcmatrix()
        #print self.vertexs

if __name__ == "__main__":
    import json, math
    foostraightlen = lambda v1, v2: int(math.pow(math.pow((v1.lon - v2.lon),2) +
                                                 math.pow((v1.lat - v2.lat),2), 0.5))
    tsp = TSP(3000, foostraightlen)
    tsp.load('testt.json')
    #print tspvertexs.vertexlist
    #print tsp.vertexs.distance[1][9]

    tsp.calc()


    
        
        








        
