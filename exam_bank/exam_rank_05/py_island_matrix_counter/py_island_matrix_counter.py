def island_matrix_counter(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]:
        return 0

    rows, cols = len(matrix), len(matrix[0])
    visited = [[False] * cols for _ in range(rows)]
    count = 0

    def flood_fill(r, c):
        stack = [(r, c)]
        visited[r][c] = True
        while stack:
            cr, cc = stack.pop()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = cr + dr, cc + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and not visited[nr][nc] and matrix[nr][nc] == "1"):
                    visited[nr][nc] = True
                    stack.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == "1" and not visited[r][c]:
                count += 1
                flood_fill(r, c)

    return count

# print(island_matrix_counter([
#     ["1", "1", "1", "1", "0"],
#     ["1", "1", "1", "0", "0"],
#     ["1", "1", "1", "1", "0"],
#     ["0", "0", "0", "0", "0"],
# ]))
# print(island_matrix_counter([]))
