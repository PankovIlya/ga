import ga2 as ga
import vertexs, tsp_optimizations as opt
import random as rand, os

from PIL import Image 
from PIL import ImageDraw
#from PIL import ImageFont


class Way (ga.Individual):

    def __init__(self, *args):
        super(self.__class__, self).__init__(*args)
        self.back = 1.10
        self.vertexs = args[0]
        self.sorted = True
                   
    def __str__(self):
##        for g in self.dna:
##            print g.id, g.val
        return super(self.__class__, self).__str__()


    def printbest(self):
        for g in self.dna:
            print g.id, g.val

    def wslice(self, n, m):
        dna = []
        for itm in self.dna[n:m]:
            gene = ga.Gene()
            gene._id, gene.val = itm.id, itm.val
            dna += [gene]
        return dna


            
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

            rand.shuffle(self.dna)

            for i in xrange(cnt):
                self[i].val = i 

        self.fitness()
        opt.Gready().mutate(self, 0, None)
        #CrossFide().mutate(self, -1, None)

class TSP( object ):
    def __init__(self, iteration, num, lenfoo):
        self.vertexs = vertexs.Vertexs(lenfoo)
        self.tspga = None
        self.iteration = iteration
        self.tt_num = num

    def after_best_create(self, best):
        CrossFide().mutate(best, 0, None)

    def result(self):
        return self.tspga.population.best.fx

    def calc(self):
        self.tspga = ga.Evolution(size = 190, iteration = self.iteration, 
                                  generatemutation = 20, populationratemutation = 90, ClassIndividual = Way,
                                  MutationsClasses = [opt.CrossingoverTSP, opt.ExchangeCity, opt.MoveCity], #Gready 
                                  args = [self.vertexs], ratestatic = False, kfactor = 40, tt_num = self.tt_num)

        self.tspga.after_best_create = self.after_best_create
        self.tspga.calc()
        best = self.tspga.population.best
        best.ordval()
        #self.setimage(best)
        #self.save(best)

    def setimage(self, best):
        im = Image.new("RGB", (512, 512), "white")
        draw = ImageDraw.Draw(im)
        #font = ImageFont.truetype("sans-serif.ttf", 16)
        #fonts_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts')
        #font = ImageFont.truetype(os.path.join(fonts_path, 'sans_serif.ttf'), 24)
        for i in xrange(best.count-1):
            #draw.text((self.vertexs[best[i].id].lon-5, self.vertexs[best[i].id].lat+5), str(i), (0,0,0), font = font)
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
    import json, math, time
    foostraightlen = lambda v1, v2: int(math.pow(math.pow((v1.lon - v2.lon),2) +
                                                  math.pow((v1.lat - v2.lat),2), 0.5))
    t = time.time()
    res = []
    for i in xrange(70):
        tsp = TSP(3500, i, foostraightlen)
        tsp.load('testt.json')
        #print tspvertxs.vertexlist
        #print tsp.vertexs.distance[1][9]
        tsp.calc()
        res += [tsp.result()]

    res.sort()
    l100 = filter(lambda x: x < 2076, res)
    print 'result < 2076', len(l100), 'rrr', l100
    l100 = filter(lambda x: 2076 < x < 2100, res)
    print 'result < 2100', len(l100), 'rrr', l100 
    print res
    print time.time() - t
            


    
        
        








        
