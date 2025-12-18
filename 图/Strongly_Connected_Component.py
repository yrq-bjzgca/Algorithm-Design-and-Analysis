from collections import defaultdict

def Strongly_Connected_Component(G):
    """
    Kosaraju算法：计算有向图的强连通分量(SCC)
    
    参数:
        G: 有向图的邻接表表示，字典类型
           键为顶点，值为该顶点指向的邻居列表
    
    返回:
        list: 强连通分量列表，每个分量是一个顶点集合
    """
    # 第一步：对原图G进行DFS，获取顶点的完成时间顺序
    visited = set()
    finish_order = []  # 按完成时间排序的顶点列表（后序遍历）
    
    def dfs_first(v):
        """第一次DFS：计算完成时间"""
        visited.add(v)
        for w in G.get(v, []):
            if w not in visited:
                dfs_first(w)
        # 顶点探索完成后，将其加入列表（后序遍历）
        finish_order.append(v)
    
    # 遍历所有顶点
    for vertex in G:
        if vertex not in visited:
            dfs_first(vertex)
    
    # 第二步：构建反向图GR
    GR = defaultdict(list)
    for u in G:
        for v in G[u]:
            GR[v].append(u)  # 将边u->v反转为v->u
    
    # 第三步：按完成时间逆序对反向图进行DFS
    visited.clear()
    scc_components = []  # 存储所有强连通分量
    
    def dfs_second(v, component):
        """第二次DFS：在反向图中探索SCC"""
        visited.add(v)
        component.append(v)
        for w in GR.get(v, []):
            if w not in visited:
                dfs_second(w, component)
    
    # 按照完成时间的逆序遍历顶点
    for vertex in reversed(finish_order):
        if vertex not in visited:
            component = []
            dfs_second(vertex, component)
            scc_components.append(component)
    
    return scc_components


def DFS(G):
    """
    辅助函数：返回按完成时间排序的顶点列表
    （用于Kosaraju算法的第一步）
    """
    visited = set()
    finish_order = []
    
    def dfs_visit(v):
        visited.add(v)
        for w in G.get(v, []):
            if w not in visited:
                dfs_visit(w)
        finish_order.append(v)
    
    for vertex in G:
        if vertex not in visited:
            dfs_visit(vertex)
    
    return finish_order


# 示例图：包含多个强连通分量
# 1,10,3,4构成一个SCC；2,5,6构成一个SCC；7自成一个SCC；8,9构成一个SCC
G = {
    1: [10, 3],
    2: [6],
    3: [4, 7],
    4: [1, 6],
    5: [2],
    6: [5],
    7: [7],
    8: [9, 10],
    9: [7, 8],
    10: [1]
}

# 计算并打印强连通分量
scc_list = Strongly_Connected_Component(G)
print(f"图中共有 {len(scc_list)} 个强连通分量:")
for i, component in enumerate(scc_list, 1):
    print(f"SCC {i}: {component}")