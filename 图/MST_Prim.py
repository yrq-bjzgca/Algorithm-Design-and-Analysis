import numpy as np
from collections import defaultdict

def MST_Prim(G):
    """
    Prim算法：求无向连通带权图的最小生成树(MST)
    适用于顶点为字符串的图结构
    
    参数:
        G: 图的邻接表表示，字典的字典结构
           外层键是顶点，内层键是邻居顶点，值是边权重
    
    返回:
        tuple: (mst_edges, total_weight)
               mst_edges: MST边的列表，格式为[(起点, 终点, 权重), ...]
               total_weight: 最小生成树的总权重
    """
    if not G:
        return [], 0
    
    # 获取所有顶点
    vertices = list(G.keys())
    if not vertices:
        return [], 0
    
    # 初始化访问状态、距离数组和前驱节点
    # 使用字典结构支持字符串顶点
    color = {v: "white" for v in vertices}  # white=未访问, black=已加入MST
    dist = {v: np.inf for v in vertices}    # 各顶点到当前MST的最短距离
    pred = {v: None for v in vertices}      # 前驱节点
    
    # 任选一个起始顶点
    start = vertices[0]
    dist[start] = 0
    mst_edges = []      # 存储MST的边
    total_weight = 0    # MST的总权重
    
    # 主循环：直到所有顶点都被加入MST
    for _ in range(len(vertices)):
        # 第一步：在还未加入MST的顶点中，选择dist最小的顶点
        min_dist = np.inf
        rec = None  # 记录当前选中的顶点
        
        for v in vertices:
            if color[v] != "black" and dist[v] < min_dist:
                min_dist = dist[v]
                rec = v
        
        # 如果没有找到可达顶点（图不连通）
        if rec is None:
            print("警告：图不连通，无法生成完整的最小生成树")
            break
        
        # 将选中的顶点加入MST
        color[rec] = "black"
        if pred[rec] is not None:
            mst_edges.append((pred[rec], rec, dist[rec]))
            total_weight += dist[rec]
        
        # 第二步：更新rec的所有邻居的距离
        for u in G.get(rec, {}):
            # 如果邻居u还未加入MST，且新边权重更小
            if color[u] != "black" and G[rec][u] < dist[u]:
                dist[u] = G[rec][u]
                pred[u] = rec
    
    return mst_edges, total_weight


# 测试图（无向带权图，注意大小写统一）
G = {
    "a": {"b": 4, "h": 8},
    "b": {"a": 4, "h": 1, "c": 8},
    "c": {"b": 8, "i": 2, "h": 4, "d": 7},  # 修复：统一为"c"小写
    "d": {"c": 7, "f": 14, "z": 9},
    "f": {"g": 2, "c": 4, "d": 14, "z": 10},
    "g": {"h": 1, "i": 4, "f": 2},
    "h": {"a": 8, "b": 1, "i": 7, "g": 1},
    "i": {"c": 2, "h": 7, "g": 4},
    "z": {"d": 9, "f": 10}  # 添加了"z"的出边（双向图）
}

# 执行Prim算法
mst_edges, total_weight = MST_Prim(G)

# 打印结果
print("最小生成树的边:")
for edge in mst_edges:
    print(f"  {edge[0]} - {edge[1]} : 权重 {edge[2]}")

print(f"\n最小生成树总权重: {total_weight}")