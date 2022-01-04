---
layout: default
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

## Other Examples
* [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/): the recurrence relation is `minPathSum((i,j)) = min(minPathSum((i-1,j)), minPathSum((i,j-1))) + grid[i][j]`. The result of the same subproblem `minPathSum((i, j))` can be used to solve multiple larger subproblems `minPathSum((i+1, j))` and `minPathSum((i, j+1))`. Since the results for one row (or column) is only used in computing the results for the subsequent row, we only need to keep one row of intermediate results in memory in the iterative bottom-up approach.
* [Decode Ways](https://leetcode.com/problems/decode-ways/): we use `i` to index into the string, and the recurrence relation is `numDecodings(i) = numDecodings(i+1) + int(int(s[i:i+2]) <= 26) * numDecodings(i+2)`. Since this problem is one dimensional and we only use the results from `i+1` and `i+2` to calculate the result for `i`, we only need to store two previous results in the iterative bottom-up approach.

## LeetCode HARD
Problem: [Edit Distance](https://leetcode.com/problems/edit-distance/)

This is actually a fairly straightforward example of DP. There are only two dimensions to consider (conceptually just a bit more difficult than the 1-D Fibonacci sequence example), one for each of the words. So we use `i` and `j` to index into the words. Let's see what the recurrence relation looks like:
at any point `(i, j)`, we have three choices: remove `word1[i]`, insert `word2[j]` into `i`th position in `word1`, or replace `word1[i]` with `word2[j]` (in this case if `word1[i]` is the same as `word2[j]`, we simply don't count the replacement as an edit). Here is a rough draft of the code (I've implemented basic recursion without memoization, and I've left out the terminal conditions for brevity):

```python
def editDistance(i, j, word1, word2):
    a = editDistance(i+1, j, word1, word2) + 1
    b = editDistance(i, j+1, word1, word2) + 1
    c = editDistance(i+1, j+1, word1, word2) + 1
    if word1[i] == word2[j]:
        c -= 1
    return min(a, b, c)
```

Of course to get the speed up from DP, we'll need to either add memoization to the above recursion or implement bottom-up approach. In either case, both the time and space complexities are `O(M*N)` where `M` and `N` are the lengths of `word1` and `word2`, respectively. You can look at my full solution [here]({{ site.github.repo }}/blob/main/solutions/72_EditDistance.py)

This problem actually has a real world application in DNA sequence alignment, where we need to compute the smallest edit distance between two segments of DNA.

## Other applications

* [0-1 Knapsack Problem](https://en.wikipedia.org/wiki/Knapsack_problem)
* [Bellman-Ford Single Source Shortest Paths Algorithm](https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm)
* [Floyd-Warshall All Pairs Shortest Paths Algorithm](https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm)
