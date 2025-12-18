import numpy as np

def Bellman_Ford(G, s):
    """
    Bellman-Ford算法：单源最短路径算法，支持负权边，能检测负环
    
    参数:
        G: 带权有向图，邻接表表示，格式为 {顶点: {邻居: 权重}}
        s: 源顶点
    
    返回:
        tuple: (dist, pred)
               dist: 从源点到各顶点的最短距离字典
               pred: 前驱节点字典，用于重构路径
               如果检测到负环，返回 (None, None)
    """
    if s not in G:
        return {}, {}
    
    # 获取所有顶点（包括只有入边的顶点）
    vertices = set(G.keys())
    for neighbors in G.values():
        vertices.update(neighbors.keys())
    
    # 初始化距离和前驱
    dist = {v: np.inf for v in vertices}  # 到各顶点的最短距离
    pred = {v: None for v in vertices}    # 前驱节点
    dist[s] = 0                           # 源点到自身距离为0
    
    # 提取所有边，格式为(起点, 终点, 权重)
    edges = []
    for u in G:
        for v, weight in G[u].items():
            edges.append((u, v, weight))
    
    # 主循环：对所有边进行 |V|-1 次松弛操作
    # 原理：每次松弛都会使某些顶点的最短距离变得更优
    # 进行 |V|-1 次可以确保所有顶点的最短距离最终确定
    for _ in range(len(vertices) - 1):
        # 遍历每条边 (u, v)
        for u, v, weight in edges:
            # 如果通过u到v的路径更短，则更新dist和pred
            # 这就是松弛操作的核心
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                pred[v] = u
    
    # 负环检测：再进行一次遍历
    # 如果还能松弛，说明存在负权环
    for u, v, weight in edges:
        if dist[u] + weight < dist[v]:
            print(f"检测到负权环：从{u}到{v}可以进一步优化")
            return None, None  # 返回None表示存在负环
    
    return dist, pred


def reconstruct_path(pred, s, t):
    """
    重构从s到t的最短路径
    
    参数:
        pred: 前驱节点字典
        s: 源顶点
        t: 目标顶点
    
    返回:
        str: 路径字符串
    """
    if pred is None or t not in pred:
        return "无法重构路径（可能检测到负环）"
    
    if pred[t] is None and t != s:
        return f"从{s}到{t}不存在路径"
    
    path = []
    current = t
    # 从目标回溯到源点
    while current is not None:
        path.append(current)
        if current == s:
            break
        current = pred.get(current)
    
    # 如果无法回溯到源点，说明没有路径
    if path[-1] != s:
        return f"从{s}到{t}没有完整路径"
    
    return " -> ".join(reversed(path))


# 测试图（有向带权图）
G = {
    "s": {"t": 8, "y": 5},
    "t": {"x": 1, "y": 2},
    "x": {"z": 4},
    "y": {"t": 3, "x": 9, "z": 2},
    "z": {"x": 6}
}

# 执行Bellman-Ford算法，源点为"s"
distances, predecessors = Bellman_Ford(G, s="s")

# 打印结果
if distances is not None:
    print("从源点's'出发的最短距离:")
    for vertex in sorted(G.keys()):
        print(f"  到 {vertex}: 距离 = {distances[vertex]}")
    
    print("\n前驱节点（用于重构路径）:")
    for vertex in sorted(G.keys()):
        if predecessors[vertex] is not None:
            print(f"  {vertex} <- {predecessors[vertex]}")
        else:
            print(f"  {vertex} <- None (源点)")
    
    # 示例：重构从s到z的路径
    print(f"\n从s到z的最短路径: {reconstruct_path(predecessors, 's', 'z')}")
else:
    print("算法检测到图中存在负权环")