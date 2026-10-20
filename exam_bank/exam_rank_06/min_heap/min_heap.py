class MinHeap:
    def __init__(self):
        self.data = []

    def push(self, val: int) -> None:
        self.data.append(val)
        i = len(self.data) - 1
        while i > 0:
            parent = (i - 1) // 2
            if self.data[parent] <= self.data[i]:
                break
            self.data[parent], self.data[i] = self.data[i], self.data[parent]
            i = parent

    def pop(self) -> int | None:
        if not self.data:
            return None
        top = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            i = 0
            n = len(self.data)
            while True:
                smallest = i
                for child in (2 * i + 1, 2 * i + 2):
                    if child < n and self.data[child] < self.data[smallest]:
                        smallest = child
                if smallest == i:
                    break
                self.data[i], self.data[smallest] = self.data[smallest], self.data[i]
                i = smallest
        return top

    def peek(self) -> int | None:
        return self.data[0] if self.data else None

    def size(self) -> int:
        return len(self.data)

# h = MinHeap(); h.push(5); h.push(3); h.push(8)
# print(h.peek(), h.pop(), h.peek(), h.size())
