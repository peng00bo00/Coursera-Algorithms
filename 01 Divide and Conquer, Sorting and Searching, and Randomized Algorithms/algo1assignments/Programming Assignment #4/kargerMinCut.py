import random
from copy import deepcopy

def read_txt(path):
    V, E = [], []
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.rstrip().split("\t")
            idx, line = int(line[0]), line[1:]
            V.append(idx)
            for vertex in line:
                v1, v2 = idx, int(vertex)
                if v1 > v2:
                    v1, v2 = v2, v1
                if [v1, v2] not in E:
                    E.append([v1, v2])

    return (V, E)

def MinCut(graph, N):
    """
    Find the min cut of a given graph.

    Params:
        graph: a tuple (V, E) to represent a graph;
        N: number of iterations.

    Return:
        mincut: the number of min cut.
    """

    V, E = graph
    mincut = len(V)
    ## Run N iterations
    for _ in range(N):
        v, e = deepcopy(V), deepcopy(E)
        while len(v) > 2:
            v1, v2 = random.choice(e)
            v.remove(v2)

            def mergev(edge):
                """
                Merge the two vertices on a given edge.
                """
                if v2 not in edge:
                    return edge
                elif edge[0] == v2:
                    edge[0] = v1
                elif edge[1] == v2:
                    edge[1] = v1
                
                if edge[0] > edge[1]:
                    edge[0], edge[1] = edge[1], edge[0]
                return edge
            
            e = list(map(mergev, e))
            e = list(filter(lambda edge: edge[0] != edge[1], e))
        
        if len(e) < mincut:
            mincut = len(e)
    return mincut
                


if __name__ == "__main__":
    V, E = read_txt("kargerMinCut.txt")
    print(MinCut((V, E), 100))
    #output: 17