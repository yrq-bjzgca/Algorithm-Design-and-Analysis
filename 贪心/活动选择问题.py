class Activity:
    """
    活动类：包装区间和名称，便于排序和输出
    """
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f"{self.name}: [{self.start}, {self.end}]"


def greedy_activity_selector(S):
    """
    活动选择问题贪心算法（不带权重）
    目标：选择最多数量的互不冲突活动
    
    参数:
        S: 字典，键为活动名，值为[开始时间, 结束时间]
    
    返回:
        selected_names: 被选中的活动名称列表
        selected_intervals: 被选中的活动区间列表
    """
    
    # ------------------------------------------------------------------
    # 阶段1: 从字典中提取所有活动并转换为对象列表
    # ------------------------------------------------------------------
    # 将字典转为Activity对象列表，保留名称信息以便后续输出
    activities = [Activity(name, interval[0], interval[1]) 
                  for name, interval in S.items()]
    
    # ------------------------------------------------------------------
    # 阶段2: 按结束时间排序（贪心策略核心）
    # ------------------------------------------------------------------
    # 为什么按结束时间排序？优先选择结束早的活动，给后续活动留出更多时间
    activities.sort(key=lambda act: act.end)
    
    # ------------------------------------------------------------------
    # 阶段3: 贪心选择过程
    # ------------------------------------------------------------------
    selected_names = []      # 存储选中的活动名称
    selected_intervals = []  # 存储选中的活动区间
    last_end_time = -1       # 上一个选中活动的结束时间（初始化为负无穷）
    
    # 遍历所有已排序的活动
    for act in activities:
        # 如果当前活动的开始时间 >= 上一个活动的结束时间
        # 说明这两个活动不冲突（兼容）
        if act.start >= last_end_time:
            selected_names.append(act.name)        # 记录活动名
            selected_intervals.append([act.start, act.end])  # 记录区间
            last_end_time = act.end               # 更新结束时间
    
    # ------------------------------------------------------------------
    # 阶段4: 返回结果
    # ------------------------------------------------------------------
    return selected_names, selected_intervals

"""
第二种写法
"""

# 不带权重的活动选择贪心算法
def greedy_activity_selector(S):
    """
    活动选择问题贪心算法
    目标：选择最多数量的互不重叠活动
    
    参数:
        S: 字典，键为活动名称，值为[开始时间, 结束时间]
    
    返回:
        selected_names: 选中的活动名称列表
        selected_intervals: 选中的活动区间列表
    """
    # 将字典转换为(名称, 开始, 结束)元组列表
    activities = [(name, interval[0], interval[1]) 
                  for name, interval in S.items()]
    
    # 按结束时间排序（贪心策略核心）
    activities.sort(key=lambda x: x[2])
    
    selected_names = []
    selected_intervals = []
    last_end_time = -1  # 上一个选中活动的结束时间
    
    # 遍历所有已排序的活动
    for name, start, end in activities:
        # 如果活动不冲突则选中
        if start >= last_end_time:
            selected_names.append(name)
            selected_intervals.append([start, end])
            last_end_time = end
    
    return selected_names, selected_intervals


# ------------------------------------------------------------------
# 测试数据
# ------------------------------------------------------------------
S = {
    'a1': [1, 4], 'a2': [3, 5], 'a3': [0, 6], 'a4': [4, 7],
    'a5': [3, 9], 'a6': [5, 9], 'a7': [6, 10], 'a8': [8, 11],
    'a9': [8, 12], 'a10': [2, 14], 'a11': [12, 16]
}

# ------------------------------------------------------------------
# 执行算法并打印结果
# ------------------------------------------------------------------
if __name__ == "__main__":
    names, intervals = greedy_activity_selector(S)
    
    print("="*60)
    print("活动选择问题（贪心算法）")
    print("="*60)
    print(f"总活动数: {len(S)}")
    print(f"可安排的最大活动数: {len(names)}")
    print("-"*60)
    print("选中的活动（按开始时间排序）:")
    
    # 按开始时间排序后输出，更直观
    sorted_results = sorted(zip(names, intervals), key=lambda x: x[1][0])
    for name, interval in sorted_results:
        print(f"  {name}: 开始时间={interval[0]}, 结束时间={interval[1]}")
    
    print("="*60)