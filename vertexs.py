class Vertex( object):
    def __init__(self):
        self._id = 0
        self.num = 0
        self.name = ''
        self.lon = 0.0
        self.lat = 0.0
        self.timeid = 0
        self.weight = 0
        self.courierid = 0

    id = property(lambda self: self._id)

class Courier (object):
    def __init__(self):
        self.id = 0
        self.name = ''
  

class Couriers (object):
    def __init__(self):
        self.couriers = []

    count = property(lambda self: len(self.couriers))

    def __getitem__(self, i):
        return self.couriers[i]
    
    def add(self):
        res = Courier()
        self.couriers.append(res)
        return res


class Vertexs (object):
    def __init__(self, foocalcmatrix):
        self.vertexlist = []
        self.distance = []
        self.foocalcmatrix = foocalcmatrix

    count = property(lambda self: len(self.vertexlist))

    def __getitem__(self, i):
        return self.vertexlist[i]
        
    
    def calcmatrix(self):
        for i in xrange(self.count):
            a = []
            for j in xrange(self.count):
                if i <> j:
                    a.append(self.foocalcmatrix(self[i], self[j]))
                else:
                    a.append(2000000000)
            self.distance.append(a)

    def add(self):
        res = Vertex()
        res._id = self.count
        self.vertexlist.append(res)
        return res

    def intersection(self, v11, v12, v21, v22):
        def det (a, b, c, d):
            return a * d - b * c

        res = False
        
        ax1 = self[v11].lon;  ay1 = self[v11].lat;
        ax2 = self[v12].lon;  ay2 = self[v12].lat;
        bx1 = self[v21].lon;  by1 = self[v21].lat;
        bx2 = self[v22].lon;  by2 = self[v22].lat;

        zn = det(ay2-ay1, ax2-ax1, by2-by1, bx2-bx1)
        if  abs(zn) == 0:
            return res

        xi =   det((ax1*ay2 - ay1*ax2),ax2-ax1,(bx1*by2 - by1*bx2),bx2-bx1) / zn
        yi = - det(ay2-ay1, (ax1*ay2 - ay1*ax2), by2-by1, (bx1*by2 - by1*bx2)) / zn

        res = False
        if ((ax1 <=xi) and (ax2>=xi)) or ((ax1>=xi) and (ax2<=xi)):
            if ((ay1<=yi) and (ay2>=yi)) or ((ay1>=yi) and (ay2<=yi)):
                if ((bx1<=xi) and (bx2>=xi)) or ((bx1>=xi) and (bx2<=xi)):
                    if ((bx1<=xi) and (bx2>=xi)) or ((bx1>=xi) and (bx2<=xi)):
                        res = True
        return res

    def near(self, i):
        jm = 0
        for j in xrange(self.count):
            if self.distance[i][j] < self.distance[i][jm]:
                jm = j
        return jm
