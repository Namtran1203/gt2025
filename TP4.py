import heapq

def create_weighted_adjacency_matrix():
    size = 9
    adj_matrix = [[0] * size for _ in range(size)]
    edges = [
        (1, 2, 4), (1, 5, 1), (1, 7, 2),
        (2, 3, 7), (2, 6, 5),
        (3, 4, 1), (3, 6, 8),
        (4, 6, 6), (4, 7, 4), (4, 8, 3),
        (5, 6, 9), (5, 7, 10),
        (6, 9, 2),
        (7, 9, 8),
        (8, 9, 1),
        (9, 8, 7)
    ]
    for u, v, w in edges:
        adj_matrix[u - 1][v - 1] = w
        adj_matrix[v - 1][u - 1] = w  
    return adj_matrix

def print_adjacency_matrix(adj_matrix):
    print("Weighted Adjacency Matrix:")
    for row in adj_matrix:
        print(" ".join(f"{cell:2}" for cell in row))

def prim(adj_matrix, root):
    n = len(adj_matrix)
    visited = [False] * n
    min_heap = [(0, root, root)]
    mst_edges = []
    total_weight = 0

    while min_heap:
        weight, from_node, to_node = heapq.heappop(min_heap)
        if visited[to_node]:
            continue
        visited[to_node] = True
        if from_node != to_node:
            mst_edges.append((from_node + 1, to_node + 1, weight))
            total_weight += weight
        for neighbor in range(n):
            if adj_matrix[to_node][neighbor] != 0 and not visited[neighbor]:
                heapq.heappush(min_heap, (adj_matrix[to_node][neighbor], to_node, neighbor))

    return mst_edges, total_weight

def kruskal(adj_matrix):
    edges = []
    n = len(adj_matrix)
    
    for i in range(n):
        for j in range(i + 1, n):
            if adj_matrix[i][j] != 0:
                edges.append((adj_matrix[i][j], i, j))
    edges.sort()

    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            if rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            elif rank[root_x] < rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_y] = root_x
                rank[root_x] += 1

    mst_edges = []
    total_weight = 0

    for weight, u, v in edges:
        if find(u) != find(v):
            union(u, v)
            mst_edges.append((u + 1, v + 1, weight))
            total_weight += weight

    return mst_edges, total_weight

if __name__ == "__main__":
    adj_matrix = create_weighted_adjacency_matrix()
    print_adjacency_matrix(adj_matrix)
    
    root_node = int(input("\nEnter the root node for Prim's algorithm (1-9): ")) - 1

    prim_mst, prim_weight = prim(adj_matrix, root_node)
    print("\nFor Prim's Algorithm, there is minimum spanning tree:")
    for edge in prim_mst:
        print(f"Edge {edge[0]}-{edge[1]} with weight {edge[2]}")
    print(f"Total Weight of MST (Prim's): {prim_weight}")

    kruskal_mst, kruskal_weight = kruskal(adj_matrix)
    print("\nFor Kruskal's Algorithm, there is minimum spanning tree:")
    for edge in kruskal_mst:
        print(f"Edge {edge[0]}-{edge[1]} with weight {edge[2]}")
    print(f"Total Weight of MST (Kruskal's): {kruskal_weight}")
