from collections import deque

def topological_order(graph):
    reverse_graph = {node: [] for node in graph}

    for node in graph:
        for element in graph[node]:
            reverse_graph[element].append(node)
    
    indegree = {node: 0 for node in graph}
    for node in graph:
        for _ in graph[node]:
            indegree[node] += 1
    
    queue = deque(node for node in graph if indegree[node] == 0)
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for element in reverse_graph[node]:
            indegree[element] -= 1
            if indegree[element] == 0:
                queue.append(element)
    
    if len(result) != len(graph):
        return ""
    
    return result

# graph = {
#     "A": ["B"],
#     "D": [],
#     "B": ["C", "D"],
#     "C": []
# }

# print(topological_order(graph))  