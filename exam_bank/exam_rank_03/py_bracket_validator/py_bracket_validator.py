def bracket_validator(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    opening = set(pairs.values())
    stack = []

    for c in s:
        if c in opening:
            stack.append(c)
        elif c in pairs:
            if not stack or stack[-1] != pairs[c]:
                return False
            stack.pop()

    return not stack

# print(bracket_validator("()"))
# print(bracket_validator("()[]{}"))
# print(bracket_validator("(]"))
# print(bracket_validator("([)]"))
# print(bracket_validator("{[]}"))
