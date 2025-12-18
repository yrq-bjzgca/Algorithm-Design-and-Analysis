import numpy as np
import heapq
from collections import defaultdict

def MST_Prim_PriQueue(G):
    """
    Prim算法：使用优先队列（最小堆）实现的最小生成树算法
    
    参数:
        G: 无向带权图的邻接表表示，字典的字典结构
           外层键是顶点，内层键是邻居顶点，值是边权重
    
    返回:
        tuple: (mst_edges, total_weight)
               mst_edges: MST边的列表，格式为(起点, 终点, 权重)
               total_weight: 最小生成树的总权重
    """
    if not G:
        return [], 0
    
    # 获取所有顶点
    vertices = list(G.keys())
    if not vertices:
        return [], 0
    
    # 初始化访问状态、距离数组和前驱节点
    color = {v: "white" for v in vertices}  # white=未访问, black=已加入MST
    dist = {v: np.inf for v in vertices}    # 各顶点到当前MST的最短距离
    pred = {v: None for v in vertices}      # 前驱节点
    
    # 任选一个起始顶点
    start = vertices[0]
    dist[start] = 0
    
    # 优先队列：(距离, 顶点)，按照距离排序
    # Python的heapq实现的是最小堆
    pq = [(0, start)]  # (当前顶点加入MST所需的最小边权重, 顶点)
    
    mst_edges = []      # 存储MST的边
    total_weight = 0    # MST的总权重
    
    # 主循环：直到所有顶点都被加入MST
    while pq:
        # 弹出距离最小的顶点
        current_dist, v = heapq.heappop(pq)
        
        # 如果该顶点已处理过，跳过（避免重复入队）
        if color[v] == "black":
            continue
        
        # 将顶点加入MST
        color[v] = "black"
        if pred[v] is not None:
            mst_edges.append((pred[v], v, current_dist))
            total_weight += current_dist
        
        # 更新v的所有邻居的距离
        for u, weight in G.get(v, {}).items():
            # 如果邻居未访问且新边权重更小
            if color[u] == "white" and weight < dist[u]:
                dist[u] = weight
                pred[u] = v
                # 将邻居加入优先队列
                heapq.heappush(pq, (weight, u))
    
    # 检查图是否连通
    if len([v for v in vertices if color[v] == "black"]) != len(vertices):
        print("警告：图不连通，无法生成完整的最小生成树")
    
    return mst_edges, total_weight


# 测试图（无向带权图，注意大小写统一）
G = {
    "a": {"b": 4, "h": 8},
    "b": {"a": 4, "h": 1, "c": 8},
    "c": {"b": 8, "i": 2, "h": 4, "d": 7},
    "d": {"c": 7, "f": 14, "z": 9},
    "f": {"g": 2, "c": 4, "d": 14, "z": 10},
    "g": {"h": 1, "i": 4, "f": 2},
    "h": {"a": 8, "b": 1, "i": 7, "g": 1},
    "i": {"c": 2, "h": 7, "g": 4},
    "z": {"d": 9, "f": 10}
}

# 执行Prim算法
mst_edges, total_weight = MST_Prim_PriQueue(G)

# 打印结果
print("最小生成树的边:")
for edge in mst_edges:
    print(f"  {edge[0]} - {edge[1]} : 权重 {edge[2]}")

print(f"\n最小生成树总权重: {total_weight}")