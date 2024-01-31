class DLL:
    def __init__(self, val=None, prev = None,nxt=None):
        self.val = val
        self.next = nxt
        self.prev = prev
    

class LRU:
    def __init__(self, capacity):
        self.head = None
        self.last = None
        self.capacity = capacity
        self.len = 0
        self.dict = {}

    def get(self, cache_val):
        if cache_val not in self.dict:
            print("Value not present in cache")
        else:
            curr = self.dict.get(cache_val)
            if curr == self.last:
                pass
            elif curr == self.head:
                self.head = self.head.next
                curr.next = None
                curr.prev = self.last
                self.last.next = curr
                self.last = self.last.next
            else:
                before_curr = curr.prev
                after_curr = curr.next
                before_curr.next = after_curr
                after_curr.prev = before_curr
                curr.prev = self.last
                curr.next = None
                self.last.next = curr
                self.last = self.last.next
            self.dict[cache_val] = self.last
            print("Present in cache")


    def put(self, cache_val):
        if cache_val in self.dict.keys():
            self.get(cache_val)
        elif self.len == 0:
            print("first")
            self.head = DLL(cache_val)
            self.last = self.head
            self.len += 1

        elif self.len < self.capacity:
            print("still capacity")
            self.last.next = DLL(val=cache_val, prev=self.last)
            self.last = self.last.next
            self.len += 1
        else:
            print("capacity exceeded")
            self.dict.pop(self.head.val)
            self.head = self.head.next
            self.last.next = DLL(val=cache_val, prev=self.last)
            self.last = self.last.next
            self.dict[self.last.val] = self.last
        self.dict[cache_val] = self.last

    def traverse(self):
        a = []
        curr  = self.head
        while curr:
            a.append(curr.val)
            curr = curr.next
        return a

import pdb;pdb.set_trace()
lru = LRU(4)
lru.put(1)
lru.put(2)
lru.put(3)
lru.put(4)
lru.get(2)
print('end')