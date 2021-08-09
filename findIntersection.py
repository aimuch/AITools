
def findIntersection(x1,y1,x2,y2,x3,y3,x4,y4):
    px = ((x1*y2 - y1*x2) * (x3-x4) - (x1-x2) * (x3*y4 - y3*x4)) / ((x1-x2) * (y3-y4) - (y1-y2) * (x3-x4))
    py = ((x1*y2 - y1*x2) * (y3-y4) - (y1-y2) * (x3*y4 - y3*x4)) / ((x1-x2) * (y3-y4) - (y1-y2) * (x3-x4))
    return (px, py)

def findIntersectionArray(x, y):
    px = ((x[2] - x[3]) * (x[1] * y[0] - x[0] * y[1]) - (x[0] - x[1]) * (x[3] * y[2] - x[2] * y[3])) / ((x[2] - x[3]) * (y[0] - y[1]) - (x[0] - x[1]) * (y[2] - y[3]));
    py = ((y[2] - y[3]) * (y[1] * x[0] - y[0] * x[1]) - (y[0] - y[1]) * (y[3] * x[2] - y[2] * x[3])) / ((y[2] - y[3]) * (x[0] - x[1]) - (y[0] - y[1]) * (x[2] - x[3]));
    return (px, py)
