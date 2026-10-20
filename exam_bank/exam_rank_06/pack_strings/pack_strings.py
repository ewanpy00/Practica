def pack(strs: list[str]) -> str:
    return "".join("%d:%s" % (len(s), s) for s in strs)


def unpack(s: str) -> list[str]:
    result = []
    i = 0

    while i < len(s):
        colon = s.index(":", i)
        length = int(s[i:colon])
        result.append(s[colon + 1:colon + 1 + length])
        i = colon + 1 + length

    return result

# print(unpack(pack(["hello", "world"])))
# print(unpack(pack([])), unpack(pack([""])))
