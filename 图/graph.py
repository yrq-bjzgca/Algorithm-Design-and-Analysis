graph_dict = {
    "a": ["b", "d"],
    "b": ["a", "c", "d", "f"],
    "c": ["b", "f"],
    "d": ["a", "b", "f"],
    "f": ["b", "c", "d"]
}

matrix = [
    [0, 1, 0, 1, 0, 0],  # a的邻居
    [1, 0, 1, 1, 1, 0],  # b的邻居
    [0, 1, 0, 0, 1, 0],  # c的邻居
    [1, 1, 0, 0, 1, 1],  # d的邻居
    [0, 1, 1, 1, 0, 1],  # e的邻居
    [0, 0, 0, 1, 1, 0]   # f的邻居
]
# 节点顺序: a=0, b=1, c=2, d=3, e=4, f=5

def adj_list_to_matrix(adj_list):
    nodes = list(adj_list.keys())
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)
    matrix = [[0] * n for _ in range(n)]
    
    for node, neighbors in adj_list.items():
        i = node_to_idx[node]
        for neighbor in neighbors:
            j = node_to_idx[neighbor]
            matrix[i][j] = 1
    
    return matrix


# 使用
matrix = adj_list_to_matrix(graph_dict)


def matrix_to_adj_list(matrix, node_names):
    adj_list = {name: [] for name in node_names}
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                adj_list[node_names[i]].append(node_names[j])
    return adj_list

# 使用
node_names = ["a", "b", "c", "d", "e", "f"]
adj_dict = matrix_to_adj_list(matrix, node_names)

