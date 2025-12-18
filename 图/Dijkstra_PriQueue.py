import heapq
import numpy as np
from collections import defaultdict

def Dijkstra_PriQueue(G, source):
    """
    Dijkstra算法：使用优先队列优化的单源最短路径
    
    参数:
        G: 带权有向图，邻接表表示，格式为 {顶点: {邻居: 权重}}
        source: 源顶点
    
    返回:
        tuple: (dist, pred)
               dist: 从源点到各顶点的最短距离字典
               pred: 前驱节点字典，用于重构路径
    """
    if not G or source not in G:
        return {}, {}
    
    # 获取所有顶点（包括只有入边的顶点）
    all_vertices = set(G.keys())
    for neighbors in G.values():
        all_vertices.update(neighbors.keys())
    
    # 初始化
    color = {v: "white" for v in all_vertices}  # white=未访问, black=已确定最短距离
    pred = {v: None for v in all_vertices}       # 前驱节点
    dist = {v: np.inf for v in all_vertices}     # 当前最短距离估计
    dist[source] = 0                             # 源点到自身距离为0
    
    # 优先队列：(当前距离, 顶点)，按距离排序
    pq = [(0, source)]
    
    # 主循环
    while pq:
        current_dist, v = heapq.heappop(pq)
        
        # 如果该顶点已处理过，跳过（避免重复处理）
        if color[v] == "black":
            continue
        
        # 标记为已访问（最短距离已确定）
        color[v] = "black"
        
        # 遍历v的所有邻居
        for u, weight in G.get(v, {}).items():
            # 如果找到更短的路径，则更新
            if color[u] != "black" and dist[v] + weight < dist[u]:
                dist[u] = dist[v] + weight
                pred[u] = v
                # 将邻居加入优先队列
                heapq.heappush(pq, (dist[u], u))
    
    return dist, pred


def reconstruct_path(pred, source, target):
    """
    重构从source到target的最短路径
    
    参数:
        pred: 前驱节点字典
        source: 源顶点
        target: 目标顶点
    
    返回:
        str: 路径字符串或错误信息
    """
    if pred.get(target) is None and target != source:
        return f"从{source}到{target}没有路径"
    
    path = []
    current = target
    while current is not None:
        path.append(current)
        if current == source:
            break
        current = pred.get(current)
    
    if path[-1] != source:
        return f"从{source}到{target}没有完整路径"
    
    return " -> ".join(reversed(path))


# 测试图（有向带权图）
G = {
    "s": {"t": 8, "y": 5},
    "t": {"x": 1, "y": 2},
    "x": {"z": 4},
    "y": {"t": 3, "x": 9, "z": 2},
    "z": {"x": 6}
}

# 执行Dijkstra算法，源点为"s"
distances, predecessors = Dijkstra_PriQueue(G, source="s")

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

# 示例：重构从s到x的最短路径
print(f"\n从s到x的最短路径: {reconstruct_path(predecessors, 's', 'x')}")
print(f"从s到z的最短路径: {reconstruct_path(predecessors, 's', 'z')}")

# 验证算法正确性：检查s到x的路径
# 预期：s(0) -> y(5) -> t(5+3=8) -> x(8+1=9)
# 实际输出应为9
assert abs(distances['x'] - 9) < 0.001, "s到x的距离应为9"