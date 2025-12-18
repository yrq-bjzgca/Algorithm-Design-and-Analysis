from collections import deque

def Topological_Sort_BFS(G):
    """
    使用Kahn算法（BFS版本）实现拓扑排序
    
    参数:
        G: 有向无环图(DAG)的邻接表表示，字典类型
           键为顶点，值为该顶点指向的邻居列表
    
    返回:
        list: 拓扑排序结果列表，顶点按依赖顺序排列
              若图中存在环则返回空列表
    """
    # 初始化入度字典：记录每个顶点的入度（依赖数量）
    in_degree = {vertex: 0 for vertex in G}
    
    # 计算所有顶点的实际入度
    # 遍历图的每条边 (u -> v)，增加v的入度
    for vertex in G:
        for neighbor in G[vertex]:
            # 确保邻居顶点在字典中（处理只有入度没有出度的顶点）
            if neighbor not in in_degree:
                in_degree[neighbor] = 0
            in_degree[neighbor] += 1
    
    # 初始化队列：将所有入度为0的顶点加入队列
    # 这些顶点是没有任何依赖的起点，可以立即处理
    Q = deque()
    for vertex in G:
        if in_degree[vertex] == 0:
            Q.append(vertex)
    
    # 存储拓扑排序的结果
    result = []
    
    # 处理队列：不断取出没有依赖的顶点
    while Q:
        u = Q.popleft()  # 从队列左侧弹出，保证FIFO顺序
        result.append(u)  # 将顶点加入结果列表
        
        # 遍历u的所有邻居顶点v
        # 移除边u->v后，v的入度减1
        for v in G.get(u, []):
            in_degree[v] -= 1
            # 如果v的入度变为0，说明其所有依赖已处理完
            # 可以加入队列进行处理
            if in_degree[v] == 0:
                Q.append(v)
    
    # 检测图中是否存在环
    # 如果结果列表长度小于图中顶点总数，说明有环
    if len(result) != len(in_degree):
        print("警告：图中存在环，无法完成拓扑排序")
        return []
    
    return result


# 示例：穿衣顺序的依赖关系图
# 边表示"必须在...之前"，如"袜子" -> "鞋" 表示先穿袜子再穿鞋
G = {
    "袜子": ["鞋"],          # 袜子必须在鞋之前
    "鞋": [],                # 鞋没有依赖
    "手表": [],              # 手表没有依赖
    "衬衫": ["腰带", "领带"], # 衬衫必须在腰带和领带之前
    "短裤": ["长裤", "鞋"],   # 短裤必须在长裤和鞋之前
    "长裤": ["腰带"],         # 长裤必须在腰带之前
    "腰带": ["外套"],         # 腰带必须在外套之前
    "领带": ["外套"],         # 领带必须在外套之前
    "外套": []               # 外套没有依赖
}

# 执行拓扑排序
sorted_order = Topological_Sort_BFS(G)

# 打印结果
if sorted_order:
    print("拓扑排序结果:", sorted_order)
    print("\n一个有效的穿衣顺序（从头到尾）:")
    for i, item in enumerate(sorted_order, 1):
        print(f"{i}. {item}")