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

#lst = parse('result.json')['cities']

def load(filename):
    f = open(filename)
    data = json.load(f)
    return data["cities"]


lst = load('result.json') 
lenw = 0

foo = lambda x1,x2,y1,y2 : round((((x1 - x2)**2 + (y1 - y2)**2)**0.5),0)

for idx in xrange(len(lst) - 1):
    lenw += foo(lst[idx][0], lst[idx+1][0], lst[idx][1], lst[idx+1][1])
    
print lenw + foo(lst[-1][0], lst[0][0], lst[-1][1], lst[0][1])


#with open('testg.json', 'w') as outfile:
#            json.dump(parse('test1.txt'), outfile)
