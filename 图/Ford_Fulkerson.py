from collections import defaultdict, deque

def Ford_Fulkerson(G, s, t):
    """
    Ford-Fulkerson算法实现（使用BFS寻找增广路径，即Edmonds-Karp算法）
    
    参数:
        G: 网络的邻接表表示，格式为 {起点: {终点: 容量}}
           例如: {"s": {"v1": 12, "v2": 13}, "v1": {"v3": 10}}
        s: 源点（字符串）
        t: 汇点（字符串）
    
    返回:
        tuple: (max_flow, flow_dict)
               max_flow: 最大流值
               flow_dict: 字典，键为(起点, 终点)，值为当前流量
    """
    # 获取所有顶点
    vertices = set(G.keys())
    for neighbors in G.values():
        vertices.update(neighbors.keys())
    
    # 初始化流量字典：每条边的流量初始为0
    # flow[(u, v)] 表示边u->v的当前流量
    flow = defaultdict(int)
    
    # 主循环：不断寻找增广路径
    while True:
        # 使用BFS寻找从s到t的增广路径
        # parent字典记录路径：parent[v] = (u, residual_capacity)
        parent = {}
        queue = deque([s])
        visited = set([s])
        
        # BFS遍历残差图
        while queue:
            u = queue.popleft()
            
            # 遍历u的所有邻居v
            for v in G.get(u, {}):
                # 计算残差容量 = 容量 - 当前流量
                residual_capacity = G[u][v] - flow[(u, v)]
                
                # 如果残差容量>0且v未被访问
                if residual_capacity > 0 and v not in visited:
                    visited.add(v)
                    parent[v] = (u, residual_capacity)  # 记录前驱和残差容量
                    queue.append(v)
                    
                    if v == t:  # 提前到达汇点，找到增广路径
                        break
            
            # 如果已经找到汇点，退出BFS
            if t in visited:
                break
        
        # **终止条件**：如果汇点t未被访问，说明不存在增广路径
        if t not in visited:
            break
        
        # **计算瓶颈容量**：从t回溯到s，找到路径上的最小残差容量
        path_capacity = float('inf')
        current = t
        while current != s:
            u, cap = parent[current]
            path_capacity = min(path_capacity, cap)
            current = u
        
        # **增广流量**：沿找到的路径增加流量
        current = t
        while current != s:
            u, _ = parent[current]
            flow[(u, current)] += path_capacity  # 正向边增加流量
            # 反向边流量减少（残差网络中，反向边容量=原流量）
            flow[(current, u)] -= path_capacity
            current = u
        
        # 继续下一轮寻找增广路径
    
    # **计算最大流值**：从源点s出发的所有边的流量之和
    max_flow = sum(flow[(s, v)] for v in G.get(s, {}))
    
    return max_flow, flow


def print_network(G, flow_dict=None):
    """
    可视化网络状态
    
    参数:
        G: 网络结构
        flow_dict: 流量字典（可选）
    """
    print("=" * 60)
    print("网络结构")
    print("=" * 60)
    
    if flow_dict:
        print(f"{'边':<10} {'容量':<8} {'流量':<8} {'残差':<8}")
        print("-" * 35)
        for u, neighbors in G.items():
            for v, cap in neighbors.items():
                flow = flow_dict.get((u, v), 0)
                residual = cap - flow
                print(f"{u} -> {v:<4} {cap:<8} {flow:<8} {residual:<8}")
    else:
        print(f"{'边':<10} {'容量':<8}")
        print("-" * 20)
        for u, neighbors in G.items():
            for v, cap in neighbors.items():
                print(f"{u} -> {v:<4} {cap:<8}")


# ==================== 示例：构建网络 G=<V,E,C> ====================

# 网络V：顶点集合
# 网络E：边集合
# 网络C：容量函数

# 示例网络（教材经典例子）
G = {
    "s": {"v1": 12, "v2": 14},  # 源点到v1容量12，到v2容量14
    "v1": {"v3": 10},            # v1到v3容量10
    "v2": {"v1": 5, "v3": 11, "v4": 6},
    "v3": {"v4": 5, "t": 14},
    "v4": {"t": 11},
    "t": {}                      # 汇点没有出边
}

# 打印初始网络
print_network(G)

# 执行最大流算法
max_flow, flow_dict = Ford_Fulkerson(G, "s", "t")

print("\n" + "=" * 60)
print("最大流计算结果")
print("=" * 60)
print(f"最大流值: {max_flow}")
print("\n最终流量分布:")
print_network(G, flow_dict)

# 验证最大流
print("\n" + "=" * 60)
print("流量守恒验证（除s和t）：")
print("=" * 60)
for vertex in G:
    if vertex not in ["s", "t"]:
        # 计算流入流量
        in_flow = sum(flow_dict.get((u, vertex), 0) 
                     for u in G if vertex in G.get(u, {}))
        # 计算流出流量
        out_flow = sum(flow_dict.get((vertex, v), 0) 
                      for v in G.get(vertex, {}))
        print(f"{vertex}: 流入={in_flow}, 流出={out_flow}, 守恒={in_flow==out_flow}")

# 找到最小割
def min_cut(G, flow_dict, s):
    """
    根据最大流后的残差图，找到最小割
    
    参数:
        G: 原网络
        flow_dict: 最大流后的流量
        s: 源点
    
    返回:
        list: 源点所在割集的顶点
    """
    # BFS在残差图中寻找从s可达的顶点
    visited = set([s])
    queue = deque([s])
    
    while queue:
        u = queue.popleft()
        for v in G.get(u, {}):
            # 残差容量 > 0
            residual = G[u][v] - flow_dict.get((u, v), 0)
            if residual > 0 and v not in visited:
                visited.add(v)
                queue.append(v)
    
    return visited

source_side = min_cut(G, flow_dict, "s")
sink_side = set(G.keys()) - source_side

print("\n" + "=" * 60)
print("最小割（Max-Flow Min-Cut定理）：")
print("=" * 60)
print(f"源点侧S: {sorted(source_side)}")
print(f"汇点侧T: {sorted(sink_side)}")
print(f"割边（从S到T的边）：")
cut_edges = []
for u in source_side:
    for v in G.get(u, {}):
        if v in sink_side:
            capacity = G[u][v]
            flow = flow_dict.get((u, v), 0)
            cut_edges.append((u, v, capacity, flow))
            print(f"  {u} -> {v}: 容量={capacity}, 流量={flow}")
cut_capacity = sum(cap for _, _, cap, _ in cut_edges)
print(f"割的容量: {cut_capacity}")
print(f"最大流 = 最小割 = {cut_capacity}")