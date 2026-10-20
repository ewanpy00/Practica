def merge_sorted_lists(lists: list[list[int]]) -> list[int]:
    merged = []
    for current in lists:
        merged = _merge_two(merged, current)
    return merged


def _merge_two(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# print(merge_sorted_lists([[1, 3, 5], [2, 4, 6]]))
# print(merge_sorted_lists([[], [1, 2, 3]]))
# print(merge_sorted_lists([[-5, -1, 0], [-3, 2, 4]]))
