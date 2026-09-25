def prism_detector(grid: list[str], pattern: str):
    if not grid or not pattern:
        return []

    rows = len(grid)
    cols = len(grid[0])
    plen = len(pattern)

    directions = {
        (1, 0): "H",
        (-1, 0): "H-",
        (0, 1): "V",
        (0, -1): "V-",
        (1, 1): "D1",
        (-1, -1): "D1-",
        (-1, 1): "D2",
        (1, -1): "D2-",
    }

    def matches(x, y, dx, dy):
        for i in range(plen):
            nx, ny = x + dx * i, y + dy * i
            if not (0 <= nx < cols and 0 <= ny < rows):
                return False
            if grid[ny][nx] != pattern[i]:
                return False
        return True

    results = []
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] != pattern[0]:
                continue
            for (dx, dy), code in directions.items():
                if matches(x, y, dx, dy):
                    results.append((x, y, code))

    return results

# print(prism_detector(["CAT", "A..", "T.."], "CAT"))
# print(prism_detector([], "CAT"))
