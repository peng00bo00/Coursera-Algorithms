import sys   
sys.setrecursionlimit(100000)

def read_txt(path):
    items = []
    with open(path, "r") as file:
        lines = file.readlines()
        constraint, _ = lines[0].rstrip().split(" ")
        constraint = int(constraint)

        for line in lines[1:]:
            value, weight = line.rstrip().split(" ")
            value, weight = int(value), int(weight)
            items.append(Item(value, weight))
    
    return items, constraint


class Item:
    __slots__ = "value", "weight"

    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
    
    def __str__(self):
        return "Value: {}, Weight: {}".format(self.value, self.weight)

def recursive_knapsack(items, constraint):
    """
    Find the maximum value in the items with constraint recursively. Can be slower in small cases, but MUCH FASTER IN LARGE CASES.

    Params:
        items: a list of items with value and weight;
        constraint: the weight constraint.
    
    Return:
        Vmax: the maximum value of items
    """

    def helper(items, item, constraint, acc):
        """
        A helper function in recursion.

        Params:
            items: current item list;
            item: item as the index key, not included in items;
            constraint: current weight constraint;
            acc: accumulator.
        
        Return:
            Vmax: current maximum value;
            acc: updated accumulator.
        """

        value, weight = item.value, item.weight

        ## Try to look up in the acc first
        if (item, constraint) in acc:
            return acc[(item, constraint)], acc

        ## Vmax = 0 when constraint <= 0
        elif constraint <= 0:
            return 0, acc

        ## Vmax = 0 or item.value when there is nothing left in items
        elif len(items) == 0:
            ## Vmax = item.value if item.weight <= constraint
            if weight <= constraint:
                return value, acc
            ## Vmax = 0 if item.weight > constraint
            else:
                return 0, acc

        ## if weight > constraint, Vmax is the max value with the next item and the same constraint
        elif weight > constraint:
            item = items.pop()
            return helper(items, item, constraint, acc)
        
        ## Compute Vmax in other cases and try looking up in acc if possible
        else:
            ## V1 is the max value if current item is excluded
            _item = items[-1]
            _items = items[:-1]
            V1, acc = helper(_items, _item, constraint, acc)
            ## V2 is the max value if current item is included (if possible)
            V2, acc = helper(_items, _item, constraint-weight, acc)
            V2 += value
            
            Vmax = max(V1, V2)
            ## Add Vmax in the acc
            acc[(item, constraint)] = Vmax

            return Vmax, acc

    item = items.pop()
    Vmax, acc = helper(items, item, constraint, {})
    return Vmax, acc

def knapsack(items, constraint):
    """
    Find the maximum value in the items with constraint.

    Params:
        items: a list of items with value and weight;
        constraint: the weight constraint.
    
    Return:
        Vmax: the maximum value of items
    """
    
    ## Only 2 columns are useful indeed
    V = [[0 for _ in range(2)] for _ in range(constraint + 1)]
    Vmax = 0

    for j in range(1, (len(items)+1)):
        item = items[j-1]
        value, weight = item.value, item.weight
        for i in range(weight, constraint+1):
            ## V1 is the max value if current item is excluded
            V1 = V[i][0]
            ## V2 is the max value if current item is included (if possible)
            V2 = V[i-weight][0] + value
            V[i][1] = max(V1, V2)
        ## Copy the 2nd column to the 1st column
        for i in range(constraint+1):
            V[i][0] = V[i][1]
    ## Vmax is the last value in V
    Vmax = V[-1][0]
    
    return Vmax

if __name__ == "__main__":
    items, constraint = read_txt("knapsack_big.txt")
    Vmax, acc = recursive_knapsack(items, constraint)
    #Vmax = knapsack(items, constraint)
    print(Vmax)
    ## outputs: 4243395
    ## knapsack takes about 40 min to compute but the recursion version takes only 2 min