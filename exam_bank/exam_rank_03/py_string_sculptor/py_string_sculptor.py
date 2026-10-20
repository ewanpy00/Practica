def string_sculptor(text: str) -> str:
    result = []
    idx = 0

    for c in text:
        if c.isalpha():
            result.append(c.lower() if idx % 2 == 0 else c.upper())
            idx += 1
        else:
            result.append(c)

    return "".join(result)

# print(string_sculptor("hello"))
# print(string_sculptor("Hello World"))
