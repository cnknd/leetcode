# problem: https://leetcode.com/problems/count-of-smaller-numbers-after-self/

# naive solution: brute force is O(n^2), where for each element in the given
#    array, we scan the rest of the array and track a counter of number of
#    smaller elements. Obviously the question is looking for a faster solution.

# first solution: the strategy here is the instantiate a counter array of
#    the same size as the original array, then we start counting the numbers
#    in the original array in ascending order. Every time we count a new
#    number (may be duplicated), we first find the sum to the right of each
#    index of that number and save it to the output. Then we set the counter
#    to 1 at each index of that number. Now this might seem like O(n^2) again,
#    but there is a data structure that allows us to do range queries (e.g.
#    sum of array elements from index i to index j) in log(n) time that also
#    supports updating array values in log(n) time as well. That is a Segment
#    Tree. See this: https://www.youtube.com/watch?v=Tr-xEGoByFQ for a very
#    good explanation of what segment trees are.

# alternative: notice that the "smaller than" and "to the right of" are sort
#    of interchangeable. Specifically, for every index in the array, we're
#    looking for numbers "smaller than" that value and has an index "larger
#    than" that index. So we can interchange these two to create an alternate
#    solution. Our segment tree will be based on an array of all possible
#    distinct values in nums (initialized to zeros), and indicates simply
#    the count of each value that we've seen so far, as we traverse right to
#    left in the original array. The range query for the segment tree will
#    be the sum from index 0 up to and excluding the index of current number
#    we're looking at. After the range query we increment the counter at
#    that index in the segment tree by 1.

# notes: In the first solution, we do sort nums by value and associate with each
#    value all the indices that value appeared at in the original array.
#    There are two ways to do this, one is store num: indices in a hashmap.
#    The other is to leverage the fact that nums are integers in a given range
#    and use bucket sort. However, the two methods have the same time complexity
#    as the segment tree operations are still O(nlogn).
#    We would prefer the second method if the range of numbers is smaller than
#    the size of the array. If the range of numbers is size m, then the second
#    method would have O(nlogm) time complexity as the segment tree is based on
#    the range of numbers.


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

    def increment(self, i: int):
        """
        increment counter in array by 1 at position i
        we do this by finding the leaf node for position i
        and increment the value there by 1.
        then we backtrack up the tree and increment parent
        nodes by 1 as well
        """
        self._increment(1, i)

    def _increment(self, tree_idx: int, i: int):
        left, right, val = self.tree[tree_idx]
        if i < left or i > right:
            return
        else:
            self.tree[tree_idx][2] += 1
            if left < right:
                self._increment(tree_idx*2, i)
                self._increment(tree_idx*2+1, i)

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
            return left_val + right_val


class Solution1a:
    """segment tree range based on indices in the original array;
    store values from the original array and their indices in hashmap
    and do comparison sort to iterate through the values in increasing
    order;
    """
    def countSmaller(self, nums: List[int]) -> List[int]:
        nums_dict = {}
        for i, n in enumerate(nums):
            if n in nums_dict:
                nums_dict[n].append(i)
            else:
                nums_dict[n] = [i]
        
        seg_tree = SegTree(len(nums))
        out = [0] * len(nums)
        for n in sorted(nums_dict.keys()):
            for idx in nums_dict[n]:
                out[idx] = seg_tree.query(idx+1, len(nums)-1)
            for idx in nums_dict[n]:
                seg_tree.increment(idx)
        return out


class Solution1b:
    """segment tree range based on indices in the original array;
    store values from the original array and their indices in buckets
    so the values are already bucket sorted after reading once;
    """
    def countSmaller(self, nums: List[int]) -> List[int]:
        MAX_VAL = 10**4
        nums_buckets = [[] for _ in range(2 * MAX_VAL+1)]
        for i, n in enumerate(nums):
            bucket_loc = n + MAX_VAL
            nums_buckets[bucket_loc].append(i)

        seg_tree = SegTree(len(nums))
        out = [0] * len(nums)
        for loc in range(2 * MAX_VAL+1):
            for idx in nums_buckets[loc]:
                out[idx] = seg_tree.query(idx+1, len(nums)-1)
            for idx in nums_buckets[loc]:
                seg_tree.increment(idx)
        return out


class Solution2:
    """segment tree range based on range of possible values in the
    original array; iterate through the original array backwards
    """
    def countSmaller(self, nums: List[int]) -> List[int]:
        MIN_VAL = min(nums)
        MAX_VAL = max(nums)
        seg_tree_size = MAX_VAL - MIN_VAL + 1

        seg_tree = SegTree(seg_tree_size)
        out = []
        for num in nums[::-1]:
            num_loc = num - MIN_VAL
            out.append(seg_tree.query(0, num_loc-1))
            seg_tree.increment(num_loc)
        return out[::-1]


# There is another data structure with same time complexity but better constants.
# This is the Fenwick Tree (aka Binary Indexed Tree). Again the AlgorithmsLive
# youtube channel has an excellent explanation: 
# https://www.youtube.com/watch?v=kPaJfAUwViY
# The code for the Solution class is almost the same as above, except the segment
# tree is replaced with a Fenwick tree (and the interface is slightly different,
# as Fenwick tree naturally does prefix sums, and we don't have to specify the
# left end of the range with index 0)

def get_lsd(n):
    """taken from stackoverflow
    https://stackoverflow.com/questions/5520655/return-index-of-least-significant-bit-in-python
    """
    return (n&-n).bit_length()-1


def get_next_lower(n):
    return n - (1 << get_lsd(n))


def get_next_higher(n):
    return n + (1 << get_lsd(n))


class FenwickTree:
    def __init__(self, length):
        self.tree = [0] * length
    
    def add_val(self, i, val):
        idx = i+1
        while idx <= len(self.tree):
            self.tree[idx-1] += val
            idx = get_next_higher(idx)
        
    def rangesum(self, i, j):
        return self.cumsum(j) - self.cumsum(i)

    def cumsum(self, i):
        out = 0
        while i != 0:
            out += self.tree[i-1]
            i = get_next_lower(i)
        return out


class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        MIN_VAL = min(nums)
        MAX_VAL = max(nums)
        tree_size = MAX_VAL - MIN_VAL + 1

        fenwick_tree = FenwickTree(tree_size)
        out = []
        for num in nums[::-1]:
            num_loc = num - MIN_VAL
            out.append(fenwick_tree.cumsum(num_loc))
            fenwick_tree.add_val(num_loc, 1)
        return out[::-1]
