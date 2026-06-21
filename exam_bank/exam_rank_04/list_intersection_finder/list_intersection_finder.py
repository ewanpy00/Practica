def find_intersection(l1, l2):
    result = []

    for value in l1:
        if value in l2 and value not in result:
            result.append(value)

    return sorted(result)

# print(find_intersection([1, 2, 3, 4], [2, 4, 6]))
# print(find_intersection([1, 1, 2], [1, 1, 1]))
# print(find_intersection([1, 2], [3, 4]))
