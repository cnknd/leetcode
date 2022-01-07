# problem: https://leetcode.com/problems/design-add-and-search-words-data-structure/

# approach: simply build a Trie data structure; now wildcard character does increase search
#           time, as we would need to explore all children at a given node where the next
#           character is a wildcard.

# implementation details: root node and end of word nodes are simply TrieNode('')

class TrieNode:
    def __init__(self, char=''):
        self.char = char
        self.children = {}
    
    def add_child(self, child):
        """adds child node to current node
        """
        self.children[child.char] = child

    def find_child(self, char):
        """returns TrieNode that is a child of the
        current node and represents the given
        character
        """
        return self.children.get(char, None)

    def get_all_children(self):
        """returns a list of all children;
        this is used to match wildcard
        """
        return self.children.values()


class WordDictionary:

    def __init__(self):
        self.root = TrieNode('')


    def addWord(self, word: str) -> None:
        current = self.root
        for char in word:
            child = current.find_child(char)
            if not child:
                child = TrieNode(char)
                current.add_child(child)
            current = child
        current.add_child(TrieNode(''))
        

    def search(self, word: str) -> bool:
        return self._search(self.root, word)

    
    def _search(self, node, suffix):
        if len(suffix) == 0:
            return '' in node.children
        if suffix[0] == '.':
            return any([self._search(child, suffix[1:]) for child in node.get_all_children()])
        child = node.find_child(suffix[0])
        if child:
            return self._search(child, suffix[1:])
        else:
            return False


# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)