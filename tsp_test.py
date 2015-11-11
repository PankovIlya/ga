import tsp as ts
import math, time

foostraightlen = lambda v1, v2: round((math.pow(math.pow((v1.lon - v2.lon),2) +
                                              math.pow((v1.lat - v2.lat),2), 0.5)),2)
t = time.time()
res = []
for i in xrange(500):
    tsp = ts.TSP(2000, i, foostraightlen)
    tsp.load('testt.json')
    #print tspvertxs.vertexlist
    #print tsp.vertexs.distance[1][9]
    tsp.calc()
    res += [tsp.best]
    
l100 = filter(lambda x: tsp.best.fx < 2092.60, res)
l100.sort(key = lambda x: x.num_gn)
print 'opt', len(l100), 'rrr', [x.num_gn for x in l100] 
l100 = filter(lambda x: 2092.60 < tsp.best.fx < 2100, res)
l100.sort(key = lambda x: x.fx)
print 'result < 2100', len(l100), 'rrr', [x.fx for x in l100] 
print time.time() - t
