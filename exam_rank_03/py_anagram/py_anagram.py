def anagram(s1: str, s2: str) -> bool:
    a = sorted(c.lower() for c in s1 if c != " ")
    b = sorted(c.lower() for c in s2 if c != " ")
    return a == b

print(anagram("listen", "silent"))
print(anagram("Triangle", "Integral"))
print(anagram("hello", "world"))
