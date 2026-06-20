def whisper_cipher(text: str, shift: int) -> str:
    result = []

    for c in text:
        if c.isupper():
            result.append(chr((ord(c) - ord("A") + shift) % 26 + ord("A")))
        elif c.islower():
            result.append(chr((ord(c) - ord("a") + shift) % 26 + ord("a")))
        else:
            result.append(c)

    return "".join(result)

print(whisper_cipher("hello", 3))
print(whisper_cipher("khoor", -3))
