def py_graph_cycle_detector(graph: dict[int, list[int]]) -> bool:
    if not graph:
        return False

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}

    def dfs(node):
        color[node] = GRAY
        for neighbor in graph.get(node, []):
            if neighbor not in color:
                color[neighbor] = WHITE
            if color[neighbor] == GRAY:
                return True
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        color[node] = BLACK
        return False

    for node in list(graph):
        if color[node] == WHITE:
            if dfs(node):
                return True
    return False

# print(py_graph_cycle_detector({0: [1], 1: [2], 2: [0]}))
# print(py_graph_cycle_detector({0: [1], 1: [2], 2: []}))
# print(py_graph_cycle_detector({}))
