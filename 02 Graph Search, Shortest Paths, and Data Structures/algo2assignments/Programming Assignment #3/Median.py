def read_txt(path):
    array = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            array.append(int(line.rstrip()))
    return array

class Heap:
    """
    A base heap data structure.
    """
    def __init__(self):
        self.data = []
    
    def insert(self, x):
        """
        Insert object x to the heap.
        """

        self.data.append(x)

        if len(self) > 1:
            idx = len(self) - 1
            p = self._parent(idx)
            while self.cmp(self.data[idx], self.data[p]) and p != idx:
                self.data[idx], self.data[p] = self.data[p], self.data[idx]
                idx = p
                p = self._parent(idx)
    
    def top(self):
        """
        Return the object at the top of the heap.
        """

        assert len(self) > 0

        return self.data[0]
    
    def extract(self):
        """
        Extract the object at the top of the heap and maintain the heap properties.
        """

        assert len(self) > 0

        re = self.data[0]
        ## Move the last leaf to the root.
        self.data = [self.data[-1]] + self.data[1:-1]
        idx = 0
        while not self.isLeaf(idx):
            left, right = self._children(idx)
            ## If the left and right indices are both valid, then choose one from them.
            if right < len(self):
                if self.cmp(self.data[left], self.data[right]):
                     child = left
                else:
                    child = right
            ## Only the left index is valid, then choose the left one.
            else:
                child = left
            
            if self.cmp(self.data[child], self.data[idx]):
                self.data[idx], self.data[child] = self.data[child], self.data[idx]
                idx = child
            else:
                break

        return re
    
    def __len__(self):
        return len(self.data)
    
    def isEmpty(self):
        return len(self) == 0
    
    def cmp(self, a, b):
        """
        A comparision function to be implemented by subclass.
        """

        return True
    
    def isLeaf(self, idx):
        """
        A helper function to find whether the idx noede is a leaf node.
        """
        left, right = self._children(idx)
        return (left > len(self)-1) and (right > len(self)-1)
    
    def _parent(self, idx):
        """
        A helper function to return the parent index of the given idx.
        """

        assert idx >= 0 and idx < len(self)
        if idx == 0:
            return idx
        elif idx % 2 == 0:
            return idx // 2 - 1
        else:
            return idx // 2
    
    def _children(self, idx):
        """
        A helper function to return the left and right children of the given idx.
        """

        assert idx >= 0 and idx < len(self)
        left, right = 2*idx+1, 2*idx+2
        return left, right


class MinHeap(Heap):
    def cmp(self, a, b):
        return a < b

class MaxHeap(Heap):
    def cmp(self, a, b):
        return a > b


class MedianMaintainer:
    def __init__(self):
        self.low = MaxHeap()
        self.high = MinHeap()
    
    def add_number(self, x):
        """
        Add a number to the heaps.
        """

        if len(self.low) == 0 and len(self.high) == 0:
            self.low.insert(x)
        else:
            if x < self.low.top():
                self.low.insert(x)
            else:
                self.high.insert(x)
            
            ## Check if the two heaps are balanced
            if len(self.low) - len(self.high) > 1:
                self.high.insert(self.low.extract())
            elif len(self.high) - len(self.low)> 1:
                self.low.insert(self.high.extract())
    
    def median(self):
        """
        Return the median of the numbers.
        """
        if len(self.low) == len(self.high):
            return self.low.top()
        elif len(self.low) > len(self.high):
            return self.low.top()
        elif len(self.low) < len(self.high):
            return self.high.top()

if __name__ == "__main__":
    array = read_txt("Median.txt")
    maintainer = MedianMaintainer()
    medians = []

    for num in array:
        maintainer.add_number(num)
        medians.append(maintainer.median())
    
    print(sum(medians) % 10000)
    # outputs: 1213