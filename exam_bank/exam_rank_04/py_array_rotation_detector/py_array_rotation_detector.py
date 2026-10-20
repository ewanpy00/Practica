def array_rotation_detector(arr1: list, arr2: list) -> bool:
    if len(arr1) != len(arr2):
        return False
    if not arr1:
        return True

    doubled = arr1 + arr1
    n = len(arr1)
    for start in range(n):
        if doubled[start:start + n] == arr2:
            return True
    return False

# print(array_rotation_detector([1, 2, 3, 4, 5], [4, 5, 1, 2, 3]))
# print(array_rotation_detector([1, 2, 3], [3, 2, 1]))
# print(array_rotation_detector([], []))
