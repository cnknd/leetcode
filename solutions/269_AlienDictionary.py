# problem: https://leetcode.com/problems/alien-dictionary/

# strategy: two steps:
#   1. scan words and build ordering graph. e.g. if we have ['acb', 'abc'],
#      then we get that 'c' -> 'b', where '->' indicates a 'preceeds' relation;
#      note that we can only get at most ONE relation for each two adjacent
#      words in the words list. We get no information if we have something like
#      ['ab', 'abc']. And we have an invalid input if we have something like
#      ['abc', 'ab'].
#   2. The 'preceeds' relationships form a directed graph. Now to find a valid
#      ordering of the alphabet, we simply compute the topological ordering on
#      this graph (I've implemented DFS as I'm not familiar with other algorithms
#      for topological sort). If we detect a cycle in the graph, then the original
#      input would be invalid (e.g. ['a', 'b', 'a']).

# implementation details:
#   * I wrote separate functions for each of the two steps, and each would raise an
#     error if it detects invalid input (for getting ordering information, invalid
#     means a word preceeds a prefix of itself; for topological sort, invalid means
#     there's a cycle in the ordering graph). This way in the main function I can
#     immediately return "" upon detecting invalid input.
#   * I used a recursive implementation of DFS, but there are other ways to do this.
#     This is a matter of personal taste.

# time complexity: O(M*N), M is the length of each word, N is the number of words
# space complexity: O(1) here due to limited alphabet size. Space complexity is
#                   determined by the information about the nodes and edges of the
#                   ordering graph. We can only have at most 26^2 number of edges
#                   in the graph due to a 26 letter alphabet, so we only need
#                   constant space. But if we have an unlimited alphabet (e.g.
#                   characters are separated by some delimiter and each character
#                   is actually a string of unlimited size), then the space
#                   complexity would be O(N), as we can only get at most one
#                   edge per pair of adjacent words.

from collections import defaultdict

class Solution:
    def alienOrder(self, words: List[str]) -> str:
        # get alphabet
        alphabet = set()
        for word in words:
            for char in word:
                alphabet.add(char)

        # get edges
        edges = set()
        for i in range(1, len(words)):
            try:
                edge = self.getEdge(words[i-1], words[i])
            except:
                return ""
            if edge:
                edges.add(edge)

        # construct topological ordering on alphabet
        out = self.topologicalSort(alphabet, edges)
        return out

    def getEdge(self, word1, word2):
        for i in range(min(len(word1), len(word2))):
            if word1[i] != word2[i]:
                return (word1[i], word2[i])
        if len(word1) > len(word2):
            raise RuntimeError("bad ordering!")
        return

    def topologicalSort(self, alphabet, edges):
        """if we identify a cycle, return ""
        otherwise return a topological ordering
        of the alphabet given the edges
        """
        out = []
        seen = set()
        processed = set()

        adj_list = defaultdict(list)
        for char1, char2 in edges:
            adj_list[char1].append(char2)

        def dfs(char):
            if char in seen:
                if char not in processed:
                    raise RuntimeError("cycle detected")
                else:
                    return
            seen.add(char)
            if char in processed:
                return
            for next_char in adj_list[char]:
                dfs(next_char)
            out.append(char)
            processed.add(char)

        for letter in alphabet:
            try:
                dfs(letter)
            except RuntimeError:
                return ""

        return "".join(reversed(out))
