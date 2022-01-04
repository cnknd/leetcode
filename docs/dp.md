---
layout: default
title: My LeetCode Journey
tagline: Lessons learned from grinding LeetCode problems
---
# Dynamic Programming

## Introduction
Dynamic programming refers to recursive algorithms where the recursion tree is recombining: i.e. you can reach an interior or leaf node via multiple paths, so it can have multiple parents. The basic example is to find the nth element in the Fibonacci sequence: `fib(n) = fib(n-1) + fib(n-2)`.

If we naively write a recursive function to compute this, we quickly find that the runtime becomes exponential (not to mention that it's very easy to hit the recursion stack limit):
```python
def fib(n):
    if n <= 1:
        return 1
    return fib(n-1) + fib(n-2)
```

Why does this happen? Well, when we compute `fib(5)`, we make a call to `fib(4)` and a call to `fib(3)`, and in each of these two calls there will be a call to `fib(2)`, so already we're calculating `fib(2)` twice. To save time, we can cache results of previously seen calls to `fib`. This method is called "memoization":
```python
def fib(n, memo={}):
    if n <= 1:
        return 1
    if n in memo:
        return memo[n]
    else:
        res = fib(n-1) + fib(n-2)
        memo[n] = res
        return res
```

By introducing this "memo" object (`O(n)` space complexity), we've reduced the runtime (I'll get into what it is in the subsequent section). However, we still have the issue of recursion stack limit. If we think of the recursive calls as performing DFS on the recursion tree, the maximum number of recursive calls we put on the stack is just the height of the tree, and in this case it will be `O(n)`. To get around this, we have to do away with recursion and build the solution iteratively in a bottom-up manner. We initialize an array of size `n` and save previous results into the array:
```python
def fib(n):
    if n <= 1:
        return 1
    res = [0 for _ in range(n+1)]
    res[0] = 1
    res[1] = 1
    for i in range(2, n+1):
        res[i] = res[i-1] + res[i-2]
    return res[-1]
```

Now it's very easy to see that the time complexity is `O(n)` (there are only `n` interations of the for-loop, and each iteration consists of two array lookups). The space complexity is still `O(n)`, but we can do even better! Notice that in the original recurrence relation `fib(n) = fib(n-1) + fib(n-2)`, `fib(n)` does not depend on any `fib(i)` where `i < n-2`. So in reality instead of keeping a size `n` array to store the intermediate results, we only need two numbers to store the last two results:
```python
def fib(n):
    if n <= 1:
        return 1
    prev1, prev2 = 1, 1
    for i in range(2, n+1):
        prev1, prev2 = prev1 + prev2, prev1
    return prev1
```


Find out more by [visiting my GitHub project]({{ site.github.repo }}).

[Back to Home](index.html)