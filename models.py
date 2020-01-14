import operator
from functools import reduce

class Clique():
    """
    Model for a clique of n points of a cloud.

    Required arguments:
        points -- points that make up the clique
    Optional arguments:
        k -- the clique appears when computing mutual k-nearest neighbours
    """

    def __init__(self, points, k = None):
        self.points = points
        self.k = k
        self.size = len(points)
        self.diameter = max([0] + [dist(*p) for p in combinations(points, 2)])

    def __eq__(self, other):
       return (set(self.points) == set(other.points) 
               and self.k == other.k)

    def __hash__(self):
        return reduce(operator.xor, [hash(p) for p in self.points])

    def __repr__(self):
        return str(self.points)

    def __str__(self):
        return (f"{self.size}-clique with points " 
                + str(self.points) 
                + " born at k = {self.k}")

class Simplex():
    """
    Simplex of R^n.

    Required arguments:
        points -- list of points that form the simplex (list of n-tuples)
    """
    def __init__(self, points):
        if not all([len(p) == len(points[0]) for p in points]):
            raise ValueError("All points of the simplex should have the same dimension")
        self.points = points

    @property
    def dim(self):
        """ Dimension of the simplex """
        return len(self.points)

    @property
    def faces(self):
        """ Returns a list of the faces of the simplex """
        if len(self.points) is 1:
            return []
        else:
            return [Simplex([q for q in self.points if q != p]) for p in self.points]

    def __eq__(self, other):
        return set(self.points) == set(other.points)

    def __hash__(self):
        return reduce(operator.xor, [hash(p) for p in self.points])

    def __repr__(self):
        return "S" + str(self.points)
    def __str__(self):
        return f"{self.dim}-simplex with points " + str(self.points)

class Chain():
    """
    Chain of n-simplices.

    Required arguments:
        simplices -- list of simplices of the chain
    """
    def __init__(self, simplices):
        if not all([s.dim == simplices[0].dim for s in simplices]):
            raise ValueError("All simplices of the chain should have the same dimension")
        self.simplices = set(simplices)

    @property
    def dim(self):
        """ Dimension of the chain"""
        return list(self.simplices)[0].dim

    @property
    def boundary(self):
        return sum([Chain(s.faces) for s in list(self.simplices)], Chain([]))
    
    @property
    def is_cycle(self):
        return len(self.boundary.simplices) is 0

    def __add__(self, other):
        return Chain(self.simplices ^ other.simplices)

    def __repr__(self):
        if len(self.simplices) is 0:
            return "C[]"
        else:
            return " + ".join([repr(s) for s in self.simplices])

    def __str__(self):
        return f"Chain of {self.dim}-simplices: " + str(self.simplices)
        
        
