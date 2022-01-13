# problem: https://leetcode.com/problems/flip-string-to-monotone-increasing/

# strategy: at every bit in the binary string, we can either flip or not flip it,
#           so we can iterate through the binary string and at each bit track the 
#           minimum number of flips up to and including that bit.
#           These two values depend only on the two values from the previous bit AND
#           the values of the previous and current bits.
#           There are four possibilities for the arrangement of two consecutive bits:
#           00, 11, 01, 10; the update to the two minimum values will be different
#           for each arrangement.

# Example: 00110
# 0 -> 0, 1
# 00 -> 0, 1
# 001 -> 0, 1
# 0011 -> 0, 2
# 00110 -> 2, 1
# --> answer: 1

# Note: this is basically a Dynamic Programming solution, and the description
#       above lends to a bottom-up implementation that is optimized to only use
#       constant space


class Solution:
    def minFlipsMonoIncr(self, s: str) -> int:
        res_no_flip, res_flip = 0, 1
        for i in range(1, len(s)):
            char, prev_char = s[i], s[i-1]
            if prev_char == '0' and char == '0':
                res_no_flip, res_flip = res_no_flip, min(res_no_flip, res_flip)+1

            elif prev_char == '1' and char == '1':
                res_no_flip, res_flip = res_no_flip, res_flip+1
            
            elif prev_char == '0' and char == '1':
                res_no_flip, res_flip = min(res_no_flip, res_flip), res_no_flip+1
            
            else: # prev_char == '1' and char == '0':
                res_no_flip, res_flip = res_flip, min(res_no_flip, res_flip)+1

        return min(res_no_flip, res_flip)
