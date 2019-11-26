""" Heap algorithms for implementing a min-heap and using it as a min-priority queue """


class MinHeap:
    """ Class containing methods to be used on a min-heap """
    
    def __init__(self, A):
        """ Inializes and builds a min-heap from input array A (which should contain comparable objects) """
        # array representing the heap
        self.array = list(A)
        self.build_min_heap()
    
    def size(self):
        """ Returns size of the heap """
        return len(self.array)

    def __iter__(self):
        """ Makes the heap iterable """
        return self.array.__iter__()
    
    def parent(self, i):
        """ Returns index of parent in a heap """
        return int(i/2)

    def left(self, i):
        """ Returns index of left child in a heap """
        # adding an additional 1 because of 0-indexing
        return (2 * i + 1)

    def right(self, i):
        """ Returns index of right child in a heap """
        # adding an additional 1 because of 0-indexing
        return (2 * i + 1) + 1

    def min_heapify(self, parent_index):
        """ Recursively heapify parent and its children """
        l_index = self.left(parent_index)
        r_index = self.right(parent_index)

        # if left child exists and left child is larger than parent
        if l_index < len(self.array) and self.array[l_index] < self.array[parent_index]:
            largest_index = l_index
        else:
            largest_index = parent_index
        
        # if right child exists and right child is larger than max(parent, left)
        if r_index < len(self.array) and self.array[r_index] < self.array[largest_index]:
            largest_index = r_index
        
        # heapify parent and children by swapping places (indexes) if the parent is not largest
        if largest_index != parent_index:
            self.array[parent_index], self.array[largest_index] = self.array[largest_index], self.array[parent_index]
            self.min_heapify(largest_index)

    def build_min_heap(self):
        """ Builds a min heap from self.array """
        for i in range(int(len(self.array)/2), -1, -1):
            self.min_heapify(i)

    def minimum(self):
        """ Returns the minimum value of a heap A """
        return self.array[0]

    def extract_min(self):
        """ Returns the minimal value of A and re-heapifies the heap """
        if len(self.array) < 1:
            raise ValueError("A is empty")
        min_result = self.array[0]
        self.array[0] = self.array[-1]
        self.array.pop()
        self.min_heapify(0)
        return min_result

    def decrease_key(self, i, key):
        """ Decrases key of an index and makes sure its still at the right place in the heap """
        if key > self.array[i]:
            raise ValueError("New key is larger than current key")
        self.array[i] = key
        while i > 1 and self.array[parent(i)] > self.array[i]:
            self.array[i], self.array[parent(i)] = self.array[parent(i)], self.array[i]
            i = parent(i)
    
    def print(self):
        print(self.array)


def test(): 
    a = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]

    print(a)

    heap = MinHeap(a)
    print(heap.extract_min())
    heap.print()
    print(heap.extract_min())
    heap.print()
    print(heap.extract_min())
    heap.print()

# test()
