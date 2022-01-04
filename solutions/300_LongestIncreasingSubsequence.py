# problem: https://leetcode.com/problems/longest-increasing-subsequence/

# Ideas:
#   Brute Force: brute force solution here is going to have exponential time complexity
#        as we need to check every single subsequence of the array.
#   Dynamic Programming: let LIS(i) = longest increasing subsequence in nums[i:],
#        then we have the following recurrence:
#           LIS(i) = max([LIS(i+1)] + [1 + LIS(j) for j in range(i+1, n) if nums[i] < nums[j]])
#        we can now incrementally build up the longest increasing subsequence by scanning
#        the array from right to left. This method has quadratic time complexity
#   Range Query: let's start with an array representing all possible numbers in nums. i.e. an
#        array of size 2*10^4+1, where the first element represents -10^4 and the last element
#        represents 10^4. Then we fill the array with the longest increasing subsequence of nums
#        ending in that particular number; when we're done, the maximum value in this array is
#        our answer. To fill the array, we iterate through the numbers and do two things at each
#        num:
#         * first get the max LIS before num, call this "v"
#         * then update the array value at num with v + 1
#        For example, let's say our input is [5, 1, 4, 2, 3, 6, 0], the LIS array starts off as
#        [0, 0, 0, 0, 0, 0, 0], and this is how it evolves after each iteration:
#         * num = 5, max(LIS[:5]) = 0 -> LIS = [0, 0, 0, 0, 0, 1, 0]
#         * num = 1, max(LIS[:1]) = 0 -> LIS = [0, 1, 0, 0, 0, 1, 0]
#         * num = 4, max(LIS[:4]) = 1 -> LIS = [0, 1, 0, 0, 2, 1, 0]
#         * num = 2, max(LIS[:2]) = 1 -> LIS = [0, 1, 2, 0, 2, 1, 0]
#         * num = 3, max(LIS[:3]) = 2 -> LIS = [0, 1, 2, 3, 2, 1, 0]
#         * num = 6, max(LIS[:6]) = 3 -> LIS = [0, 1, 2, 3, 2, 1, 4]
#         * num = 0, max(LIS[:0]) = 0 -> LIS = [1, 1, 2, 3, 2, 1, 4]
#        Finally, the output is max(LIS) = 4.
#        Notice that at every iteration, we're doing a range max query and a point update on the
#        array LIS. Simply keeping LIS as an array makes this O(M) time in each iteration (dominated
#        by the range max query. To improve upon this, we can use a Segment Tree or Fenwick Tree
#        to speed up each iteration to O(logM). Here M is the size of the range of possible values
#        in nums. Since len(nums) = N << M, we can improve upon this solution by first performing an
#        O(NlogN) coordinate compression operation nums. So the final time complexity of this
#        algorithm will be O(NlogN)


from typing import List


class SegTree:
    def __init__(self, n: int):
        self.size = n
        # tree is a list of lists
        # inner lists are [low, high, val]
        self.tree = [[]] * (4*n+1)
        self.init_tree(1, 0, n-1)
    
    def init_tree(self, tree_idx: int, i: int, j: int):
        self.tree[tree_idx] = [i, j, 0]
        if j > i:
            mid = i+(j-i)//2
            self.init_tree(tree_idx*2, i, mid)
            self.init_tree(tree_idx*2+1, mid+1, j)

    def update(self, i: int, val: int):
        self._update(1, i, val)

    def _update(self, tree_idx: int, i: int, val: int):
        left, right, node_val = self.tree[tree_idx]
        if i < left or i > right:
            return
        else:
            self.tree[tree_idx][2] = max(node_val, val)
            if left < right:
                self._update(tree_idx*2, i, val)
                self._update(tree_idx*2+1, i, val)

    def query(self, i: int, j: int) -> int:
        return self._query(1, i, j)
    
    def _query(self, tree_idx: int, i: int, j: int) -> int:
        # 3 cases:
        #   1. disjoint: do nothing
        #   2. full cover: increment 
        #   3. partial cover: go down left and right subtrees
        left, right, val = self.tree[tree_idx]
        if j < left or i > right:
            return 0
        elif i <= left and j >= right:
            return val
        else:
            left_val = self._query(tree_idx*2, i, j)
            right_val = self._query(tree_idx*2+1, i, j)
            return max(left_val, right_val)


def coordinate_compression(nums):
    unique = list(set(nums))
    unique.sort()
    mapping = dict([(val, i) for i, val in enumerate(unique)])
    out = [mapping[n] for n in nums]
    return out
        

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        compressed = coordinate_compression(nums)
        tree = SegTree(len(compressed))
        for num in compressed:
            tmp = tree.query(0, num-1)
            tree.update(num, tmp+1)
        return tree.query(0, len(compressed))


# Alternative Solution (Greedy method)
#   As we're iterating through nums, let's say we've kept track of the LIS so far.
#   Now we encounter a new num. If num > LIS[-1] we simply append num to LIS.
#   If num < LIS[-1] but num > LIS[-2], then we can greedily replace LIS[-1] with num.
#   After this replacement operation, as we continue down the list, we're guaranteed to
#   have an LIS at least as long as the LIS we would have achieved without the replacement.
#   Now what if num < LIS[-1] but num < LIS[-2]? Let's first look at the case where
#   num > LIS[-3]. Suppose we replace LIS[-2] with num. This does invalidate LIS as it's
#   no longer in order, but LIS[-1] remains unchanged. If at any point we encounter a new
#   number that is greater than the new LIS[-2] and less than LIS[-1], we can definitely
#   swap it with LIS[-1] and now the new LIS is valid again, we retain the same length,
#   and this new LIS is better than the one we had before (smaller last element).
#   In fact, this logic works with any swap operation nums[j] <-> LIS[i] where LIS[i] is 
#   the first element in LIS that is >= nums[j]. After any such swap operation of
#   nums[j] <-> LIS[i], as we continue to scan the list, one of two things will happen:
#      1. we don't find enought elements in the rest of the list to swap out LIS[i+1:];
#         in this case LIS may not be valid when we reach the end of the list, but its length
#         is the same as the length of a valid LIS
#      2. we do find enough elements in the rest of the list to swap out LIS[i+1:],
#         in this case we do have a valid LIS that is an improved version of the original
#         LIS before the nums[j] <-> LIS[i] swap operation.
#   Now we would also be appending to the tail of the LIS as we scan through the list, but
#   the append operation doesn't change the logic above. And in either case, we're safe
#   to simply make these swap operations and retain a correct LIS length. 
#   A naive approach to doing the swap operation would be to scan through the entire LIS
#   list, which is linear time. But we can improve upon this with binary search since by
#   construction LIS is sorted.

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        lis = []
        for n in nums:
            if len(lis) == 0 or n > lis[-1]:
                lis.append(n)
            else:
                self.findAndSwap(lis, n)
        return len(lis)

    def findAndSwap(self, lis, num):
        i, j = 0, len(lis)-1
        while i < j:
            mid = i + (j-i) // 2
            if lis[mid] >= num:
                j = mid
            else:
                i = mid + 1
        lis[i] = num
