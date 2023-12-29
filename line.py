import numpy as np

class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
        xa,ya = self.a
        xb,yb = self.b
        
        if xa==xb:
            self.slope = np.inf
            self.intercept = None
        else:
            self.slope = (ya - yb)/(xa - xb)
            self.intercept = ya - self.slope*xa

    def __repr__(self):
        if self.slope ==0:
            ret = f'y = {self.intercept:.3f}'
        elif self.slope == np.inf:
            ret = f'x = {self.a[0]:.3f}'
        else:
            ret = f'y = {self.slope:.3f}x + {self.intercept:.3f}'
        return f'Line: {ret} \nEnd points: a: {self.a}, b: {self.b}'
    
    def get_intersection_point_with_line(self, line):
        a1 = self.a
        a2 = self.b
        b1, b2 = line.a, line.b

        s = np.vstack([a1,a2,b1,b2])        # s for stacked
        h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
        l1 = np.cross(h[0], h[1])           # get first line
        l2 = np.cross(h[2], h[3])           # get second line
        x, y, z = np.cross(l1, l2)          # point of intersection
        if z == 0:                          # lines are parallel
            return False
            # return (float('inf'), float('inf'))
        point = (x/z, y/z)
        
        if not (line.contains_point_within_segment(point) and self.contains_point_within_segment(point)):
            return False
        return point
        

    def get_point_from_x(self, x):
        if self.slope == np.inf:
            return x==self.a[0]

        y = self.slope*x + self.intercept
        return (x, y)
    
    def get_point_from_y(self, y):
        if self.slope == 0:
            return y == self.a[1]

        x = (y - self.intercept)/self.slope
        return (x, y)

    def contains_point(self, point):
        x,y = point
        if self.slope == np.inf:
            return np.isclose(x, self.a[0], rtol=5e-3)

        y_ = x*self.slope + self.intercept
        return np.isclose(y, y_, rtol=5e-3)

    def contains_point_within_segment(self, point):
        if not self.contains_point(point):
            print('sdsds')
            return False

        x,y = point
        xa,ya = self.a
        xb,yb = self.b

        within_x = max(xa,xb) + 5e-3 >= x >= min(xa,xb) - 5e-3
        within_y = max(ya,yb) + 5e-3 >= y >= min(ya,yb) - 5e-3
        return within_x and within_y
