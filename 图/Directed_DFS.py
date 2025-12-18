def Directed_DFS(G):
    """
    有向图的深度优先搜索(DFS)遍历
    
    参数:
        G: 邻接表表示的有向图，字典类型，键为顶点，值为邻接顶点列表
           例如: {1: [2, 3], 2: [4], 3: [], 4: [1]}
    
    返回:
        pred: 前驱节点数组，记录每个顶点的父节点
        d: 发现时间数组，记录顶点首次被访问的时间戳
        f: 完成时间数组，记录顶点探索完成的时间戳
    """
    # 获取图中所有顶点，确保处理不连续的顶点编号
    all_vertices = set(G.keys()) | {v for neighbors in G.values() for v in neighbors}
    max_vertex = max(all_vertices) if all_vertices else 0
    
    # 初始化访问状态数组（大小为max_vertex+1，支持1-based索引）
    # color: white=未访问, gray=正在访问, black=访问完成
    color = ["white"] * (max_vertex + 1)
    pred = [None] * (max_vertex + 1)      # 前驱节点，用于重构DFS树
    d = [0] * (max_vertex + 1)            # 发现时间（进入时的时间戳）
    f = [0] * (max_vertex + 1)            # 完成时间（结束时的时间戳）
    time = [0]                            # 使用列表实现闭包，便于在递归中修改
    
    # 遍历所有顶点，确保处理非连通图
    for v in range(1, max_vertex + 1):
        if v in G and color[v] == "white":
            # 从每个未访问的顶点启动DFS
            DFS_visit(G, v, color, pred, d, f, time)
    
    return pred, d, f


def DFS_visit(G, v, color, pred, d, f, time):
    """
    DFS递归访问函数
    
    参数:
        G: 图结构
        v: 当前访问的顶点
        color: 访问状态数组
        pred: 前驱节点数组
        d: 发现时间数组
        f: 完成时间数组
        time: 时间戳计数器（使用列表实现引用传递）
    """
    # 标记当前顶点为正在访问（gray）
    color[v] = "gray"
    time[0] += 1
    d[v] = time[0]  # 记录发现时间
    
    # 遍历当前顶点的所有邻接顶点
    for w in G.get(v, []):  # 使用get防止KeyError，处理出度为0的顶点
        if color[w] == "white":
            # 发现未访问的邻接顶点，建立树边
            pred[w] = v
            DFS_visit(G, w, color, pred, d, f, time)
    
    # 当前顶点及其所有后代已探索完成
    color[v] = "black"
    time[0] += 1
    f[v] = time[0]  # 记录完成时间


if __name__ == "__main__":
    # 示例：有向图的邻接表表示
    # 图结构: 1→2, 1→3, 1→4, 2→4, 3→2, 3→5, 4→1, 5无出边
    G = {
        1: [2, 3, 4],
        2: [4],
        3: [2, 5],
        4: [1],
        5: []
    }
    
    # 执行DFS遍历
    pred, d, f = Directed_DFS(G)
    
    # 打印结果
    print("前驱节点:", pred[1:])  # 切片从索引1开始，忽略索引0
    print("发现时间:", d[1:])
    print("完成时间:", f[1:])