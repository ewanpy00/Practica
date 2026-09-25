from collections import deque
from string import ascii_lowercase


def word_ladder(start: str, end: str, sentence: list[str]) -> int:
    word_set = set(sentence)
    if end not in word_set:
        return 0

    queue = deque([(start, 1)])
    visited = {start}

    while queue:
        word, steps = queue.popleft()
        if word == end:
            return steps

        for i in range(len(word)):
            for ch in ascii_lowercase:
                if ch == word[i]:
                    continue
                candidate = word[:i] + ch + word[i + 1:]
                if candidate in word_set and candidate not in visited:
                    visited.add(candidate)
                    queue.append((candidate, steps + 1))

    return 0

# print(word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]))
# print(word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log"]))
