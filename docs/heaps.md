---
layout: default
title: My LeetCode Journey
tagline: Lessons learned from grinding LeetCode problems
---
# Heaps

## Basics

The basic usecase for heaps is when we want to track `k` largest or smallest elements in some array. The problem [Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) is a good example. A heap data structure grants easy access to the maximum or minimum element contained inside the heap (`O(1)`), while having `O(log(n))` time complexity for adding an element to the heap and removing the maximum or minimum element from the heap. So in this example problem, we first initialize an empty min heap (heap that tracks the minimum element). As we read in a new element from the stream, we first "push" the element into the heap, and then if the size of the heap is larger than `k`, then we "pop" the minimum element. At any time in the stream, the minimum element in the heap is the kth largest element in the stream so far. Here's a code snippet:
```python
import heapq

def print_kth_largest(stream, k):
    k_largest = []
    heapq.heapify(k_largest)
    for num in stream:
        heapq.heappush(num, k_largest)
        if len(k_largest) > k:
            heapq.heappop(k_largest)
        print(k_largest[0])
```

## Event Stream



[Back to Home](index.html)