import math
import random

def read_txt(path):
    clauses = []
    with open(path, "r") as file:
        lines = file.readlines()

        for line in lines[1:]:
            id1, id2 = line.rstrip().split(" ")
            id1, id2 = int(id1), int(id2)
            sign1, sign2 = True, True

            if id1 < 0:
                id1 = -id1
                sign1 = False
            
            if id2 < 0:
                id2 = -id2
                sign2 = False
            
            clause = Clause(id1, sign1, id2, sign2)
            clauses.append(clause)
    
    return clauses


class Clause:
    __slots__ = "id1", "sign1", "id2", "sign2"

    def __init__(self, id1, sign1, id2, sign2):
        self.id1 = id1
        self.sign1 = sign1
        self.id2 = id2
        self.sign2 = sign2

class Node:
    __slots__ = "id"

    def __init__(self, id):
        self.id = id
    
    def parent(self):
        """
        Return the parent id (real id) of this node.
        """
        if self.id % 2 == 0:
            return self.id // 2
        else:
            return self.id // 2 + 1
    
    def __str__(self):
        return "{}".format(self.id)

class Edge:
    __slots__ = "node1", "node2"

    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

def conNode(id):
    """
    Return a pair of nodes instance given real id.
    """

    return Node(2*id-1), Node(2*id)

def conEdge(id1, sign1, id2, sign2, dV):
    """
    Return a pair of edges instance.
    """

    ## odd number implies True state and even number implies False state
    node11, node12 = dV[2*id1-1], dV[2*id1]
    node21, node22 = dV[2*id2-1], dV[2*id2]
    ## construct edges with sign1 and sign2
    if sign1 and sign2:
        return Edge(node12, node21), Edge(node22, node11)
    elif not sign1 and sign2:
        return Edge(node11, node21), Edge(node22, node12)
    elif sign1 and not sign2:
        return Edge(node12, node22), Edge(node21, node11)
    elif not sign1 and not sign2:
        return Edge(node11, node22), Edge(node21, node12)


def Papadimitriou(clauses):
    """
    Solve the 2-SAT problem with Papadimitriou's 2-SAT algorithm.

    Params:
        clauses: a list of clauses, note that the number of clauses equals to the number of variables.
    
    Return:
        ret: whether there exists a state that satisfies all the clauses.
    """
    
    n = len(clauses)
    for _ in range(int(math.log2(n)+1)):
        ## initialize a random state
        state = [random.random()<0.5 for _ in range(n)]
        for _ in range(2*n*n):
            flag = True
            unsatisfied = []
            for clause in clauses:
                id1, sign1 = clause.id1, clause.sign1
                id2, sign2 = clause.id2, clause.sign2

                id1, id2 = id1-1, id2-1

                bool1 = state[id1]
                bool2 = state[id2]

                if not sign1:
                    bool1 = not bool1
                if not sign2:
                    bool2 = not bool2

                if bool1 or bool2:
                    continue
                else:
                    flag = False
                    unsatisfied.append(clause)
            
            if flag:
                return True
            else:
                clause = random.choice(unsatisfied)
                id1, sign1 = clause.id1, clause.sign1
                id2, sign2 = clause.id2, clause.sign2

                id1, id2 = id1-1, id2-1

                ## randomly choose a state
                rand = random.random() < 0.5
                if rand:
                    id = id1
                else:
                    id = id2
                    
                state[id] = not state[id]
    return False

def Tarjan(V, E):
    """
    Find the SCCs in a given graph with Tarjan algorithm.
    Params:
        V, E: vertices and edges of a graph.

    Return:
        SCCs: a list of SCCs.
    """
    
    ## --------- Start of tarjan(u) --------- ##
    def tarjan(u):
        """
        A helper function in Tarjan algorithm.
        """
        
        ## initialize TIME, DFN, LOW and VISITED for node u
        nonlocal TIME
        TIME += 1
        DFN[u] = TIME
        LOW[u] = TIME
        STACK.append(u)
        VISITED[u] = True

        edges = iter(E[u])
        
        #for edge in edges:
        for edge in edges:
            v = edge.node2
            ## visit v recursively if node v has not been visited
            if not VISITED[v]:
                tarjan(v)
                LOW[u] = min(LOW[u], LOW[v])
            ## update LOW[u] if v is still in the STACK
            elif v in STACK:
                LOW[u] = min(LOW[u], DFN[v])
        
        ## DFN[u] == LOW[u] means that u is the root of a search tree
        if DFN[u] == LOW[u]:
            scc = [u]
            v = STACK.pop()
            while v is not u:
                scc.append(v)
                v = STACK.pop()
            SCCs.append(scc)
            
    ## --------- End of tarjan(u) --------- ##
    
    ## initialization
    DFN = {u: 0 for u in V}
    LOW = {u: 0 for u in V}
    STACK = []
    VISITED = {u: False for u in V}
    TIME = 0
    SCCs = []

    for u in V:
        if not VISITED[u]:
            tarjan(u)
    
    return SCCs


def TWO_SAT(clauses):
    """
    Solve the 2-SAT problem with Tarjan algorithm. MUCH FASTER THAN Papadimitriou's 2-SAT algorithm.

    Params:
        clauses: a list of clauses, note that the number of clauses equals to the number of variables.
    
    Return:
        ret: whether there exists a state that satisfies all the clauses.
    """

    ## build a graph with clauses
    n = len(clauses)
    ## initialize 2 states for each node
    dV = {i: Node(i) for i in range(1, 2*n+1)}
    E = {u: [] for u in dV.values()}
    for clause in clauses:
        id1, sign1 = clause.id1, clause.sign1
        id2, sign2 = clause.id2, clause.sign2

        node11, node12 = conNode(id1)
        node21, node22 = conNode(id2)

        E1, E2 = conEdge(id1, sign1, id2, sign2, dV)
        E[E1.node1].append(E1)
        E[E2.node1].append(E2)
    V = list(dV.values())
    
    SCCs = Tarjan(V, E)
    IDS = [list(map(lambda x: x.parent(), scc)) for scc in SCCs]
    for ids in IDS:
        if len(set(ids)) < len(ids):
            return False
    return True
    
    
if __name__ == "__main__":
    for i in range(1, 7):
        clauses = read_txt(f"2sat{i}.txt")
        ret = TWO_SAT(clauses)
        print(f"2sat{i}.txt => {ret}")
    
    ## outputs: 2sat1 => True
    ##          2sat2 => False
    ##          2sat3 => True
    ##          2sat4 => True
    ##          2sat5 => False
    ##          2sat6 => False
    ## TWO_SAT() takes 10~20 s for each case while Papadimitriou() may take hours.
    