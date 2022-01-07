---
layout: default
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

Oftentimes a problem can be viewed as an event stream, where "events" occur at certain times (there may be an end time for each event, and some other parameter associated with the event), and at any point in time, we need to keep track of all the "active" events (start time <= current time, and if there is an end time, end time > current time) and be able to quickly find the one active event that maximizes or minimizes some parameter. Since we are constantly querying for a min or max element, we can use a heap to store all active events: simply iterate through events and push them onto the heap. At each iteration, if we need to query for the min or max of an active event, we look at the min or max element in the heap (if there is an end time associated with each event, we pop from the heap until the top element has an end time > current time). Here is the rough sketch of the code:
```python
import heapq

def print_largest_val(events)
    """I'm assuming events are in the form of (start, end, val), where val is the parameter
    that we want to maximize or minimize among active events at any time
    """
    events.sort(key=lambda x: x[0])
    active_events = []
    heapq.heapify(active_events)
    for start, end, val in event:
        # push new event onto heap
        heapq.heappush(active_events, (val, end))

        # if the top element in the heap is no longer active
        # we simply remove it; there may still be other
        # inactive events elsewhere down in the heap, but
        # we don't care in the current iteration as long as
        # the top element is active.
        while active_events[0][1] <= start:
            heapq.heappop(active_events)

        # process the top element from amongst the active events
        # in this template I'm just printing the value
        print(active_events[0][0])
```

It's straightforward to modify the above template to suit the given problem. Here are a few examples:
* [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/): here we only need to store the end time of each event as the key in the heap, and we query the size of the heap at each iteration after popping off inactive meeting events.
* [Single Threaded CPU](https://leetcode.com/problems/single-threaded-cpu/): here we're no longer simply iterating through start times; instead we need a `current_time` value that is either incremented by the duration of the current task or moved to the start of the next available task. We store duration and index of each event as the key in the heap.
* [Furthest Building You Can Reach](https://leetcode.com/problems/furthest-building-you-can-reach/): events are just building numbers; we start by using only ladders, but keep the climbs in a heap keyed by the height of each climb. When we run out of ladders, we greedily replace the shortest climb in the heap with bricks and use the freed up ladder for the next building. We do this until we also run out of bricks.

## LeetCode HARD
Problem: [The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/)

The most important step in tackling this problem is understanding what it's asking for. We want, at each point on the x-axis where there is a potential change in building height, to find and record the height of the tallest building at that point (if there is no building at that point, then we need to record a zero). Note that a potential height change (event) occurs at each left AND right endpoint. At each event point, we move buildings from the list of all buildings into the heap based on left endpoint, and then we remove buildings from the heap based on right endpoint. However, since we only care about maximum height, we don't need to remove buildings that have gone past BUT are not at the top of the heap. Here is a rough draft of the code where I just print the max height and ignore the case where there are no buildings at a given event point.

```python
import heapq

def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        buildings.sort(key=lambda x: x[0])
        
        # identify events
        events = []
        for building in buildings:
            events.append(building[0])
            events.append(building[1])
        events.sort()

        # make active events heap
        current_buildings = []
        heapq.heapify(current_buildings)

        # iterate through events
        for x in events:
            # remove from original list of buildings
            while len(buildings) and buildings[0][0] <= x:
                left, right, height = buildings.pop(0)
                tmp = (-height, right)
                heapq.heappush(current_buildings, tmp)
            # remove buildings that are no longer present
            # (inactive events) from top of heap
            while current_buildings[0][1] <= x:
                _ = heapq.heappop(current_buildings)
            # print height
            print(-current_buildings[0][0])
```
[Here]({{ site.github.repo }}/blob/main/solutions/218_SkylineProblem.py) is my full solution.