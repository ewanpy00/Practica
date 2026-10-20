class _Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class CacheKeeper:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.nodes = {}
        self.head = _Node()   # least recently used side
        self.tail = _Node()   # most recently used side
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _append(self, node):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key: int) -> int:
        node = self.nodes.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._append(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self.nodes.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._append(node)
            return
        node = _Node(key, value)
        self.nodes[key] = node
        self._append(node)
        if len(self.nodes) > self.capacity:
            oldest = self.head.next
            self._unlink(oldest)
            del self.nodes[oldest.key]

# c = CacheKeeper(2); c.put(1, 1); c.put(2, 2); c.get(1); c.put(3, 3)
# print(c.get(2), c.get(1))
