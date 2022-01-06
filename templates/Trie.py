import string


ALPHABET = string.ascii_lowercase
ALPHABET_SIZE = len(ALPHABET)


class TrieNode:
    def __init__(self):
        """Here I pre-allocate slots to children nodes
        compared to the alternative of not pre-allocating
        these slots, insertion is a bit faster, while
        deletion is a bit slower.
        I've included a flag to indicate word-end, but
        word-end can also be implemented as an extra
        child node for empty string with no children.
        (although deletion might get a bit more complicated)
        """
        self.children = [None] * ALPHABET_SIZE
        self.end_of_word = False


class Trie:
    def __init__(self, words=[]):
        self.root = TrieNode() # root node
        for word in words:
            self.insert(word)

    def get_loc(self, char):
        # if alphabet is set to ascii_lowercase,
        # then ord(char) - ord('a') is faster
        return ALPHABET.index(char)

    def insert(self, word):
        current = self.root
        for char in word:
            loc = self.get_loc(char)
            if not current.children[loc]:
                current.children[loc] = TrieNode()
            current = current.children[loc]
        current.end_of_word = True
    
    def delete(self, word):
        """this only deletes if the exact word exists in the
        trie
        """
        self._delete(self.root, word)
        
    def _delete(self, node, suffix):
        """helper function
        """
        loc = self.get_loc(suffix[0])
        child = node.children[loc]
        # tree doesn't contain the next letter in the word
        if not child:
            return
        if len(suffix) == 1:
            # next letter is end of suffix, and tree has no
            # other words in this branch, we can remove
            if not any(child.children):
                node.children[loc] = None
            # next letter is end of suffix, but tree
            # contains other words, we remove end-of-word
            # flag from the child
            else:
                child.end_of_word = False
                return

        else:
            self._delete(child, suffix[1:])
            
    def find(self, word):
        node = self._find_node(word)
        if node and node.end_of_word:
            return True
        return False
        
    def search(self, prefix):
        """returns all words that start with prefix
        """
        node = self._find_node(prefix)
        suffixes = self._get_suffixes(node)
        return [prefix + suffix for suffix in suffixes]
        
    def _find_node(self, prefix):
        current = self.root
        for char in prefix:
            loc = self.get_loc(char)
            if not current.children[loc]:
                return
            current = current.children[loc]
        return current
    
    def _get_suffixes(self, node):
        out = []
        for i, child in enumerate(node.children):
            if child:
                char = ALPHABET[i]
                out.extend([char + suffix for suffix in self._get_suffixes(child)])
        if node.end_of_word:
            out.append('')
        return out

