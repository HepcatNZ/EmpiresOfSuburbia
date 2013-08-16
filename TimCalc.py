import math

class TimCalc:
    def __init__(self):
        c = 1

#    def dist_to_point(self,x1,y1,x2,y2):
#        if x1 < x2:
#            a = float((x2-x1)*(x2-x1))
#        else:
#            a = float((x1-x2)*(x1-x2))
#        if y1 < y2:
#            b = float((y2-y1)*(y2-y1))
#        else:
#            b = float((y1-y2)*(y1-y2))
#        d = math.sqrt(a+b)
#        return (d)

    def dist_to_point(self,x1,y1,x2,y2):
        #print "x1",x1,"y1",y1,"\nx2",x2,"y2",y2
        a = float((x2-x1)*(x2-x1))
        b = float((y2-y1)*(y2-y1))
        c = a+b
        d = math.sqrt(c)
        return (d)

    def midpoint(self,points):
        x1 = points[0][0]
        y1 = points[0][1]
        x2 = points[1][0]
        y2 = points[1][1]
        return((x1 + x2)/2 , (y1 + y2)/2)