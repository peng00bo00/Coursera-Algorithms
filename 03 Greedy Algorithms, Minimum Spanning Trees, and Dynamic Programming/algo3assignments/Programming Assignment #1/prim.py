import heapq

class Edge:
    def __init__(self, node1, node2, cost):
        self.node1 = node1
        self.node2 = node2
        self.cost = cost

    def __gt__(self, edge):
        return self.cost > edge.cost
    
    def __lt__(self, edge):
        return self.cost < edge.cost

class Node:
    def __init__(self, Id, cost):
        self.Id = Id
        self.cost = cost
    
    def __gt__(self, node):
        return self.cost > node.cost
    
    def __lt__(self, node):
        return self.cost < node.cost

def read_txt(path):
    """
    Read the txt file and return a graph.
    """

    V, E = [], []
    with open(path) as file:
        lines = file.readlines()

        for line in lines[1:]:
            u, v, cost = line.split(' ')
            cost = int(cost)

            if u not in V:
                V.append(u)
            if v not in V:
                V.append(v)
        
            E.append(Edge(u, v, cost))

    return V, E

def Prim(V, E):
    """
    Find the LST with Prim algorithm.

    Params:
        V, E: Vertices and Edges of a graph.
    
    Return:
        cost: Total cost of the LST.
    """
    
    cost = 0
    heap = [Node(v, float("inf")) for v in V]
    heap[0].cost = 0
    heapq.heapify(heap)

    while len(heap) > 0:
        node = heapq.heappop(heap)
        cost += node.cost

        edges = [edge for edge in E if node.Id in [edge.node1, edge.node2]]
        for edge in edges:
            if edge.node1 == node.Id:
                u = edge.node2
            else:
                u = edge.node1
            
            for v in heap:
                if v.Id == u and v.cost > edge.cost:
                    v.cost = edge.cost
        
        heapq.heapify(heap)

    return cost


if __name__ == "__main__":
    V, E = read_txt('edges.txt')
    cost = Prim(V, E)
    print(cost)
    # output: -3612829