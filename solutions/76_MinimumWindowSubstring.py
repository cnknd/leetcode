# problem: https://leetcode.com/problems/minimum-window-substring/

# strategy: Naively we can do a double for loop (start and end points of substrings) over indices in
#           s and check that t is contained in each s[i:j]. This solution has a cubic runtime:
#           the double for loop is O(n^2), and the amount of work done to check in each iteration
#           of the inner loop is O(n).
#           We can replace the double for loop with a sliding window approach using two pointers:
#           if t is not contained in s[i:j], then increment j; if t is contained in s[i:j], then
#           increment i. This reduces the total runtime down to O(n^2), since the sliding window
#           portion does 2n pointer updates, while we check that t is contained in each s[i:j] in
#           linear time at each pointer update iteration.
#           Finally, we can optimize the checking step. One idea that comes to mind is to store
#           the frequencies of characters in t in a hashmap (freqs = {char:freq}), then as we increment
#           j in s and encounter a charater in t, we decrement that frequency counter. Then we only
#           have to check that the values in the hashmap are <= 0. This check operation has time
#           complexity (O(size of alphabet) = O(52) = O(1)).
#           This is nice, but we can speed up the algorithm a bit further by introducing another
#           hashset called "missing" to store characters in t that are still missing in s[i:j].
#           Now when we decrement a frequency counter in freqs to <= 0, we remove that character
#           from the "missing" hashset. Now at the cost of an additional constant amount of memory,
#           we've improved the speed of checking t in s[i:j] to one hashmap and one hashset operation.


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        # alternatively we can store freqs in a length 52 array
        # but a hashmap is easier to extend to cases with a larger
        # alphabet
        freqs = {}
        missing = set()
        for char in t:
            if char in freqs:
                freqs[char] += 1
            else:
                freqs[char] = 1
            missing.add(char)

        # we initialize a few variables:
        # shortest_len is the length of the minimum window that
        # satisfies the condition; it's initialized to a value that is
        # too large, so that if after looking through the entirety of s
        # and this shortest_len is still too large, we know we haven't
        # found any windows that satisfies the condition.
        # shortest_start and shortest_end record the [start, end) indices
        # of the minimum window
        # i and j are the two pointers that constitute our sliding window
        shortest_len = max(len(s), len(t)) + 1
        shortest_start, shortest_end = 0, 0
        i, j = 0, 0
        while True:
            if len(missing):
                if j == len(s):
                    break
                else:
                    self.add_char(s[j], freqs, missing)
                    j += 1

            else:
                length = j - i
                if length < shortest_len:
                    shortest_len = length
                    shortest_start, shortest_end = i, j
                self.remove_char(s[i], freqs, missing)
                i += 1

        if shortest_len == max(len(s), len(t)) + 1:
            return ""
        else:
            return s[shortest_start:shortest_end]

    def add_char(self, char, freqs, missing):
        if char in freqs:
            freqs[char] -= 1
            if freqs[char] <= 0 and char in missing:
                missing.remove(char)

    def remove_char(self, char, freqs, missing):
        if char in freqs:
            freqs[char] += 1
            if freqs[char] > 0:
                missing.add(char)
