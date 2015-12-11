import json


def parse(filename):
    f = open(filename)
    res = []
    lstr = f.readline()
    while lstr:
        res += [lstr.rstrip('\n')]
        lstr = f.readline()
    return res

lst = parse('test2.txt')

print lst  
