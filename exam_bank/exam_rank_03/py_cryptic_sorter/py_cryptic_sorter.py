def cryptic_sorter(strings: list[str]) -> list[str]:
    vowels = "aeiou"

    def case_insensitive(s):
        return "".join(c.lower() if c.isalpha() else c for c in s)

    def vowel_count(s):
        return sum(1 for c in s.lower() if c in vowels)

    return sorted(strings, key=lambda s: (len(s), case_insensitive(s), vowel_count(s)))

# print(cryptic_sorter(["apple", "cat", "banana", "dog", "elephant"]))
