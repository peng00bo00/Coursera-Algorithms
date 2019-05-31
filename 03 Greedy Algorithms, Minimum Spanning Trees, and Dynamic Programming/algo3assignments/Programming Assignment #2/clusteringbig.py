import itertools


def read_txt(path):
    V = {}
    with open(path, "r") as file:
        lines = file.readlines()
        _, bits = lines[0].rstrip().split(" ")
        bits = int(bits)
        for v, line in enumerate(lines[1:]):
            line = line.rstrip().split(" ")
            ## The bits are transfered to binary system
            V[v] = int("".join(line), 2)

    return V, bits


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


def ClusteringBig(V, dist=3, bits=24):
    """
    Clustering in a VERY BIG graph.

    Params:
        V: a graph;
        dist: the distance threshold;
        bits: bits code in describing each node.
    
    Return:
        num_clusters: the number of clusters.
    """

    forest = UnionFind()
    clusters = {v: forest.make_group(v) for v in V}

    ## dict records all the vertices with the same bit code
    dict = {}
    for key, value in V.items():
        if value not in dict:
            dict[value] = [key]
        else:
            ## Union the nodes with the same bit
            u = dict[value][0]
            p = forest.find(clusters[u])

            q = forest.find(clusters[key])
            forest.union(p, q)

            dict[value].append(key)
    
    ## Find all the possible bit changes
    idxs = []
    for distance in range(1, dist):
        idxs += list(itertools.combinations(range(bits), distance))

    ## Union the nodes within given distances
    for u in V:
        code = V[u]
        p = forest.find(clusters[u])
        
        for positions in idxs:
            new_code = code
            for i in positions:
                new_code = new_code ^ (1 << i)
                
            if new_code in dict:
                v = dict[new_code][0]
                q = forest.find(clusters[v])

                if p != q:
                    forest.union(p, q)
    
    num_clusters = len(set([forest.find(clusters[v]).element() for v in V]))

    return num_clusters

if __name__ == "__main__":
    V, bits = read_txt("clustering_big.txt")
    print(ClusteringBig(V, dist=3, bits=bits))
    ## outputs: 6118