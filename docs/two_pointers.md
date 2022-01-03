---
layout: page
title: My LeetCode Journey
tagline: Lessons learned from grinding LeetCode problems
---

## Basics

We start with a warmup: [Two Sum with Sorted Input](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/).
In this problem we can employ a common trick with pointers that we can use to traverse an array to find the answer we're looking for.
The problem gives us a sorted array and asks us to find two elements in the array (can't use the same element twice) that sum to a given target. The answer will be `numbers[i]` and `numbers[j]`, for some `i` and `j` such that `i < j`. Let's try to scan the array for `i` and `j`. Naively for each `i`, we look through all values of `j > i`.  This naive approach runs in quadratic time. It's doing a lot of redundant work since our array is already sorted: if at some point in our search (at `i1`, `j1`), the sum of the two numbers we're looking at is larger than the target, then we don't have to look at `j > j1`, as the answer won't be there. Similarly, if the sum is smaller than the target, then we don't have to look at `i < i1`.
Using these observations, we can start our `i` and `j` pointers at the two ends of the array, and either imcrement `i` or decrement `j` depending on how the current sum compares to the target. This way we only visit each element in the array once, so the improved algorithm runs in linear time.
Here is the code for the solution:

```python
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        i, j = 0, len(numbers)-1
        while i < j:
            tmp_sum = numbers[i] + numbers[j]
            if tmp_sum < target:
                i += 1
            elif tmp_sum > target:
                j -= 1
            else:
                return [i+1, j+1]
```

## More Advanced Examples

* [Container with Most Water](https://leetcode.com/problems/container-with-most-water/)
* [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)

## Uses in Linked Lists

Tricks with pointers show up frequently in linked lists. Examples:
* Reversing a linked list requires 3 pointers: two for the two nodes that we are about to reverse (let's call these `node1` and `node2`), and a third one to hold onto the next node in the list before we execute `node2.next = node1`.
* Finding the middle of a linked list can be done with `slow` and `fast` pointers, where `slow` travels one node at a time and `fast` travels two nodes at a time. When `fast` gets to the end of the list, `slow` should be at the middle
* Finding the kth node from the end of the list can also be done with `slow` and `fast` pointers, but here `fast` simply has a head-start of k nodes.
* There is a [famous algorithm](https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare) for finding cycles in a linked list that uses `slow` and `fast` pointers.


Find out more by [visiting my GitHub project]({{ site.github.repo }}).