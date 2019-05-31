def read_txt(path):
    weights = {}
    nodes = []
    with open(path, 'r') as file:
        lines = file.readlines()
        i = 1
        for line in lines[1:]:
            weight = int(line.rstrip())
            weights[i] = weight
            nodes.append(i)
            i += 1
    return nodes, weights

def MIS(nodes, weights):
    """
    Find the MIS with given nodes.

    Params:
        nodes: a list of nodes;
        weights: the weight map.
    
    Return:
        IS: the maximum IS.
    """

    ## cost1 records total cost 1 step before
    ## cost2 records total cost 2 steps before
    ## cost records current total cost
    cost1 = weights[nodes[0]]
    cost2 = 0
    cost = 0

    ## IS1 records nodes set 1 step before
    ## IS2 records nodes set 2 steps before
    ## IS records current nodes set
    IS1 = {nodes[0]}
    IS2 = set()
    IS = set()

    for i in range(1, len(nodes)):
        node = nodes[i]
        w = weights[node]

        ## Add current node or remain the same
        if cost2 + w > cost1:
            cost = cost2 + w
            ## Note that set should be copied instead of assignmnet
            IS = IS2.copy()
            IS.add(node)
        
        else:
            cost = cost1
            ## Note that set should be copied instead of assignmnet
            IS = IS1.copy()
        
        cost2, cost1 = cost1, cost
        IS2, IS1 = IS1, IS

    return IS

if __name__ == "__main__":
    nodes, weights = read_txt("mwis.txt")
    IS = MIS(nodes, weights)
    
    answer = ""
    for i in [1, 2, 3, 4, 17, 117, 517, 997]:
        if i in IS:
            answer += "1"
        else:
            answer += "0"
    print(answer)
    ## outputs: 10100110