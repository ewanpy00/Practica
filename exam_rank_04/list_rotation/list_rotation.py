def list_rotation(l1, l2):
    if len(l1) != len(l2):
        return False

    ls1 = "," + ",".join(map(str, l1)) + ","
    ls2 = "," + ",".join(map(str, l2 + l2)) + ","

    return ls1 in ls2

print(list_rotation([3, 4, 5, 1, 2], [1, 2, 3, 4, 5]))
print(list_rotation([1, 2, 3], [1, 2, 3]))
print(list_rotation([2, 1, 3], [1, 2, 3]))
print(list_rotation([1, 2], [1, 2, 3]))
