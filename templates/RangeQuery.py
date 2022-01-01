# Some problems boil down to querying something within a range in a
# dynamic array (array gets updated frequently). Fortunately, in a
# lot of these situations the array size remains the same. This type
# of situation calls for some very interesting data structures.
# Naively if we just store the original array and do a range query
# (e.g. range sum: sum(nums[i:j])), then the range query will have
# time complexity O(n), which is not great if we have to do many
# such queries. On the other hand, point updates are O(1), which
# is nice.
# One thing we can do is store the prefix array (like a cumsum):
# prefix_sum[i] = sum(nums[:i]). This way range sum query has time
# complexity O(1) (sum(nums[i:j]) = prefix_sum[j] - prefix_sum[i])
# But this comes at the cost of O(n) for point updates, as updating
# one element in the original array would update all subsequent
# elements in the prefix sum array. Another issue is that this
# doesn't work for range min or max queries.
# We can improve on these naive ideas with some interesting
# data structures. I will implement two below: Segment Tree and
# Fenwick Tree.
# For more information on these, check out the youtube videos
# on the Algorithms Live channel:
# https://www.youtube.com/watch?v=kPaJfAUwViY
# https://www.youtube.com/watch?v=Tr-xEGoByFQ


class RangeQuery:
    def __init__(self, vals):
        self.vals = vals

    def range_query(self, i, j):
        pass

    def point_update(self, i, val):
        self.vals[i] = val

    def range_update(self, i, j, val):
        pass

# Example: queries are for range sum, point updates are add a value
#          to the value at an existing index of the array,
#          range updates are add a value to all existing values
#          between two indices

# Basic implementation: store the original array
# Query time complexity: O(n)
# Point update time complexity: O(1)
class RangeSumAdd(RangeQuery):
    def range_query(self, i, j):
        return sum(self.vals[i:j])

    def point_update(self, i, val):
        self.vals[i] += val

    def range_update(self, i, j, val):
        for k in range(i, j):
            self.vals[k] += val

# Prefix sum implementation
# Query time complexity: O(1)
# Point update time complexity: O(n)
class PrefixSumAdd(RangeQuery):
    def __init__(self, vals):
        self.prefix_sum = []
        current_sum = 0
        for n in vals:
            current_sum += n
            self.prefix_sum.append(current_sum)
    
    def range_query(self, i, j):
        if i == j:
            return 0
        if i == 0:
            return self.prefix_sum[j-1]
        return self.prefix_sum[j-1] - self.prefix_sum[i-1]
    
    def point_update(self, i, val):
        for k in range(i, len(self.prefix_sum)):
            self.prefix_sum[k] += val
    
    def range_update(self, i, j, val):
        for k in range(i, len(self.prefix_sum)):
            mult = (min(k, j-1) - i + 1)
            self.prefix_sum[k] += mult * val


# Segment Tree

class SegmentTree(RangeQuery):
    """segment tree with lazy propagation
    see youtube video for explanation: https://www.youtube.com/watch?v=Tr-xEGoByFQ
    * tree is stored in an array of length 4n+1
    * each node in the tree contains 4 values: low, high, value, delta
    * low and high are endpoints (inclusive) of the node's range
    * value is the current value (prior to evaluating lazy propagation)
    * delta is the amount of change that need to be made from past update
      operations that are held at the current node due to lazy propagation
      
    to implement a custom range query with custom update function, simply
    subclass this class and write the _op, _incr, and _incr_range functions
    """
    def __init__(self, vals):
        n = len(vals)
        self.tree = [[] for _ in range(4*n+1)]
        self._init_node(1, 0, n-1, vals)

    def _init_node(self, tree_idx, low, high, vals):
        if low == high:
            self.tree[tree_idx] = [low, high, vals[low], 0]
            return vals[low]
        else:
            mid = low + (high-low) // 2
            left_val = self._init_node(tree_idx*2, low, mid, vals)
            right_val = self._init_node(tree_idx*2+1, mid+1, high, vals)
            val = self._op(left_val, right_val)
            self.tree[tree_idx] = [low, high, val, 0]
            return val

    def _op(self, a, b):
        """main operation of the range query. e.g. if we query for range sums,
        this function should be +; if we query for range max, this function
        should be max
        """
        pass

    def _incr(self, val, delta):
        """operation of point updates (this is actually used to aggregate
        deltas from all past updates held at a node due to lazy propagation).
        """
        pass
    
    def _incr_range(self, low, high, val, delta):
        """operation of range updates. this is used to update the range query
        value for any node in the tree. so if range query is sum and point
        update function is add, then this operation is add r * delta, where
        r is the size of the range. if range query is max and point update
        function is set, then this operation simply returns delta. if range
        query is sum and point update is set, then this operation returns
        r * delta
        """
        pass

    @property
    def _default(self):
        """identity element for _op
        e.g. if _op is max, then this should be -inf
             if _op is min, then this should be +inf
             if _op is sum, then this should be 0
        """
        pass
    
    def _propagate(self, tree_idx):
        """Helper function to do lazy propagation. This simply pushes
        accumulated increments from current tree node to its two children
        """
        low, high, val, delta = self.tree[tree_idx]
        if low == high:
            return

        self.tree[tree_idx*2][3] = self._incr(self.tree[tree_idx*2][3], delta)
        self.tree[tree_idx*2+1][3] = self._incr(self.tree[tree_idx*2+1][3], delta)
        self.tree[tree_idx][3] = 0
    
    def _update(self, tree_idx):
        """updates the value of a node based on updates to its children;
        this is called alongside _propagate
        """
        low, high, val, delta = self.tree[tree_idx]
        if low == high:
            self.tree[tree_idx][2] = self._incr(val, delta)
            self.tree[tree_idx][3] = 0
            return

        new_val = self._op(self._incr_range(*self.tree[tree_idx*2]),
                           self._incr_range(*self.tree[tree_idx*2+1]))
        self.tree[tree_idx][2] = new_val
    
    def range_query(self, i, j):
        return self._range_query(1, i, j-1)

    def _range_query(self, tree_idx, low, high):
        # 3 cases:
        #   1. full cover, return value
        #   2. disjoint, return some default value (e.g. 0)
        #   3. partial cover, return binary operation applied
        #      to left child and right child; but this is also
        #      when we push down the changes held at this node
        #      from lazy propagation; finally update current
        #      node's value
        node_low, node_high, val, delta = self.tree[tree_idx]
        if low > node_high or high < node_low:
            return self._default
        if low <= node_low and high >= node_high:
            return self._incr_range(node_low, node_high, val, delta)

        self._propagate(tree_idx)
        left_val = self._range_query(tree_idx*2, low, high)
        right_val = self._range_query(tree_idx*2+1, low, high)
        self._update(tree_idx)
        return self._op(left_val, right_val)
    
    def range_update(self, i, j, val):
        self._range_update(1, i, j-1, val)

    def _range_update(self, tree_idx, low, high, val):
        # 3 cases:
        #   1. disjoint, do nothing
        #   2. full cover, increment by val
        #   3. partial cover, push down the changes previously
        #      held at this node from lazy propagation, and
        #      recursively increment children nodes; finally
        #      update current node's value
        node_low, node_high, node_val, delta = self.tree[tree_idx]
        if low > node_high or high < node_low:
            return
        if low <= node_low and high >= node_high:
            self.tree[tree_idx][3] = self._incr(delta, val)
            return

        self._propagate(tree_idx)
        self._range_update(tree_idx*2, low, high, val)
        self._range_update(tree_idx*2+1, low, high, val)
        self._update(tree_idx)
    
    def point_update(self, i, val):
        self._range_update(1, i, i, val)


class SegmentTreeSumAdd(SegmentTree):
    def _op(self, a, b):
        return a + b
    
    def _incr(self, val, delta):
        return val + delta
    
    def _incr_range(self, low, high, val, delta):
        return val + (high - low + 1) * delta
    
    @property
    def _default(self):
        return 0
    

class SegmentTreeMinAdd(SegmentTree):
    def _op(self, a, b):
        return min(a, b)
    
    def _incr(self, val, delta):
        return val + delta
    
    def _incr_range(self, low, high, val, delta):
        return val + delta
    
    @property
    def _default(self):
        return float('inf')


# helper functions for Fenwick Tree

def get_lsd(n):
    """taken from stackoverflow
    https://stackoverflow.com/questions/5520655/return-index-of-least-significant-bit-in-python
    """
    return (n&-n).bit_length()-1


def get_next_lower(n):
    return n - (1 << get_lsd(n))


def get_next_higher(n):
    return n + (1 << get_lsd(n))


# Fenwick Tree (aka Binary Indexed Tree)
# Note that this only implements prefix operations
# so we can't do range min or range max with this data structure
# I've only implemented range sum below

class FenwickTree(RangeSumAdd):
    def __init__(self, vals):
        self.tree = [0] * len(vals)
        # note: there is a more efficient way to do this
        for i, val in enumerate(vals):
            self.point_update(i, val)
    
    def point_update(self, i, val):
        idx = i+1
        while idx <= len(self.tree):
            self.tree[idx-1] += val
            idx = get_next_higher(idx)
    
    def range_update(self, i, j, val):
        for k in range(i, j):
            self.point_update(k, val)
        
    def range_query(self, i, j):
        return self.prefix_sum(j) - self.prefix_sum(i)

    def prefix_sum(self, i):
        out = 0
        while i != 0:
            out += self.tree[i-1]
            i = get_next_lower(i)
        return out