def merge_sorted(arrays):
    result = []

    for array in arrays:
        for value in array:
            result.append(value)

    return sorted(result)

# print(merge_sorted([[3, 1], [2], [5, 4]]))
# print(merge_sorted([[10, -1, 7], [0]]))
# print(merge_sorted([[], [2, 1], []]))
# print(merge_sorted([]))
# print(merge_sorted([[2, 2], [1, 2]]))
