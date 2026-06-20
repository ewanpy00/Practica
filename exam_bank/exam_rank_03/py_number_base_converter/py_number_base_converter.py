def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if not (2 <= from_base <= 36) or not (2 <= to_base <= 36):
        return "ERROR"
    if not number:
        return "ERROR"

    value = 0
    for ch in number.upper():
        if ch not in digits:
            return "ERROR"
        d = digits.index(ch)
        if d >= from_base:
            return "ERROR"
        value = value * from_base + d

    if value == 0:
        return "0"

    out = ""
    while value > 0:
        out = digits[value % to_base] + out
        value //= to_base

    return out

print(number_base_converter("1010", 2, 10))
print(number_base_converter("FF", 16, 2))
print(number_base_converter("10", 2, 99))
