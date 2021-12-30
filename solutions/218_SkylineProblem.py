# problem: https://leetcode.com/problems/the-skyline-problem/

# solution:
#     We can describe the problem as follows: at every point on the
#     x-axis where there is a potential height change, what is largest
#     height immediately to the right of this point?
#     We need to iterate through these significant points from left
#     right, and that we need to constantly keep track of a maximum
#     height of buildings where we have not gone past their right
#     endpoints. The obvious data structure to use to track a maximum
#     among a list of objects is a max-heap. So the strategy to tackle
#     the problem looks like this:
#     1. sort the significant points (left and right endpoints of buildings)
#        from left to right
#     2. iterate through the significant points, at each point, add buildings
#        we have not yet seen to a max-heap keyed off the height
#     3. also at each point, pop max element from the heap if that element
#        is associated with a building whose right endpoint is less than
#        or equal to the current significant point (we've gone past that
#        particular building, so we can't consider its height anymore)
#     4. finally we read the max height from what's remaining in the heap.

# implementation details:
#     * I sort the buildings first by left-endpoint into a stack so as I
#       iterate through significant points I can simply pop buildings off
#       the stack
#     * only height and right endpoint are stored in the heap (no reason to
#       include left endpoint as it's already been used as criterion for
#       entry into the heap)
#     * I added a building of height 0 that stretches to infinity to the
#       heap so I don't need to worry about the case where heap is empty
#     * python only has min-heap (and not max-heap), so to deal with this
#       I simply multiplied all heights by -1

# time complexity: O(nlogn)
#     * sorting buildings by left-endpoint: O(nlogn)
#     * sorting significant points: O(2nlog(2n)) = O(nlogn)
#     * heap operations as we iterate through significant points: O(nlogn)
#         * we don't need to look at the time complexity of each iteration
#           of the loop as it varies from iteration to iteration.
#         * we can simply ask how many operations are performed
#           on each building
#         * we perform 3 operations on each building: pop from stack,
#           push onto heap, and pop from heap
#         * popping a building from stack is O(1), while the two
#           heap operations are O(logn)
#         * with n buildings, total time complexity of the main loop
#           is O(nlogn)
# space complexity: O(n)
#      * O(n) to store significant points
#      * O(n) to store the heap
#      * O(n) to store the output

from typing import List
import heapq


class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        # sort buildings in descending order of left-endpoint
        # use this as a stack. as we scan the input from left to right
        # we would be popping buildings from the end of the stack
        # to add the the heap
        buildings.sort(key=lambda x: x[0], reverse=True)
        
        # identify significant points
        significant_points = []
        for building in buildings:
            significant_points.append(building[0])
            significant_points.append(building[1])
        significant_points.sort()

        # always keep a fictitious building of 0 height so we don't have
        # to handle the case where there is no building left in the heap
        current_buildings = [(0, float('inf'))]
        heapq.heapify(current_buildings)
        skyline = []
        for p in significant_points:
            # remove from stack and put onto heap
            while len(buildings) and buildings[-1][0] <= p:
                left, right, height = buildings.pop()
                tmp = (-height, right)
                heapq.heappush(current_buildings, tmp)
            # remove from heap
            while current_buildings[0][1] <= p:
                _ = heapq.heappop(current_buildings)
            new_height = -current_buildings[0][0]
            self.addToSkyline(skyline, p, new_height)
        return skyline

    def addToSkyline(self, skyline, x, height):
        if len(skyline) > 0 and skyline[-1][1] == height:
            pass
        else:
            skyline.append([x, height])
