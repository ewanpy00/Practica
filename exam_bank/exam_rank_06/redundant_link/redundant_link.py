def redundant_link(edges: list[list[int]]) -> list[int]:
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    answer = []
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            answer = [u, v]
        else:
            parent[ru] = rv

    return answer

# print(redundant_link([[1, 2], [1, 3], [2, 3]]))
# print(redundant_link([[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]]))
