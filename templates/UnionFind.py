# basics: pointers are in the form of a list called "parent"
#         where root node of each component occurs where parent[i] == i

# naive implementation with lazy union: O(N) find, O(N) union

def find(parent, i):
    current = i
    while parent[current] != current:
        current = parent[current]
    return current

def union(parent, node1, node2):
    leader1 = find(parent, node1)
    leader2 = find(parent, node2)
    parent[leader1] = leader2

 
# union by rank: O(logN) find, O(logN) union
# We store both parent and rank values,
# so either we need two lists, or a list of pairs.
# I've implemented with two lists here.
# In this implementation I've put the calls
# to find directly inside the union function.
# But you can also keep it outside

def union(parent, rank, node1, node2):
    leader1 = find(parent, node1)
    leader2 = find(parent, node2)
    if leader1 == leader2:
        return
    if rank[leader1] > rank[leader2]:
        parent[leader2] = leader1
    elif rank[leader2] > rank[leader1]:
        parent[leader1] = leader2
    else: # rank[leader1] == rank[leader2]
        parent[leader2] = leader1
        rank[leader1] += 1

# with path compression: O(Nlog*N) for the entire
#     algorithm to find connected components.
#     log* is the inverse-Ackerman function and can
#     be treated as constant for all practical purposes
# Upon each call to find, we update the 
# parent of the argument of find to the leader of
# its component. We implement this via a recursive
# definition of find

def find(parent, i):
    if parent[i] == i:
        return i
    else:
        parent[i] = find(parent, parent[i])
        return parent[i]

