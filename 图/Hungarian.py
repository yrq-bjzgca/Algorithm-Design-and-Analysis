def Hungarian(G):
    """
    匈牙利算法：求二分图的最大匹配
    
    参数:
        G: 二分图的邻接表表示，格式为 {左部顶点: {右部顶点集合}}
           例如: {"L1": {"R2"}, "L2": {"R1", "R3"}}
    
    返回:
        dict: 右部顶点到左部顶点的匹配字典
              格式: {右部顶点: 匹配的左部顶点}
    """
    # 获取所有左部顶点和右部顶点
    L = list(G.keys())  # 左部顶点列表
    R_set = set()        # 右部顶点集合
    for neighbors in G.values():
        R_set.update(neighbors)
    R = list(R_set)      # 右部顶点列表
    
    # matched: 记录右部顶点匹配的左部顶点
    # matched[r] = l 表示右部顶点r当前匹配左部顶点l
    matched = {r: None for r in R}
    
    # 对每个左部顶点尝试寻找增广路径
    for v in L:
        # color: 记录右部顶点在本次DFS中的访问状态
        color = {r: "white" for r in R}
        
        # 如果找到增广路径，则匹配成功
        if DFS_Find(G, v, color, matched):
            # 匹配成功，继续处理下一个左部顶点
            pass
    
    # 过滤掉未匹配的右部顶点
    return {r: l for r, l in matched.items() if l is not None}


def DFS_Find(G, v, color, matched):
    """
    DFS寻找增广路径
    
    参数:
        G: 二分图
        v: 当前访问的左部顶点
        color: 右部顶点的访问状态字典
        matched: 匹配字典，记录右部顶点匹配了哪个左部顶点
    
    返回:
        bool: 是否找到增广路径
    """
    # 遍历左部顶点v的所有右部邻居u
    for u in G.get(v, set()):
        # 如果右部顶点u已访问过，跳过（避免环路）
        if color[u] == "black":
            continue
        
        # 标记右部顶点u为已访问
        color[u] = "black"
        
        # 如果u是空闲的（未匹配），或者可以让给matched[u]（当前匹配u的左部顶点）
        # 并且matched[u]能找到其他匹配
        if matched[u] is None or DFS_Find(G, matched[u], color, matched):
            # 将u匹配给v
            matched[u] = v
            return True
    
    # 所有邻居都无法匹配，返回False
    return False


# ==================== 测试示例 ====================

# 二分图 G = <L, R, E>
# L: 左部顶点（工人）
# R: 右部顶点（任务）
G = {
    "L1": {"R2"},           # L1可以完成R2
    "L2": {"R1", "R3", "R5"},  # L2可以完成R1,R3,R5
    "L3": {"R1", "R4"},        # L3可以完成R1,R4
    "L4": {"R3"},              # L4可以完成R3
    "L5": {"R4"},              # L5可以完成R4
}

print("二分图结构:")
for left, rights in G.items():
    print(f"  {left} -> {rights}")

# 执行匈牙利算法
matching = Hungarian(G)

print("\n最大匹配结果:")
print("左部顶点 -> 右部顶点")
for right, left in matching.items():
    print(f"  {left} -> {right}")

print(f"\n最大匹配数: {len(matching)}")

# 验证最大匹配
expected_matching = 4  # 理论上最多4条匹配边
print(f"预期最大匹配数: {expected_matching}")
print(f"结果正确: {len(matching) == expected_matching}")

# 可视化匹配关系
print("\n匹配可视化:")
for left in sorted(G.keys()):
    matched_right = None
    for right, matched_left in matching.items():
        if matched_left == left:
            matched_right = right
            break
    if matched_right:
        print(f"✓ {left} 匹配 {matched_right}")
    else:
        print(f"✗ {left} 未匹配")

print("\n未匹配的右部顶点:")
all_right = set()
for neighbors in G.values():
    all_right.update(neighbors)
matched_right = set(matching.keys())
unmatched_right = all_right - matched_right
if unmatched_right:
    for r in sorted(unmatched_right):
        print(f"  - {r}")
else:
    print("  所有右部顶点都已匹配")