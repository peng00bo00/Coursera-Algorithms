def read_txt(path):
    """
    Read the txt file and return a graph.
    """

    V, E = [], []
    with open(path) as file:
        lines = file.readlines()
        for line in lines:
            line = line.rstrip()
            u, v = line.split()
            u, v = int(u), int(v)
            if u not in V:
                V.append(u)
            if v not in V:
                V.append(v)
            E.append([u, v])
    return V, E

def DFS_VISIT(V, E, u, time, visited, start, finish):
    """
    Help function of DFS to mark start and finish time.

    Params:
        V, E: vertices and edges in the graph;
        u: the current vertex;
        time: the current time;
        visited: the visited state for each vertex;
        start: the start time for each vertex;
        finish: the finish time for each vertex.
    Return:
        time: the updated time;
        visted: the updated visited states;
        start: the updated start time;
        finish: the updated finish time.
    """

    time += 1
    ## Mark the start time and label the current vertex as visited
    idx = V.index(u)
    start[idx] = time
    visited[idx] = True
    ## Loop over all the edges starting from u
    edges = [edge for edge in E if edge[0]==u]
    for edge in edges:
        v = edge[1]
        j = V.index(v)
        if not visited[j]:
            time, visited, start, finish = DFS_VISIT(V, E, v, time, visited, start, finish)
    
    time += 1
    finish[idx] = time

    return time, visited, start, finish


def DFS(V, E):
    """
    Search a graph (V, E) with DFS. Return start and finish time.

    Params:
        V, E: vertices and edges in the graph.
    
    Return:
        start: start time for each vertex;
        finish: finish time for each vertex.
    """

    ## Initialize visited state for each vertex
    visited = [False for v in V]
    time = 0

    start = [0 for v in V]
    finish = [0 for v in V]

    for i, u in enumerate(V):
        if not visited[i]:
            time, visited, start, finish = DFS_VISIT(V, E, u, time, visited, start, finish)
    
    return start, finish

def reverse(V, finish):
    """
    A helper function to sort vertices in decreasing finish order.

    Params:
        V: vertices;
        finish: finish time for each vertices.
    
    Return:
        V_rev: vertices in decreasing finish order; 
        finish_rev: finish time in decreasing order.
    """

    assert len(V) == len(finish)
    if len(V) == 1:
        return V, finish
    else:
        mid = len(V) // 2
        VL, finishL = V[:mid], finish[:mid]
        VR, finishR = V[mid:], finish[mid:]

        VL, finishL = reverse(VL, finishL)
        VR, finishR = reverse(VR, finishR)

        V_rev, finish_rev = [], []
        i, j = 0, 0
        while i < len(VL) and j < len(VR):
            if finishL[i] > finishR[j]:
                V_rev.append(VL[i])
                finish_rev.append(finishL[i])
                i += 1
            else:
                V_rev.append(VR[j])
                finish_rev.append(finishR[j])
                j += 1
        
        if i == len(VL):
            V_rev = V_rev + VR[j:]
            finish_rev = finish_rev + finishR[j:]
        else:
            V_rev = V_rev + VL[i:]
            finish_rev = finish_rev + finishL[i:]

        return V_rev, finish_rev


def SCCs_VISIT(V, E, u, visited, scc):
    """
    Help function of SCCs to find scc.

    Params:
        V, E: vertices and edges in the graph;
        u: the current vertex;
        visited: the visited state for each vertex;
        scc: the current scc.
    Return:
        visted: the updated visited states;
        scc: the updated scc.
    """

    ## Add u into current scc
    scc.append(u)
    idx = V.index(u)
    visited[idx] = True
    ## Loop over all the edges [u, v] starting from u
    edges = [edge for edge in E if edge[0]==u]

    for edge in edges:
        v = edge[1]
        j = V.index(v)
        if not visited[j]:
            scc, visited = SCCs_VISIT(V, E, v, visited, scc)
    # for i, v in enumerate(V):
    #     if [u, v] in E and not visited[i]:
    #         scc, visited = SCCs_VISIT(V, E, v, visited, scc)
    

    return scc, visited

def SCCs(V, E):
    """
    Compute SCCs with Kosaraju's Two-Pass Algorithm. Return a list of SCCs.

    Params:
        V, E: vertices and edges in the graph.

    Return:
        sccs: a list of sccs.
    """

    sccs = []

    ## Compute finish time for each vertices.
    start, finish = DFS(V, E)

    ## Compute reverse graph.
    E_rev = [[v, u] for [u, v] in E]

    ## Run DFS on reverse graph with decreasing finish order.
    V_rev, finish_rev = reverse(V, finish)
    visited = [False for v in V_rev]

    for i, u in enumerate(V_rev):
        if not visited[i]:
            scc = []
            scc, visited = SCCs_VISIT(V_rev, E_rev, u, visited, scc)
            sccs.append(scc)
    return sccs


if __name__ == "__main__":
    V, E = read_txt('SCCs.txt')
    V = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    E = [['a', 'b'],
         ['b', 'c'],
         ['b', 'e'],
         ['b', 'f'],
         ['c', 'd'],
         ['c', 'g'],
         ['d', 'c'],
         ['d', 'h'],
         ['e', 'a'],
         ['e', 'f'],
         ['f', 'g'],
         ['g', 'f'],
         ['g', 'h'],
         ['h', 'h']]

    # V = ['x', 'y', 'z', 'u', 'v', 'w', 's', 't']
    # E = [['x', 'z'],
    #      ['y', 'z'],
    #      ['z', 'y'],
    #      ['z', 'w'],
    #      ['u', 'v'],
    #      ['u', 't'],
    #      ['v', 'w'],
    #      ['v', 's'],
    #      ['w', 'x'],
    #      ['s', 'z'],
    #      ['s', 'w'],
    #      ['t', 'u'],
    #      ['t', 'v']]

    # start, finish = DFS(V, E)
    # print(V)
    # print(finish)
    # V_rev, finish_rev = reverse(V, finish)
    # print(V_rev)
    # print(finish_rev)

    V, E = read_txt('SCCs.txt')
    sccs = SCCs(V, E)
    sccs = sorted(sccs, key=len, reverse=True)
    print(list(map(len, sccs))[:5])