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

def knapsack(items, constraint):
    """
    Find the maximum value in the items with constraint.

    Params:
        items: a list of items with value and weight;
        constraint: the weight constraint.
    
    Return:
        Vmax: the maximum value of items
    """
    
    V = [[0 for _ in range(len(items)+1)] for _ in range(constraint + 1)]
    Vmax = 0

    for i in range(1, constraint+1):
        for j in range(1, (len(items)+1)):
            item = items[j-1]
            value, weight = item.value, item.weight
            ## V1 is the max value if current item is excluded
            V1 = V[i][j-1]
            ## V2 is the max value if current item is included (if possible)
            if i - weight < 0:
                V2 = 0
            else:
                V2 = V[i-weight][j-1] + value
            V[i][j] = max(V1, V2)
    ## Vmax is the last value in V
    Vmax = V[-1][-1]
    return Vmax

if __name__ == "__main__":
    items, constraint = read_txt("knapsack1.txt")
    Vmax = knapsack(items, constraint)
    print(Vmax)
    ## outputs: 2493893