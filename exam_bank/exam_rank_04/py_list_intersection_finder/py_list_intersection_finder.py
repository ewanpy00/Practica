def list_intersection_finder(lists: list[list[int]]) -> list[int]:
    if not lists:
        return []

    common = set(lists[0])
    for current in lists[1:]:
        common &= set(current)
        if not common:
            return []

    return sorted(common)

# print(list_intersection_finder([[1, 2, 3], [2, 3, 4], [2, 3, 5]]))
# print(list_intersection_finder([[1, 2, 3], []]))
# print(list_intersection_finder([]))
