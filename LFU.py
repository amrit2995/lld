import heapq
from collections import Counter
class LFU:
    def __init__(self, capacity):
        self.heap = []
        self.freq = {}
        self.capacity = capacity
        self.len = 0
        heapq.heapify(self.heap)

    def create_heap(self):
        self.heap = []
        self.heap = [(val, key) for key, val in self.freq.items()]
        heapq.heapify(self.heap)

    def get(self, val):
        if val not in self.heap.keys():
            print("Value not available")
            return 
        self.freq[val] += 1

    def push(self, val):
        if val not in self.freq.keys():
            self.freq[val] = 1
        else:
            self.freq[val] += 1

        if val in self.freq.keys():
            self.get(val)

        if self.len >= self.capacity:
            self.create_heap()
            heapq.heappop(self.heap)
        heapq.heappush((self.freq[val], val))


lfu = LFU(5)
