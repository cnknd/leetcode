# Usually we can implement an additional TrieNode class that we can instantiate as nodes of the tree. 
# Here instead of this I simply used a nested character dictionary to store the tree. This wouldn't be
# a good idea in a real system as it wouldn't allow you to implement any additional functions/features
# that you would normally be able to in a TrieNode class.

# nested character dictionary only containing the word apple would look like this:
# {'a':{'p':{'p':{'l':{'e':{'':''}}}}}}
# I used the empty string to denote the end of a word.
# When we add the word apples to the above dictionary, we get:
# {'a':{'p':{'p':{'l':{'e':{'':'', 's':{'':''}}}}}}}

class Trie:
    def __init__(self):
        self.data = {}

    def insert(self, word: str) -> None:
        self._insertHelper(word, self.data)

    def _insertHelper(self, suffix, current_dict):
        if len(suffix) == 0:
            current_dict[''] = ''
        else:
            if suffix[0] not in current_dict:
                current_dict[suffix[0]] = {}
            self._insertHelper(suffix[1:], current_dict[suffix[0]])

    def search(self, word: str) -> bool:
        return self._searchHelper(word, self.data)
        
    def _searchHelper(self, word, current_dict):
        if len(word) == 0:
            return '' in current_dict
        else:
            return word[0] in current_dict and self._searchHelper(word[1:], current_dict[word[0]])

    def startsWith(self, prefix: str) -> bool:
        return self._startsWithHelper(prefix, self.data)
        
    def _startsWithHelper(self, prefix, current_dict):
        if len(prefix) == 0:
            return True
        else:
            return prefix[0] in current_dict and self._startsWithHelper(prefix[1:], current_dict[prefix[0]])
