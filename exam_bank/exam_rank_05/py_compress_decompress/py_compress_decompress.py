def compress(s: str) -> str:
    if not s:
        return ""

    result = []
    prev = s[0]
    count = 1

    for c in s[1:]:
        if c == prev:
            count += 1
        else:
            result.append(prev + (str(count) if count > 1 else ""))
            prev = c
            count = 1
    result.append(prev + (str(count) if count > 1 else ""))

    return "".join(result)


def decompress(s: str) -> str:
    result = []
    i = 0
    n = len(s)

    while i < n:
        c = s[i]
        i += 1
        num = ""
        while i < n and s[i].isdigit():
            num += s[i]
            i += 1
        count = int(num) if num else 1
        result.append(c * count)

    return "".join(result)

# print(compress("aabcccccaaa"))
# print(decompress("a2bc5a3"))
# print(compress(""))
