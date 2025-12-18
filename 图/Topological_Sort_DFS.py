def Topological_Sort_DFS(G):
    """
    基于DFS的拓扑排序算法
    
    参数:
        G: 有向无环图(DAG)的邻接表表示，字典类型
           键为顶点(字符串)，值为该顶点指向的邻居列表
           例如: {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
    
    返回:
        list: 拓扑排序结果，顶点按依赖顺序排列
              若图中存在环，则可能无法生成完全正确的拓扑序
    """
    # 初始化访问状态字典: white=未访问, gray=正在访问, black=访问完成
    color = {vertex: "white" for vertex in G}
    
    # 存储拓扑排序结果
    L = []
    
    # 遍历图中所有顶点
    for vertex in G:
        if color[vertex] == "white":
            # 从每个未访问的顶点启动DFS
            DFS_visit(G, vertex, color, L)
    
    # 返回拓扑排序结果（已完成后序遍历的顶点列表）
    return L


def DFS_visit(G, v, color, L):
    """
    DFS访问函数，采用后序遍历收集顶点
    
    参数:
        G: 图结构
        v: 当前访问的顶点
        color: 访问状态字典
        L: 拓扑排序结果列表（引用传递）
    """
    # 标记当前顶点为正在访问（gray），用于环检测
    color[v] = "gray"
    
    # 遍历当前顶点的所有邻居
    for w in G[v]:
        if color[w] == "white":
            # 递归访问未访问的邻居
            DFS_visit(G, w, color, L)
        elif color[w] == "gray":
            # 如果遇到正在访问的节点，说明存在环（拓扑排序不适用）
            # 在实际应用中应抛出异常或处理该情况
            raise ValueError(f"图中存在环，检测到反向边: {v} -> {w}")
    
    # 当前顶点及其所有后代已探索完成，标记为black
    color[v] = "black"
    
    # 将顶点加入结果列表（后序遍历: 先处理完所有依赖再添加自己）
    # 这保证了依赖项总在当前顶点之前
    L.append(v)


# 示例：穿衣顺序的依赖关系图
# 边表示"必须在...之前穿"，如"袜子" -> "鞋" 表示必须先穿袜子再穿鞋
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

try:
    # 执行拓扑排序
    result = Topological_Sort_DFS(G)
    
    # 打印结果（从后往前读更符合依赖关系）
    print("拓扑排序结果（逆序）:", result)
    print("正确穿衣顺序（从头到尾）:", list(reversed(result)))
except ValueError as e:
    print("错误:", e)