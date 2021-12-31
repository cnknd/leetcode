# problem: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/

# strategy: we can apply binary search with a few additional comparisons
#           at each iteration.
#           if left < right: then array is sorted, min value is left
#           otherwise:
#                  find mid, compare mid with left
#                  if left > mid: then pivot is at or to left of mid
#                                 then search in range [left, mid];
#                                 note that this also means mid < right
#                  if left < mid: then pivot is to the right of mid
#                                 then search in range (mid, right];

class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums)-1
        while left < right:
            if nums[left] < nums[right]:
                return nums[left]
            else:
                if right - left == 1:
                    return min(nums[left], nums[right])
                mid = left + (right - left) // 2
                if nums[left] > nums[mid]:
                    right = mid
                else:
                    left = mid+1

        return nums[left]