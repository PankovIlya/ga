import tsp as ts
import math, time

foostraightlen = lambda v1, v2: int(math.pow(math.pow((v1.lon - v2.lon),2) +
                                              math.pow((v1.lat - v2.lat),2), 0.5))
t = time.time()
res = []
for i in xrange(50):
    tsp = ts.TSP(500, i, foostraightlen)
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
