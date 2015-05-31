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


    def printbest(self):
        for g in self.dna:
            print g.id, g.val

            
    def renum(self):
        self.ordval()
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

    def randomcreate(self):
        cnt = self.vertexs.count
        if cnt < 2:
            raise Exception('City count < 2!')
        for i in xrange(cnt):
            g = self.addgen()

        random.shuffle(self.dna)

        for i in xrange(cnt):
            self[i].val = i 

        self.fitness()
        CrossFide().mutate(self, 0)

         

class ExchangeCity(ga.Mutation):
    def mutate(self, individual, cnt):
        def change(idx1, idx2):
            idc = individual[idx2]._id
            individual[idx2]._id = individual[idx1]._id
            individual[idx1]._id = idc
            
        fx = individual.fx
        for _ in xrange(cnt):
            idx1 = random.randint(0, individual.count-1)
            idx2 = random.randint(0, individual.count-1)
            change(idx1, idx2)

        if individual.fitness() < fx*individual.back:
            CrossFide().mutate(individual, cnt)


class MoveCity(ga.Mutation):
    def mutate(self, individual, cnt):
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
            CrossFide().mutate(individual, cnt)


class CrossFide(ga.Mutation):
    def mutate(self, individual, cnt):
        def change(idx1, idx2):
            idc = individual[idx2]._id
            individual[idx2]._id = individual[idx1]._id
            individual[idx1]._id = idc
            
        #start = random.randint(0, individual.count - cnt - 1)
        for i in xrange(0, individual.count - 2):
            for j in xrange(i+2, individual.count):
                if individual.vertexs.intersection(individual[i].id,
                                                   individual[i+1].id,
                                                   individual[j].id,
                                                   individual[(j+1) % (individual.count)].id):
                    fx, x = individual.fx, individual.x
                    change(i+1, j)
                    if individual.fitness() > fx:
                        change(i+1, j)
                        individual.fx = x

                    

class Gready(ga.Mutation):
    def mutate(self, individual, cnt):
        def change(idx1, idx2):
            val = individual[idx2].val
            individual[idx2].val = individual[idx1].val
            individual[idx1].val = val

        idx1 = random.randint(0, individual.count-2)
        idx2 = random.randint(idx1+1, individual.count-1)

        fx = individual.fx

        for idx in xrange(idx1, idx2):
            idcity = individual[idx].id
            nextcity = individual[idx+1].id
            nearcity = individual.vertexs.near(idcity)
            individual.ordid()
            change(nextcity, nearcity)
            individual.ordval()

        if individual.fitness() < fx*individual.back:
            CrossFide().mutate(individual, cnt)



class TSP( object ):
    def __init__(self, iteration, lenfoo):
        self.vertexs = vertexs.Vertexs(lenfoo)
        self.tspga = None
        self.iteration = iteration

    def calc(self):
        self.tspga = ga.Evolution(size = 50, iteration = self.iteration, mutationtype = ga.muRandom,
                                  generatemutation = 4, populationratemutation = 100,
                                  ClassIndividual = Way, MutationsClass = [ExchangeCity, MoveCity], #MoveCity
                                  args = [self.vertexs])
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
            #draw.text(i, (self.vertexs[best[i].id].lon, self.vertexs[best[i].id].lat-2), (0,0,0))
            draw.ellipse((self.vertexs[best[i].id].lon-2, self.vertexs[best[i].id].lat-2,
                          self.vertexs[best[i].id].lon+2, self.vertexs[best[i].id].lat+2),
                          (0,0,0))

            draw.line((self.vertexs[best[i].id].lon, self.vertexs[best[i].id].lat,
                       self.vertexs[best[i+1].id].lon, self.vertexs[best[i+1].id].lat),(0,0,0))

        #draw.line((self.vertexs[best[-1].id].lon, self.vertexs[best[-1].id].lat,
        #              self.vertexs[best[0].id].lon, self.vertexs[best[0].id].lat), (0,0,0))

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

if __name__ == "__main__":
    import json, math
    foostraightlen = lambda v1, v2: int(math.pow(math.pow((v1.lon - v2.lon),2) +
                                                  math.pow((v1.lat - v2.lat),2), 0.5))
    tsp = TSP(5000, foostraightlen)
    tsp.load('points.json')
    #print tsp.vertexs.vertexlist
    #print tsp.vertexs.distance[1][9]

    tsp.calc()


    
        
        








        
