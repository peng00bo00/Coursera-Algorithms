import math
import itertools

def read_txt(path):
    coords = []
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines[1:]:
            x, y = line.rstrip().split(" ")
            x, y = float(x), float(y)
            coords.append(Coord(x, y))

    return coords

class Coord:
    __slots__ = "_x", "_y"
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    def coordinate(self):
        return self._x, self._y
    
    def __str__(self):
        return f"X: {self._x}, Y: {self._y}"
    

def distance(coord1, coord2):
    """
    Return the distance between coord1 and coord2.
    """

    x, y = coord1.coordinate()
    z, w = coord2.coordinate()

    return math.sqrt((x-z)**2 + (y-w)**2)

def TSP(coords):
    """
    Solve the TSP with dynamic programming.

    Params:
        coords: a list of coordinates.
    
    Return:
        dist: the shortest distance.
    """
    
    ## find binary code for each vertex
    ## coord1 =>   1
    ## coord2 =>  10
    ## coord3 => 100 ...
    V = {coord: 1 << i for i, coord in enumerate(coords)}
    
    ## distances between every pair of nodes
    dists = {(V[u], V[v]): distance(u, v) for u in coords for v in coords}
    ## generate all the possible combinations for all coords
    ## coord1 + coord2 =>  11
    ## coord1 + coord3 => 101
    
    ## dp[(set_code, vertex_code)] is the shortest distance of a sub-problem with given destination vertex
    ## both sub-problem and destination vertex are represented in binary code
    ## the destination vertex is included in the sub-problem
    dp = {}
    dp[(1, 1)] = 0
    
    ## base code contains only the first vertex, which is 1
    code = 1
    remove = {}
    for m in range(1, len(coords)):
        remove[m] = []
        ## Find all the possible position changes
        Set = list(itertools.combinations(range(1, len(coords)), m))
        for S in Set:
            ## find the code for each sub problem
            new_code = code
            for i in S:
                new_code = new_code ^ (1 << i)
            
            for j in S:
                dp[(new_code, 1 << j)] = min([dp.setdefault((new_code ^ (1 << j), 1 << k), float("inf")) + dists[(1 << k, 1 << j)] for k in [0] + list(S) if k != j])
                remove[m].append((new_code, 1 << j))
        
        ## remove earlier keys to save memory
        if m > 2:
            for key in remove[m-2]:
                dp.pop(key)
            remove.pop(m-2)
    
    dist = min([dp[(2 ** len(coords)-1, 1 << j)] + dists[(1 << j, 1)] for j in range(1, len(coords))])
    return dist


if __name__ == "__main__":
    coords = read_txt("tsp.txt")
    dist = TSP(coords)
    print(dist)
    ## outputs: 26442.73030895475