# Problem: https://leetcode.com/problems/making-a-large-island/

# Brute force: for each point on the grid, if it's 0, convert to 1, otherwise it stays at 1,
#              then do DFS/BFS on that point to find the size of the resulting island
#              this will run in O(N^4)

# Better strategy: Find all existing islands, then for each location with value 0 on the grid,
#                  find all its bordering islands, add those areas plus 1 to calculate the
#                  size of the resulting island if that location was turned into 1.
#                  Finding existing islands with simple DFS/BFS is O(N^2), the second step
#                  is also O(N^2) as we're visiting each location once, and the processing
#                  at each location is constant time (will use hashmaps to store island id
#                  for each location and area for each island id, and there are only 4 adjacent
#                  locations to perform these lookups on).

from typing import List

class Solution:
    def largestIsland(self, grid: List[List[int]]) -> int:
        islands, areas = self.findAllIslands(grid)
        return self.calcLargest(grid, islands, areas)
        
    def findAllIslands(self, grid):
        """returns two things:
        1. mapping from location (row, col) to island number
        2. area of each island
        I will implement this with DFS
        """
        n = len(grid)
        seen = set()
        islands = {}
        areas = {}
        current_island = set()

        def dfs(row, col):
            if (row, col) in seen:
                return
            seen.add((row, col))
            current_island.add((row, col))
            adjacents = self.getAdjacents(row, col, n)
            for adj_row, adj_col in adjacents:
                if grid[adj_row][adj_col] == 1:
                    dfs(adj_row, adj_col)
        
        island_num = 0
        for row in range(n):
            for col in range(n):
                if (row, col) in seen:
                    continue
                elif grid[row][col] == 1:
                    dfs(row, col)
                    areas[island_num] = len(current_island)
                    for loc in current_island:
                        islands[loc] = island_num
                    island_num += 1
                    current_island = set()
        
        return islands, areas
    
    def calcLargest(self, grid, islands, areas):
        # no island
        if not len(areas):
            return 1

        n = len(grid)
        largest = 0 # if all 1s, then the for loops won't update largest
        for row in range(n):
            for col in range(n):
                if grid[row][col] == 0:
                    adjacents = self.getAdjacents(row, col, n)
                    adj_islands = set()
                    for adj_row, adj_col in adjacents:
                        if grid[adj_row][adj_col] == 1:
                            adj_islands.add(islands[(adj_row, adj_col)])
                    candidate_area = sum([areas[island] for island in adj_islands]) + 1
                    largest = max(largest, candidate_area)
        if largest == 0:
            return n**2
        else:
            return largest

    def getAdjacents(self, row, col, n):
        out = []
        if row > 0:
            out.append((row-1, col))
        if row < n-1:
            out.append((row+1, col))
        if col > 0:
            out.append((row, col-1))
        if col < n-1:
            out.append((row, col+1))
        return out