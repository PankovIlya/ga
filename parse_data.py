import json

def parse(filename):
    f = open(filename)
    res = []
    x = f.readline()
    while x:
        y = f.readline()
        x = x.rstrip('\n')
        y = y.rstrip('\n')
        res += [[int(x), int(y)]]
        x = f.readline()

    res = {"structure" : ["x", "y"], "cities" : res}
    return res

lst = parse('test1.txt')['cities']

lenw = 0
for idx in xrange(len(lst) - 1):
    lenw += ((lst[idx][0] - lst[idx+1][0])**2 + (lst[idx][1] - lst[idx+1][1])**2)**0.5
    
print lenw


#with open('testg.json', 'w') as outfile:
#            json.dump(parse('test1.txt'), outfile)
