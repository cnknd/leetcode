class RangeQuery:
    def __init__(self, vals):
        self.vals = vals

    def range_query(self, i, j):
        pass

    def point_update(self, i, val):
        self.vals[i] = val

    def range_update(self, i, j, val):
        pass

# Example: queries are for range max, point updates are add a value
#          to the value at an existing index of the array,
#          range updates are add a value to all existing values
#          between two indices

# Basic implementation: store the original array
# Query time complexity: O(n)
# Point update time complexity: O(1)
class RangeMaxAdd(RangeQuery):
    def range_query(self, i, j):
        return max(self.vals[i:j])

    def point_update(self, i, val):
        self.vals[i] += val

    def range_update(self, i, j, val):
        for k in range(i, j):
            self.vals[k] += val

# Basic implementation: store the original array
# Query time complexity: O(n)
# Point update time complexity: O(1)
class PrefixMaxAdd(RangeQuery)
    pass
# 

# cool stuff
# 1. Segment Tree
# 2. Fenwick Tree

# Segment Tree

class SegmentTree(RangeQuery):
    def __init__(self, vals):
        pass