def pattern_tracker(text: str) -> int:
    count = 0

    for i in range(len(text) - 1):
        a, b = text[i], text[i + 1]
        if a.isdigit() and b.isdigit() and int(b) - int(a) == 1:
            count += 1

    return count

print(pattern_tracker("123"))
print(pattern_tracker("1357"))
print(pattern_tracker("90"))
