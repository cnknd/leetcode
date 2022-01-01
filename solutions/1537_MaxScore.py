# problem: https://leetcode.com/problems/get-the-maximum-score/

# strategy: we can break the two arrays into pieces at common elements:
#             2-3-4-5-6-8-10   -> 2-3 4-5-6-8 10
#             1-3-7-8-9        -> 1-3 7-8     9
#        I chose to use a common element as the end point; I feel this will
#        be a bit easier code than using common element as the start point
#        of each piece.
#        Next we can calculate the sum of each piece and simply compare
#        corresponding pieces from each array and pick the one with the
#        larger sum to our total score.

# details: how do we find the common elements in each array? We know
#        that each array only contains unique elements, so naively we can
#        put one array into a hashset, then iterate through the other array
#        to identify elements that are in the first array's hashset.
#        A better method is to leverage the fact that the arrays are sorted
#        and iterate through each array with a pointer and increment the
#        two pointers in a way that they land at common elements at the
#        same time. To achieve this, we can use a while loop and at every
#        iteration simply increment the pointer with the smaller value.
#        Once the two pointers have the same value, we found a common
#        element and we can increment both pointers.

# optimization: Now that we have the common elements, we can loop through
#        the arrays again to calculate piecewise sums. And we loop through
#        the piecewise sums to pick the better one to add to a running
#        maximum score. However, we can bundles these steps together with
#        the original while loop that identified the common elements:
#        we track a running current piece score for each array, and
#        as we increment one or both pointers, we add the new value(s)
#        to the corresponding piece score(s). If we've hit a common element,
#        we can just pick the higher current piece score and add it to
#        the running maximum score.

class Solution:
    def maxSum(self, nums1: List[int], nums2: List[int]) -> int:
        # initialize two pointers, running maximum score, and the
        # two current piece scores
        i, j = 0, 0
        max_cumulative_score = 0
        current_sum1, current_sum2 = 0, 0

        while True:
            # when we've reached the end of one array, simply
            # add the rest of the second array to its current piece
            # score and then select the better current piece score
            # to add to the running maximum score
            if i == len(nums1):
                current_sum2 += sum(nums2[j:])
                max_cumulative_score += max(current_sum1, current_sum2)
                break
            elif j == len(nums2):
                current_sum1 += sum(nums1[i:])
                max_cumulative_score += max(current_sum1, current_sum2)
                break
            # when we hit a common element, add it to both current piece
            # scores and then select the better current piece score
            # to add to the running maximum score; then increment both
            # pointers
            elif nums1[i] == nums2[j]:
                current_sum1 += nums1[i]
                current_sum2 += nums2[j]
                max_cumulative_score += max(current_sum1, current_sum2)
                current_sum1, current_sum2 = 0, 0
                i += 1
                j += 1
            # when we're not at a common element, add the smaller value
            # to its corresponding piece score and increment its pointer
            elif nums1[i] < nums2[j]:
                current_sum1 += nums1[i]
                i += 1
            else: # nums2[j] < nums1[i]
                current_sum2 += nums2[j]
                j += 1

        # the problem asked for the result to be given in mod (10^9+7)
        return max_cumulative_score % (10**9+7)
            
            