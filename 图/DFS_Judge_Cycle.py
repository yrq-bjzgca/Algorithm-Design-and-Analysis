from typing import Dict, List

def DFS_Judge_Cycle(G: Dict[int, List[int]]) -> bool:
    """
    使用深度优先搜索(DFS)判断有向图中是否存在环
    
    参数:
        G: 邻接表表示的有向图，字典类型，键为顶点，值为邻接顶点列表
           例如: {1: [2, 3], 2: [4], 3: [], 4: [1]}
    
    返回:
        bool: 若图中存在环返回True，否则返回False
    """
    # 获取图中所有顶点（包括只有入度没有出度的顶点）
    all_vertices = set(G.keys())
    for neighbors in G.values():
        all_vertices.update(neighbors)
    
    if not all_vertices:
        return False  # 空图无环
    
    max_vertex = max(all_vertices)
    
    # color数组标记顶点访问状态：white=未访问, gray=正在访问, black=访问完成
    color = ["white"] * (max_vertex + 1)
    
    # 对每个未访问的顶点启动DFS（处理非连通图）
    for v in range(1, max_vertex + 1):
        if v in all_vertices and color[v] == "white":
            if DFS_visit_Judge_Cycle(G, v, color):
                return True  # 发现环立即返回
    
    return False  # 所有顶点处理完毕未发现环


def DFS_visit_Judge_Cycle(G: Dict[int, List[int]], v: int, color: List[str]) -> bool:
    """
    DFS递归访问函数，检测从顶点v出发的路径中是否存在环
    
    参数:
        G: 图结构
        v: 当前访问的顶点
        color: 访问状态数组
    
    返回:
        bool: 若从v出发的子图中找到环返回True
    """
    # 标记当前顶点为正在访问（gray）
    # 如果之后在递归过程中再次访问到gray顶点，说明存在回边，即存在环
    color[v] = "gray"
    
    # 遍历当前顶点的所有邻接顶点
    for neighbor in G.get(v, []):  # 使用get避免KeyError
        if color[neighbor] == "gray":
            # 关键检测：发现邻接顶点正在访问中，说明找到了回边
            # 这表示存在一条从neighbor到v的路径，现在又有一条从v到neighbor的边
            # 构成了有向环
            return True
        
        if color[neighbor] == "white":
            # 邻接顶点未访问过，递归深入
            # 如果递归返回True，说明在子图中找到环，向上传播
            if DFS_visit_Judge_Cycle(G, neighbor, color):
                return True
    
    # 当前顶点及其所有后代已探索完成，标记为black
    color[v] = "black"
    return False  # 从当前顶点未找到环


# 测试用例
if __name__ == "__main__":
    # 示例：包含环的有向图 1→2→4→5→3→1（形成环1-2-5-3-1）
    G_with_cycle = {
        1: [2],
        2: [4],
        3: [1],
        4: [5],
        5: [3]
    }
    print("图G是否有环?", DFS_Judge_Cycle(G_with_cycle))  