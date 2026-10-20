def constellation_mapper(stars: list[tuple[int, int]], dim: int) -> list[str]:
    grid = [["."] * dim for _ in range(dim)]

    for row, col in stars:
        if 0 <= row < dim and 0 <= col < dim:
            grid[row][col] = "*"

    return ["".join(line) for line in grid]

# print(constellation_mapper([(0, 0), (1, 1), (2, 2)], 3))
# print(constellation_mapper([(0, 0), (5, 5)], 3))
