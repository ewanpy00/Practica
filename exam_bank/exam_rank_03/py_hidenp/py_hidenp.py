def hidenp(small: str, big: str) -> bool:
    it = iter(big)
    return all(c in it for c in small)

print(hidenp("abc", "a1b2c3"))
print(hidenp("abc", "acb"))
print(hidenp("", "anything"))
