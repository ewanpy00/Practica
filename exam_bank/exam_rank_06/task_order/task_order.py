def task_order(n: int, prereqs: list[list[int]]) -> list[int]:
    pending = [0] * n
    unlocks = [[] for _ in range(n)]

    for a, b in prereqs:
        pending[a] += 1
        unlocks[b].append(a)

    ready = [i for i in range(n) if pending[i] == 0]
    order = []

    while ready:
        ready.sort()
        task = ready.pop(0)
        order.append(task)
        for nxt in unlocks[task]:
            pending[nxt] -= 1
            if pending[nxt] == 0:
                ready.append(nxt)

    return order if len(order) == n else []

# print(task_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))
# print(task_order(2, [[0, 1], [1, 0]]))
