import heapq

def read_txt(path):
    nodes = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for sym, line in enumerate(lines[1:]):
            weight = int(line.rstrip())
            node = Node([sym], weight)
            nodes.append(node)
    return nodes

class Node:
    __slots__ = "_symbol", "_weight", "_left", "_right", "_parent"

    def __init__(self, symbol, weight, left=None, right=None, parent=None):
        self._symbol = symbol
        self._weight = weight
        self._left = left
        self._right = right
        self._parent = parent
    
    def isLeaf(self):
        if self._left == None and self._right == None:
            return True
        return False
    
    def __lt__(self, other):
        return self._weight < other._weight
    
    def __gt__(self, other):
        return self._weight > other._weight
    
    def __str__(self):
        return "Symbol: {}, Weight: {}".format(self._symbol, self._weight)
    
    def __len__(self):
        return len(self._symbol)

class HuffmanTree:
    
    def build(self, nodes):
        """
        Build a Huffman Tree with given nodes.
        """

        heapq.heapify(nodes)

        while len(nodes) > 1:
            left = heapq.heappop(nodes)
            right = heapq.heappop(nodes)

            node = self._merge(left, right)
            heapq.heappush(nodes, node)

        self.root = node

    def _merge(self, left, right):
        """
        Merge the given two nodes and return a new one.
        """

        symbol = left._symbol + right._symbol
        weight = left._weight + right._weight
        node = Node(symbol, weight, left, right)

        ## Add parent to left and right nodes
        left._parent = node
        right._parent = node

        return node
    
    def _depth(self, node):
        """
        Return the depth of a given node.
        """

        if node.isLeaf():
            return 0
        else:
            left__depth = self._depth(node._left)
            right_depth = self._depth(node._right)

            return max(left__depth, right_depth) + 1
    
    def _shortest(self, node):
        """
        Return the minimum length of a node.
        """

        if node.isLeaf():
            return 0
        else:
            left__depth = self._shortest(node._left)
            right_depth = self._shortest(node._right)

            return min(left__depth, right_depth) + 1

if __name__ == "__main__":
    nodes = read_txt("huffman.txt")
    tree = HuffmanTree()
    tree.build(nodes)
    root = tree.root
    print("maximum length: {}".format(tree._depth(root)))
    print("minimum length: {}".format(tree._shortest(root)))
    # outputs: maximum length: 19
    #          minimum length: 9