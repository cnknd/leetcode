# problem: https://leetcode.com/problems/decode-ways/

# The problem asks for how many ways we can decode s (call this f(0)). This boils
# down to two subproblems:
#   f(1) = how many ways can we decode s[1:]
#   f(2) = how many ways can we decode s[2:]
# And we have the recurrence: f(0) = f(1) + i * f(2), where i is the indicator of
# whether or not we can decode a single letter from s[:2] (i.e. s[:2] <= '26')
# Note that there is an edgecase: if s[0] == '0', then f(0) = 0.
# 
# This is a typical Dynamic Programming problem, and in general, we can solve
# DP problems in two different ways: top-down recursion, and bottom-up approach
# 
# In the top-down approach, we directly code the recurrence above as a recursive
# function. However, sometimes we may be solving the same subproblem over and
# over again. For example, if s = '1111', then f(0) = f(1) + f(2) = (f(2) + f(3)) +
# (f(3) + f(4)) = ..., and already we have two calls to f(3). As the size of the
# string grows, the amount of duplicate work we're doing grows exponentially,
# so it really helps to cache the results of subproblems we've already done
# and pass the cache through the recursion (think of recursion as DFS through a
# recombining tree, but now we want to keep track of visited nodes in the tree to
# save time). This top down with caching is called memoization. Once we do this
# we reduce the time complexity from exponential to polynomial (for this problem,
# the time complexity is linear, as we're only evaluating (f(i) once for each i).
# 
# In the bottom up approach, we start with f(n) and f(n-1) and build toward f(0).
# This way we don't have to write a recursive function. We can simply iterate
# through an index i from n to 0, and we save previous results along in an array
# of size n+1 (base case is empty string, which has 1 way to decode into an empty
# string). Now it's even more clear that the time complexity is linear.
# Space complexity is also linear as we're saving the entire array of results for
# previous subproblems. However, we can go one step further and improve the
# space complexity to constant. Note that f(i) only depends on f(i+1) and f(i+2)
# and we actually don't need f(i+3) when we reach f(i). We can simply discard
# old results that we no longer need to get to constant space complexity.


class Solution1:
    """naive recursion, exponential runtime
    """
    def numDecodings(self, s: str) -> int:
        if len(s) == 0:
            return 1
        elif s[0] == '0':
            return 0
        else:
            a = self.numDecodings(s[1:])
            b = len(s) >= 2 and s[:2] <= '26' and self.numDecodings(s[2:])
            return a + b


class Solution2:
    """recursion with memoization
    """
    def numDecodings(self, s: str) -> int:
        def dp(i, memo={}):
            if i == len(s):
                out = 1
            elif s[i] == '0':
                out = 0
            else:
                a = dp(i+1)
                b = i <= len(s)-2 and s[i:i+2] <= '26' and dp(i+2)
                out = a + b
            memo[i] = out
            return out
        return dp(0, {})


class Solution3:
    """bottom up
    """
    def numDecodings(self, s: str) -> int:
        out = [0] * (len(s)+1)
        out[-1] = 1
        for i in range(len(s)-1, -1, -1):
            if s[i] == '0':
                out[i] = 0
            else:
                a = out[i+1]
                b = i <= len(s)-2 and s[i:i+2] <= '26' and out[i+2]
                out[i] = a + b
        return out[0]


class Solution4:
    """bottom up with optimization for space
    """
    def numDecodings(self, s: str) -> int:
        n1, n2 = int(s[-1] != '0'), 1
        for i in range(len(s)-2, -1, -1):
            if s[i] == '0':
                n = 0
            else:
                n = n1 + (s[i:i+2] <= '26' and n2)
            n1, n2 = n, n1
        return n1