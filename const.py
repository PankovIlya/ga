coRandom = 0
coBest = 1
CrossingoverType = set ([coRandom, coBest])

muRandom = 0
muStatic = 1
MutationType = set ([muRandom, muStatic])

dsID = 0
dsVal = 1
cmp_id = lambda g1, g2: cmp(g1.id, g2.id) #or cmp(g1.Cour, g2.Cour)
cmp_val = lambda g1, g2: cmp(g1.val, g2.val) #or cmp(g1.Cour, g2.Cour) 
SortType = {dsID:cmp_id, dsVal:cmp_val}

otMin = 0
otMax = 1
optmin = lambda x: 1.0/(x+1.0)
optmax = lambda x: x
cmin = lambda x1, x2: cmp(x2, x1)
cmax = lambda x1, x2: cmp(x1, x2)
OptimisationType = {otMin:optmin, otMax:optmax}
CompareType = {otMin:cmin, otMax:cmax}
