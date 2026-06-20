def twist_sequence(arr: list[int], k: int) -> list[int]:
    if not arr:
        return []

    k = k % len(arr)
    if k == 0:
        return arr[:]

    return arr[-k:] + arr[:-k]

print(twist_sequence([1, 2, 3, 4, 5], 2))
print(twist_sequence([1, 2, 3], 1))
