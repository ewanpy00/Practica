def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
    return [row[::-1] for row in matrix]

print(mirror_matrix([[1, 2, 3], [4, 5, 6]]))
print(mirror_matrix([[1, 2], [3, 4], [5, 6]]))
