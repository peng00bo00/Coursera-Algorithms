def read_txt(path):
    V, E = [], []
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines[1:]:
            node1, node2, cost = line.rstrip().split(" ")
            edge = Edge(node1, node2, int(cost))
            E.append(edge)

            if node1 not in V:
                V.append(node1)
            
            if node2 not in V:
                V.append(node2)

    return V, E

class Edge:
    def __init__(self, node1, node2, cost):
        self.node1 = node1
        self.node2 = node2
        self.cost = cost
    
    def endpoints(self):
        return self.node1, self.node2


class UnionFind:
    """
    A Union-Find data structure implementd by python.
    """

    class Node:
        __slots__ = "_container", "_element", "_size", "_parent"

        def __init__(self, container, element):
            self._element = element
            self._container = container
            self._size = 1
            self._parent = self
        
        def element(self):
            return self._element
    
    def make_group(self, e):
        """
        Make a new group containing element e.
        """

        return self.Node(self, e)

    def find(self, x):
        """
        Find the leader of a node.
        """

        if x._parent != x:
            x._parent = self.find(x._parent)
        return x._parent
    
    def union(self, p, q):
        """
        Merge the groups containing node p and q.
        """

        a = self.find(p)
        b = self.find(q)

        if a is not b:
            if a._size > b._size:
                b._parent = a
                a._size += b._size
            else:
                a._parent = b
                b._size += a._size


def clustering(V, E, k=4):
    """
    Group the graph into k clusters.

    Params；
        V, E: a graph;
        k: number of clusters.

    Return:
        spacing: the maximum spacing of k clusters.
    """

    E = sorted(E, key = lambda x: x.cost, reverse = True)
    forest = UnionFind()
    clusters = {v: forest.make_group(v) for v in V}
    
    num_clusters = len(clusters)
    
    ## Clustering the nodes to k groups
    while num_clusters > k:
        edge = E.pop()
        u, v = edge.endpoints()

        p = forest.find(clusters[u])
        q = forest.find(clusters[v])
        
        if p != q:
            forest.union(p, q)
            num_clusters -= 1
    
    #u, v = edge.endpoints()
    p = forest.find(clusters[u])
    q = forest.find(clusters[v])
    while p == q:
        edge = E.pop()
        u, v = edge.endpoints()
        p = forest.find(clusters[u])
        q = forest.find(clusters[v])
    
    spacing = edge.cost

    return spacing

if __name__ == "__main__":
    V, E = read_txt("clustering1.txt")
    print(clustering(V, E))
    ## outputs: 106