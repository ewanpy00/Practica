def string_permutation_checker(s1: str, s2: str) -> bool:
    return sorted(s1) == sorted(s2)

print(string_permutation_checker("abc", "bca"))
print(string_permutation_checker("abc", "def"))
