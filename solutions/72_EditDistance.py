# problem: https://leetcode.com/problems/edit-distance/

# Approach:
# DP over two indices: i and j, which are used to index into the two words
# minDistance(word1[i:], word2[j:]) = 
#  case 1: word1[i] == word2[j] and we choose to use it: minDistance(word1[i+1:], word2[j+1:])
#  case 2a: word1[i] != word2[j]: delete word1[i] -> 1 + minDistance(word1[i+1:], word2[j:])
#  case 2b: word1[i] != word2[j]: insert word2[j] at index i in word1 -> 1 + minDistance(word1[i:], word2[j+1:])
#  case 2c: word1[i] != word2[j]: replace word1[i] with word2[j] -> 1 + minDistance(word1[i+1:], word2[j+1:])

# time: O(M*N)
# space: O(M*N)

class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        n, m = len(word1), len(word2)
        def dp(i, j, memo={}):
            if (i, j) in memo:
                return memo[(i, j)]
            if i == n:
                out = m - j
            elif j == m:
                out = n - i
            else:
                a = dp(i+1, j, memo) + 1
                b = dp(i, j+1, memo) + 1
                c = dp(i+1, j+1, memo) + 1
                if word1[i] == word2[j]:
                    c -= 1
                out = min(a, b, c)
            memo[(i, j)] = out
            return out

        return dp(0, 0, {})
