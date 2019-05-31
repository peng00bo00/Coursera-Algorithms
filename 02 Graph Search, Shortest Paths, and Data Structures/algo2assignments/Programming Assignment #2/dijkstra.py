def read_txt(path):
    V, E, edges = [], [], []
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.rstrip().split("\t")
            V.append(line[0])
            for e in line[1:]:
                edges.append(line[0] + ',' + e)
    
    E = [[0 for u in V]for u in V]
    for edge in edges:
        u, v, w = edge.split(',')
        u_idx, v_idx = Index(u, V), Index(v, V)
        E[u_idx][v_idx] = int(w)
    return V, E

def Index(u, V):
    """
    A helper function to get index of a vetex u in the graph.
    """

    return V.index(u)

def shortest(visited, paths):
    """
    A helper function to find the shortest unvisited node index.
    """
    shortest = float("inf")
    index = -1
    for i, path in enumerate(paths):
        if not visited[i] and path < shortest:
            index = i
            shortest = path
    return index


def Dijkstra(V, E, s):
    """
    Find the shortest paths in the graph from the source node with Dijkstra algorithm.

    Params:
        V, E: vertices and edges in the graph;
        s: the source node.
    
    Return:
        paths: shortest paths from the source node to every vertices in the graph.
    """

    visited = [False for u in V]
    paths = [float("inf") for u in V]
    paths[Index(s, V)] = 0

    for _ in range(len(V)):
        shortest_idx = shortest(visited, paths)
        visited[shortest_idx] = True
        edges = E[shortest_idx]

        for i, edge in enumerate(edges):
            if edge > 0 and paths[shortest_idx] + edge < paths[i]:
                paths[i] = paths[shortest_idx] + edge
    
    return paths
        

if __name__ == "__main__":
    V, E = read_txt("dijkstraData.txt")
    # V = ['s', 't', 'x', 'y', 'z']
    # E = [[0, 10, 0, 5, 0],
    #      [0,  0, 1, 2, 0],
    #      [0,  0, 0, 0, 4],
    #      [0,  3, 9, 0, 2],
    #      [7,  0, 6, 0, 0]]
    paths = Dijkstra(V, E, '1')
    for u in map(str, [7,37,59,82,99,115,133,165,188,197]):
        print(paths[Index(u, V)], end=',')
    # outputs: 2599,2610,2947,2052,2367,2399,2029,2442,2505,3068
