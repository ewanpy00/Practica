class PrefixDictionary:
    def __init__(self):
        self.root = {}

    def insert(self, word: str) -> None:
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
        node["$"] = True

    def _walk(self, text: str):
        node = self.root
        for c in text:
            if c not in node:
                return None
            node = node[c]
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and "$" in node

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

# d = PrefixDictionary(); d.insert("apple")
# print(d.search("apple"), d.search("app"), d.starts_with("app"))
