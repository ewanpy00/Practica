def echo_validator(text: str) -> bool:
    cleaned = [c.lower() for c in text if c.isalpha()]
    return cleaned == cleaned[::-1]

print(echo_validator("racecar"))
print(echo_validator("A man a plan a canal Panama"))
print(echo_validator("hello"))
