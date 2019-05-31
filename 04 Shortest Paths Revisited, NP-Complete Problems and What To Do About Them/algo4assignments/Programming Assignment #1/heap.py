class Empty(Exception):
    pass

class AdaptablePriorityQueue:
    """
    A queue based priority queue implemented with Python. This priority queue provides update and remove methods 
    to modify existing elements in queue.

    More details can be seen in Data Structures & Algorithms in Python, Chapter 9 Priority queues, by Goodrich, Michael T., etc.
    """

    class Locator:
        __slots__ = "_key", "_value", "_index"

        def __init__(self, k, v, j):
            self._key = k
            self._value = v
            self._index = j
        
        def __lt__(self, other):
            return self._key < other._key

    def __init__(self):
        self._data = []
    
    def __len__(self):
        return len(self._data)
    
    ## --------------- Public Behaviors --------------- ##
    
    def is_empty(self):
        return len(self) == 0
    
    def push(self, k, v):
        """
        Add a new (k, v) pair into the heap.
        """

        token = self.Locator(k, v, len(self))
        self._data.append(token)
        self._upheap(len(self) - 1)
        return token
    
    def min(self):
        """
        Return but not remove the (k, v) pair on the top of the queue.
        """

        if self.is_empty():
            raise Empty("Priority queue is empty.")
        loc = self._data[0]
        return loc._key, loc._value

    def pop(self):
        """
        Return and remove the (k, v) pair on the top of the queue.
        """

        if self.is_empty():
            raise Empty("Priority queue is empty.")
        self._swap(0, len(self)-1)
        loc = self._data.pop()
        self._downheap(0)
        return loc._key, loc._value
    
    def update(self, loc, newkey, newvalue):
        """
        Update the key, value pair for the entity identified by loc.
        """

        j = loc._index
        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError("Invalid locator")
        loc._key = newkey
        loc._value = newvalue
        self._bubble(j)
    
    def remove(self, loc):
        """
        Remove and return the (k, v) pair identified by loc.
        """

        j = loc._index
        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError("Invalid locator")
        if j == len(self) - 1:
            self._data.pop()
        else:
            self._swap(j, len(self)-1)
            self._data.pop()
            self._bubble(j)
        return loc._key, loc._value
    
    ## --------------- Non-public Behaviors --------------- ##
    def _parent(self, j):
        """
        Return the parent child index of j.
        """

        return (j-1) // 2
    
    def _left(self, j):
        """
        Return the left child index of j.
        """

        return j*2 + 1
    
    def _right(self, j):
        """
        Return the right child index of j.
        """

        return j*2 + 2
    
    def _has_left(self, j):
        """
        Return whether index j has a left child.
        """

        return self._left(j) < len(self)
    
    def _has_right(self, j):
        """
        Return whether index j has a right child.
        """

        return self._right(j) < len(self)
    
    def _swap(self, i, j):
        """
        Just swap the index i and j.
        """

        self._data[i], self._data[j] = self._data[j], self._data[i]
        ## Reset locator indices
        self._data[i]._index = i
        self._data[j]._index = j
    
    def _bubble(self, j):
        """
        Sift up or sift down from index j.
        """

        if j > 0 and self._data[j] < self._data[self._parent(j)]:
            self._upheap(j)
        else:
            self._downheap(j)
    
    def _upheap(self, j):
        """
        Sift up from index j.
        """

        parent = self._parent(j)
        if j > 0 and self._data[j] < self._data[parent]:
            self._swap(j, parent)
            ## Recursively sift up from index parent
            self._upheap(parent)
    
    def _downheap(self, j):
        """
        Sift down from index j.
        """

        if self._has_left(j):
            left = self._left(j)
            child = left

            if self._has_right(j):
                right = self._right(j)

                if self._data[right] < self._data[left]:
                    child = right
            
            if self._data[child] < self._data[j]:
                self._swap(child, j)
                ## Recursively sift down from index child
                self._downheap(child)