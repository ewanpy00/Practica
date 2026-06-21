def is_match(s, pattern):
    def helper(i, j):
        if j == len(pattern):
            return i == len(s)

        c = pattern[j]
        mod = pattern[j + 1] if j + 1 < len(pattern) and pattern[j + 1] in "*." else ""

        if mod == "*":
            if i + 1 < len(s) and s[i] == c and s[i + 1] == c:
                return helper(i + 2, j + 2)
            return False

        if mod == ".":
            if i >= len(s) or s[i] != c:
                return False
            k = i + 1
            while True:
                if helper(k, j + 2):
                    return True
                if k < len(s) and s[k] == c:
                    k += 1
                else:
                    return False

        if i < len(s) and s[i] == c:
            return helper(i + 1, j + 1)
        return False

    return helper(0, 0)

# print(is_match("aab", "a*b"))
# print(is_match("aaab", "a.b"))
# print(is_match("ab", "a.b"))
# print(is_match("ab", "a*b"))
