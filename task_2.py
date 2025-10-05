class _Node:
    """Node of Trie structure."""

    def __init__(self):
        """Initialize node with children and counters."""
        self.children = {}
        self.is_end = False
        self.subtree_words = 0


class Trie:
    """Basic Trie implementation."""

    def __init__(self):
        """Initialize empty root node."""
        self.root = _Node()

    def put(self, word: str, value):
        """Insert a word into the Trie."""
        if not isinstance(word, str):
            raise ValueError("word must be str")
        node = self.root
        node.subtree_words += 1
        for ch in word:
            if ch not in node.children:
                node.children[ch] = _Node()
            node = node.children[ch]
            node.subtree_words += 1
        node.is_end = True

    def _walk(self, s: str):
        """Traverse by prefix and return node or None."""
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def _collect_words(self):
        """Collect all words stored in Trie."""
        res, path = [], []

        def dfs(node: _Node):
            if node.is_end:
                res.append("".join(path))
            for ch, nxt in node.children.items():
                path.append(ch)
                dfs(nxt)
                path.pop()

        dfs(self.root)
        return res


class Homework(Trie):
    """Extended Trie with suffix and prefix methods."""

    def count_words_with_suffix(self, pattern) -> int:
        """Return number of words ending with given suffix."""
        if not isinstance(pattern, str):
            raise ValueError("pattern must be str")
        if pattern == "":
            return 0
        return sum(1 for w in self._collect_words() if w.endswith(pattern))

    def has_prefix(self, prefix) -> bool:
        """Check if any word has the given prefix."""
        if not isinstance(prefix, str):
            raise ValueError("prefix must be str")
        node = self._walk(prefix)
        if node is None:
            return False
        return node.subtree_words > 0


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    assert trie.count_words_with_suffix("e") == 1
    assert trie.count_words_with_suffix("ion") == 1
    assert trie.count_words_with_suffix("a") == 1
    assert trie.count_words_with_suffix("at") == 1
    assert trie.has_prefix("app") is True
    assert trie.has_prefix("bat") is False
    assert trie.has_prefix("ban") is True
    assert trie.has_prefix("ca") is True
