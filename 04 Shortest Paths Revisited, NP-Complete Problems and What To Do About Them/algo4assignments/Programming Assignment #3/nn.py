import math
import copy

def read_txt(path):
    cities = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            id, x, y = line.rstrip().split()
            id = int(id)
            x, y = float(x), float(y)
            city = City(id, x, y)
            cities.append(city)
    return cities

class City:
    __slots__ = "_x", "_y", "_id"

    def __init__(self, id, x, y):
        self._id = id
        self._x = x
        self._y = y

def shortest(city, cities):
    """
    Find the shoretest city with the given one in the cities.
    
    Params:
        city: a given city.
    
    Return:
        idx: the shortest index;
        dist: the minimum distance.
    """
    
    dist = float("inf")
    idx = 0
    for i, _city in enumerate(cities):
        _dist = math.sqrt((city._x - _city._x)**2 + (city._y - _city._y)**2)
        if _dist < dist:
            dist = _dist
            idx = i
    return idx, dist
    

def NN(cities):
    """
    Find the shortest cost of traveller with nearest neighbor heuristic.

    Params:
        cities: a list of cities.
    
    Return:
        cost: the smallest cost.
    """

    _cities = copy.copy(cities)
    cost = 0

    city = _cities[0]
    _cities = cities[1:]

    while len(_cities) > 0:
        idx, dist = shortest(city, _cities)
        cost += dist

        city = _cities.pop(idx)
        
    cost += math.sqrt((cities[0]._x-city._x)**2 + (cities[0]._y-city._y)**2)
    
    return cost

if __name__ == "__main__":
    cities = read_txt("nn.txt")
    cost = NN(cities)
    print(cost)
    ## outputs: 1203406.5012708856