import sys
import heapq
import pandas as pd

def adjacency_matrix(vertices, edges):
    n = len(vertices)
    vertex_index = {v: i for i, v in enumerate(vertices)}
    adj_matrix = [[float('inf')] * n for _ in range(n)]

    for i in range(n):
        adj_matrix[i][i] = 0

    for (u, v), weight in edges.items():
        u_idx, v_idx = vertex_index[u], vertex_index[v]
        adj_matrix[u_idx][v_idx] = weight
        adj_matrix[v_idx][u_idx] = weight

    return adj_matrix, vertex_index

def dijkstra(adj_matrix, vertex_index, source, target):
    n = len(adj_matrix)
    dist = [float('inf')] * n
    prev = [None] * n
    source_idx = vertex_index[source]
    target_idx = vertex_index[target]
    dist[source_idx] = 0
    pq = [(0, source_idx)]

    while pq:
        current_dist, current_vertex = heapq.heappop(pq)
        if current_vertex == target_idx:
            break

        if current_dist > dist[current_vertex]:
            continue

        for neighbor in range(n):
            weight = adj_matrix[current_vertex][neighbor]
            if weight < float('inf'):
                distance = current_dist + weight
                if distance < dist[neighbor]:
                    dist[neighbor] = distance
                    prev[neighbor] = current_vertex
                    heapq.heappush(pq, (distance, neighbor))

    path = []
    at = target_idx
    while at is not None:
        path.append(at)
        at = prev[at]
    path.reverse()

    idx_to_vertex = {i: v for v, i in vertex_index.items()}
    path = [idx_to_vertex[i] for i in path]

    return path, dist[target_idx]

vertices = ["A", "B", "C", "D", "E", "F", "G", "H", "L", "M"]

edges = {
    ("A", "B"): 4, ("A", "C"): 1, ("B", "F"): 3, ("C", "D"): 8,
    ("C", "F"): 7, ("D", "H"): 5, ("E", "F"): 1, ("E", "H"): 2,
    ("E", "L"): 2, ("F", "H"): 1, ("H", "G"): 3, ("H", "M"): 7,
    ("H", "L"): 6, ("G", "M"): 4, ("G", "L"): 4, ("L", "M"): 1
}

adj_matrix, vertex_index = adjacency_matrix(vertices, edges)
matrix = pd.DataFrame(adj_matrix, index=vertices, columns=vertices)

print("Adjacency Matrix:")
print(matrix)

print("\nVertices:", vertices)
source = input("Enter source vertex: ").strip().upper()
target = input("Enter target vertex: ").strip().upper()

if source not in vertex_index or target not in vertex_index:
    print("Invalid source or target vertex.")
    sys.exit(1)

path, total_weight = dijkstra(adj_matrix, vertex_index, source, target)

if total_weight == float('inf'):
    print(f"No path found from {source} to {target}.")
else:
    print(f"Shortest path from {source} to {target}: {' -> '.join(path)}")
    print(f"Total weight: {total_weight}")