# problem: https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/

# solution: this problem can be solved either with graph search (BFS or DFS) or Union Find.
#           I've implemented Union Find here. With the two well-known optimizations (union by rank
#           and path compression), the runtime of this algorithm is O(Nlog*(N)), where log* is the
#           inverse Ackermann function, and for all practical purposes we can treat it as a constant

def find(parent, i):
    if parent[i] == i:
        return i
    else:
        parent[i] = find(parent, parent[i])
        return parent[i]

def union(parent, rank, leader1, leader2):
    if rank[leader1] > rank[leader2]:
        parent[leader2] = leader1
    elif rank[leader2] > rank[leader1]:
        parent[leader1] = leader2
    else: # rank[leader1] == rank[leader2]
        parent[leader2] = leader1
        rank[leader1] += 1


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        parent = list(range(n))
        rank = [0 for _ in parent]
        for node1, node2 in edges:
            leader1 = find(parent, node1)
            leader2 = find(parent, node2)
            if leader1 != leader2:
                union(parent, rank, leader1, leader2)
        return len([i for i in range(n) if parent[i] == i])