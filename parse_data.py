import json

def parse(filename):
    f = open(filename)
    res = []
    x = f.readline()
    while x:
        y = f.readline()
        x = x.split('\n')[0]
        y = y.split('\n',)[0]
        res += [[int(x), int(y)]]
        x = f.readline()

    res = {"structure" : ["x", "y"], "cities": res}
    return res

with open('testx.json', 'w') as outfile:
            json.dump(parse('test1.txt'), outfile)
