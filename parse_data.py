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


def load(filename):
    f = open(filename)
    data = json.load(f)
    cities = data["cities"]
    res = []
    for c in cities:
        res.append(c[0])
        res.append(c[1])
    f.close()
    with open('dtestt.txt', 'w') as outfile:
        for x in res:
            outfile.write(str(x)+'\n')
        outfile.close()
            

load('testt.json')
with open('testt.json', 'w') as outfile:
            json.dump(parse('test1.txt'), outfile)
