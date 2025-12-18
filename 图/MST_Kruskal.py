from collections import defaultdict

class UnionFind:
    """并查集数据结构"""
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}
    
    def find(self, x):
        """查找根节点，带路径压缩"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """合并两个集合"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # 已经在同一集合，形成环
        
        # 按秩合并
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return True  # 成功合并

def MST_Kruskal(G):
    """
    Kruskal算法：求最小生成树
    
    参数:
        G: 无向带权图的邻接表表示
    
    返回:
        tuple: (mst_edges, total_weight)
    """
    # 1. 获取所有边并排序
    edges = sort_edges_by_weight(G)
    
    # 2. 初始化并查集和结果
    uf = UnionFind(G.keys())
    mst_edges = []
    total_weight = 0
    
    # 3. 遍历排序后的边
    for weight, u, v in edges:
        # 如果u和v不在同一连通分量（不形成环）
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
    
    return mst_edges, total_weight

def sort_edges_by_weight(G):
    """按权重升序排列所有边"""
    edges = []
    seen = set()
    
    for u in G:
        for v, weight in G[u].items():
            edge_key = tuple(sorted([u, v]))
            if edge_key not in seen:
                seen.add(edge_key)
                edges.append((weight, u, v))
    
    edges.sort(key=lambda x: x[0])
    return edges

# 测试图
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

# 执行Kruskal算法
mst_edges, total_weight = MST_Kruskal(G)

# 打印结果
print("最小生成树的边:")
for edge in mst_edges:
    print(f"  {edge[0]} - {edge[1]} : 权重 {edge[2]}")

print(f"\n最小生成树总权重: {total_weight}")