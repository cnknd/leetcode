# problem: https://leetcode.com/problems/lru-cache/

# LRU (least recently used) is a very popular cache eviction policy. The idea is very simple,
# when the cache is full, we evict the oldest key (and its associated value). Every time
# there is a cache hit, the queried key becomes newly queried (moved into the front of the
# cache), and so we always evict from the back end of the cache.
# This description lends itself to an array implementation, except there are some downsides:
#    1. lookup by key is slow in an array
#    2. moving an element to one end of the array (on cache hit) requires reshuffling many
#       other elements, and this becomes an O(n) operation
# We can solve 2 with a linked list implementation. Specifically we want a doubly linked
# list to support removing a node from inside (simply link the parent to the child of the
# node we want to remove).
# We can solve 1 with an additional hashmap, where the values are pointers to the nodes
# in the doubly linked list.
# Finally, in this implementation below, I've created two dummy nodes at the head and
# tail of the doubly linked list to make the code a bit cleaner (no need for special
# cases to handle adding or removing from either end of the list)

class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.nodes_dict = {}
        self.remaining_capacity = capacity

    def _push(self, new_node):
        prev = self.tail.prev
        prev.next = new_node
        new_node.prev = prev
        new_node.next = self.tail
        self.tail.prev = new_node

    def _pop(self):
        first = self.head.next
        if first is self.tail:
            return
        second = first.next
        self.head.next = second
        second.prev = self.head
        first.prev = None
        first.next = None
        return first

    def _remove(self, node):
        if node is self.head or node is self.tail:
            return
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        node.prev = None
        node.next = None
        return node

    def get(self, key: int) -> int:
        if key in self.nodes_dict:
            node = self._remove(self.nodes_dict[key])
            self._push(node)
            return node.value
        else:
            return -1

    def put(self, key: int, value: int) -> None:
        if key in self.nodes_dict:
            node = self.nodes_dict[key]
            node = self._remove(node)
            node.value = value
            self._push(node)
        else:
            new_node = Node(key, value)
            self.nodes_dict[key] = new_node
            self._push(new_node)
            if self.remaining_capacity > 0:
                self.remaining_capacity -= 1
            else:
                evicted = self._pop()
                if evicted:
                    del self.nodes_dict[evicted.key]

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
