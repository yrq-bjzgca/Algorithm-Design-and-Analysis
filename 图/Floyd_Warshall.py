import numpy as np
from collections import defaultdict

def Floyd_Warshall(G):
    """
    Floyd-Warshall算法：计算所有顶点对之间的最短路径
    
    参数:
        G: 带权有向图的邻接表表示，格式为 {顶点: {邻居: 权重}}
    
    返回:
        tuple: (D, Rec, index_to_vertex)
               D: 最短距离矩阵
               Rec: 路径重构矩阵
               index_to_vertex: 索引到顶点的映射
    """
    # 获取所有顶点并排序
    vertices = sorted(set(G.keys()) | {v for neighbors in G.values() for v in neighbors})
    n = len(vertices)
    
    # 创建顶点索引映射：顶点 -> 索引
    vertex_to_index = {v: i for i, v in enumerate(vertices)}
    index_to_vertex = {i: v for i, v in enumerate(vertices)}
    
    # 初始化距离矩阵D和路径重构矩阵Rec
    D = np.full((n, n), np.inf)  # 初始化为无穷大
    Rec = np.zeros((n, n), dtype=int)  # 记录中间顶点
    
    # 初始化：设置直接边的距离
    for i, u in enumerate(vertices):
        D[i][i] = 0  # 顶点到自身距离为0
        for v, weight in G.get(u, {}).items():
            j = vertex_to_index[v]
            D[i][j] = weight
    
    # Floyd-Warshall核心算法
    # k为中间顶点
    for k in range(n):
        for i in range(n):
            for j in range(n):
                # 如果通过k的路径更短，则更新
                if D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]
                    Rec[i][j] = k + 1  # 记录中间顶点（1-indexed便于阅读）
    
    # 检查负环：如果对角线有负值，说明存在负权环
    for i in range(n):
        if D[i][i] < 0:
            print(f"警告：图中存在负权环，顶点{index_to_vertex[i]}在一个负环中")
    
    return D, Rec, index_to_vertex


def Find_Path(Rec, index_to_vertex, u_idx, v_idx):
    """
    递归查找并打印从u到v的路径
    
    参数:
        Rec: 路径重构矩阵
        index_to_vertex: 索引到顶点的映射
        u_idx: 起点索引
        v_idx: 终点索引
    """
    # 如果存在中间顶点k
    if Rec[u_idx][v_idx] != 0:
        k_idx = Rec[u_idx][v_idx] - 1  # 转回0-indexed
        # 递归打印u到k的路径
        Find_Path(Rec, index_to_vertex, u_idx, k_idx)
        # 打印k到v的路径
        Find_Path(Rec, index_to_vertex, k_idx, v_idx)
    else:
        # 没有中间顶点，直接打印终点
        v = index_to_vertex[v_idx]
        print(f" -> {v}", end="")


def print_shortest_paths(G):
    """
    计算并打印所有顶点对之间的最短路径和距离
    """
    D, Rec, idx_to_v = Floyd_Warshall(G)
    vertices = sorted(set(G.keys()) | {v for neighbors in G.values() for v in neighbors})
    n = len(vertices)
    
    print("=" * 60)
    print("所有顶点对之间的最短距离矩阵:")
    print("=" * 60)
    
    # 打印表头
    print(f"{'':4}", end="")
    for v in vertices:
        print(f"{v:>6}", end="")
    print()
    
    # 打印距离矩阵
    for i, u in enumerate(vertices):
        print(f"{u:>4}", end="")
        for j, v in enumerate(vertices):
            if D[i][j] == np.inf:
                print(f"{'∞':>6}", end="")
            else:
                print(f"{D[i][j]:>6.1f}", end="")
        print()
    
    print("\n" + "=" * 60)
    print("路径重构示例:")
    print("=" * 60)
    
    # 示例：打印从第一个顶点到第四个顶点的路径
    if n >= 4:
        start = vertices[0]
        end = vertices[3]
        
        print(f"\n从{start}到{end}的最短路径:")
        print(f"{start}", end="")
        Find_Path(Rec, idx_to_v, 0, 3)
        print(f"\n总距离: {D[0][3]:.1f}")
    
    # 打印从源点到所有其他点的路径
    print(f"\n从{vertices[0]}到所有其他顶点的路径:")
    for j, v in enumerate(vertices[1:], 1):
        print(f"\n到 {v}:", end="")
        print(f" {vertices[0]}", end="")
        Find_Path(Rec, idx_to_v, 0, j)
        print(f" (距离: {D[0][j]:.1f})")


# 测试图（带权有向图）
G = {
    1: {2: 200, 3: 100, 4: 500, 5: 500},
    2: {1: 200, 3: 200, 4: 1200, 5: 1000},
    3: {1: 100, 2: 200, 4: 200, 5: 600},
    4: {1: 500, 2: 1200, 3: 200, 5: 100},
    5: {1: 500, 2: 1000, 3: 600, 4: 100},
}

# 计算并打印所有最短路径
print_shortest_paths(G)