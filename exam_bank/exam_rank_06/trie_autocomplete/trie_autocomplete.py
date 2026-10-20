def trie_autocomplete(words: list[str], prefix: str) -> list[str]:
    root = {}
    for word in words:
        node = root
        for c in word:
            node = node.setdefault(c, {})
        node["$"] = True

    node = root
    for c in prefix:
        if c not in node:
            return []
        node = node[c]

    result = []

    def collect(current, path):
        if "$" in current:
            result.append(path)
        for c in sorted(k for k in current if k != "$"):
            collect(current[c], path + c)

    collect(node, prefix)
    return result

# print(trie_autocomplete(["apple", "app", "apricot", "banana"], "app"))
# print(trie_autocomplete(["a", "ab", "abc"], ""))
