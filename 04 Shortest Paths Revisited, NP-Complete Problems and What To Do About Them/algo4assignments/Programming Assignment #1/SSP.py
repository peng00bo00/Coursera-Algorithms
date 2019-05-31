from heap import AdaptablePriorityQueue

class Edge:
    __slots__ = "node1", "node2", "weight"
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
    
    def __gt__(self, other):
        return self.weight > other.weight
    
    def __lt__(self, other):
        return self.weight < other.weight
    
    def __str__(self):
        return f"Node1: {self.node1}, Node2: {self.node2}, Weight: {self.weight}"


def read_txt(path):
    """
    Read the txt file and return a graph.
    """

    V, E = [], []
    with open(path) as file:
        lines = file.readlines()

        for line in lines[1:]:
            u, v, weight = line.split(' ')
            weight = int(weight)

            if u not in V:
                V.append(u)
            if v not in V:
                V.append(v)
        
            E.append(Edge(u, v, weight))

    return V, E

def BellmanFord(V, E, s):
    """
    Find the shortest path of a graph from source node s with Bellman-Ford algorithm.

    Params:
        V, E: vertices and edges of a graph;
        s: the source node.
    
    Return:
        ret: a boolean variable denotes whether there are negative cycles in the graph;
        paths: the shortest paths from the source node to the others. Note that paths are meaningless when ret=True.
    """
    
    def check_paths(paths1, paths2):
        """
        Check whether 2 paths are the same.
        """
        
        assert paths1.keys() == paths2.keys()
        for key in paths1:
            if paths1[key] != paths2[key]:
                return False
        return True

    ## Initialization
    ret = False
    paths = {v: float("inf") for v in V}
    paths[s] = 0
    

    for _ in range(len(V) - 1):
        _paths = paths.copy()
        for e in E:
            u, v, weight = e.node1, e.node2, e.weight
            ## Relaxation
            paths[v] = min(paths[v], paths[u] + weight)
        ## Stop early if there are no changes in paths
        if check_paths(paths, _paths):
            return ret, paths
    
    ## Check if there are negative cycles
    for e in E:
        u, v, weight = e.node1, e.node2, e.weight
        
        if paths[v] > paths[u] + weight:
            ret = True
            return ret, paths

    return ret, paths

def Dijkstra(V, E, s, edges=None):
    """
    Find the shortest path of a graph from source node s with Dijkstra algorithm.

    Params:
        V, E: vertices and edges of a graph;
        s: the source node;
        edges (optional): a dict records each edge from each vertices.
    
    Return:
        paths: the shortest paths from the source node to the others.
    """

    ## Initialization
    d = {}                          ## d[v] records upper bound of node v
    locs = {}                       ## locs[v] records locators of node v
    paths = {}                      ## paths[v] records shortest path from node s to node v
    heap = AdaptablePriorityQueue() ## heap records current shortest path from node s to node v

    ## Compute edges if not provided
    if not edges:
        edges = {u: [e for e in E if e.node1 == u] for u in V}

    for v in V:
        if v == s:
            d[v] = 0
        else:
            d[v] = float("inf")
        locs[v] = heap.push(d[v], v)
    
    while not heap.is_empty():
        weight, u = heap.pop()
        paths[u] = weight
        locs.pop(u)
        for e in edges[u]:
            v = e.node2
            if v not in paths:
                ## Relaxation
                if d[u] + e.weight < d[v]:
                    d[v] = d[u] + e.weight
                    heap.update(locs[v], d[v], v)

    return paths

def Johnson(V, E):
    """
    Find the APSP with Johnson algorithm.

    Params:
        V, E: vertices and edges of a graph.

    Return:
        D: the shortest paths for every pair of nodes in the graph.
    """

    ## Add a new node "s" in the graph
    V_p = ['s'] + V
    E_p = [Edge('s', v, 0) for v in V] + E
    ## Find the weight of each node in V with Bellman-Ford algorithm
    ret, weights = BellmanFord(V_p, E_p, "s")

    if ret:
        print("NULL")
        return None
    else:
        ## Remove the added node "s"
        weights.pop("s")

        ## Reweight the edges
        E2 = []
        for e in E:
            u, v, weight = e.node1, e.node2, e.weight
            weight2 = weight + weights[u] - weights[v]
            E2.append(Edge(u, v, weight2))
        
        ## Find the shortest paths with Dijkstra algorithm on G(V, E2)
        D = {}
        edges = {u: [e for e in E2 if e.node1 == u] for u in V}
        for u in V:
            paths = Dijkstra(V, E2, u, edges)

            ## Modify D to get the shortest distances.
            for v in V:
                paths[v] = paths[v] - weights[u] + weights[v]
            
            D[u] = paths
        return D

if __name__ == "__main__":
    V, E = read_txt('large.txt')
    D = Johnson(V, E)
    if D:
        shortest = min([min(D[d].values()) for d in D])
        print(f"Shortest Path: {shortest}")
    # output: g1 => NULL
    #         g2 => NULL
    #         g3 => -19