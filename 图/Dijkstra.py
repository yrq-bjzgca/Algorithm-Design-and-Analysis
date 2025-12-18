import numpy as np
from collections import defaultdict

def Dijkstra(G, source=None):
    """
    Dijkstra算法：单源最短路径
    
    参数:
        G: 带权有向图，邻接表表示，格式为 {顶点: {邻居: 权重}}
        source: 源顶点，默认为图的第一个顶点
    
    返回:
        tuple: (dist, pred)
               dist: 从源点到各顶点的最短距离字典
               pred: 前驱节点字典，用于重构路径
    """
    if not G:
        return {}, {}
    
    # 获取所有顶点
    vertices = list(G.keys())
    if source is None:
        source = vertices[0]
    
    # 初始化
    color = {v: "white" for v in vertices}  # white=未访问, black=已确定最短距离
    pred = {v: None for v in vertices}       # 前驱节点
    dist = {v: np.inf for v in vertices}     # 当前最短距离估计
    dist[source] = 0                         # 源点到自身距离为0
    
    # 主循环：处理所有顶点
    for _ in range(len(vertices)):
        # 第一步：在所有未访问顶点中，选择dist最小的顶点
        rec = None  # 记录当前选中的顶点
        min_dist = np.inf
        
        for v in vertices:
            if color[v] != "black" and dist[v] < min_dist:
                min_dist = dist[v]
                rec = v
        
        # 如果没有可达顶点（图不连通）
        if rec is None or min_dist == np.inf:
            break
        
        # 标记该顶点为已访问（已确定最终最短距离）
        color[rec] = "black"
        
        # 第二步：更新rec的所有邻居的距离
        for u, weight in G.get(rec, {}).items():
            # 如果通过rec到u的路径更短，则更新
            if color[u] != "black" and dist[rec] + weight < dist[u]:
                dist[u] = dist[rec] + weight
                pred[u] = rec
    
    return dist, pred


# 测试图（有向带权图）
G = {
    "s": {"t": 8, "y": 5},
    "t": {"x": 1, "y": 2},
    "x": {"z": 4},
    "y": {"t": 3, "x": 9, "z": 2},
    "z": {"x": 6}
}

# 执行Dijkstra算法，源点为"s"
distances, predecessors = Dijkstra(G, source="s")

# 打印结果
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
def reconstruct_path(pred, source, target):
    """重构从source到target的最短路径"""
    if pred[target] is None and target != source:
        return f"从{source}到{target}没有路径"
    
    path = []
    current = target
    while current is not None:
        path.append(current)
        if current == source:
            break
        current = pred.get(current)
    
    return " -> ".join(reversed(path))

print(f"\n从s到z的最短路径: {reconstruct_path(predecessors, 's', 'z')}")