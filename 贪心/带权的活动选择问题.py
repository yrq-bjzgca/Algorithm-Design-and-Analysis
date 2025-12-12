class Activity:
    """
    活动类：封装活动信息
    
    属性:
        name: 活动名称
        start: 开始时间
        end: 结束时间
        weight: 活动权重/价值
    """
    def __init__(self, name, start, end, weight):
        self.name = name
        self.start = start
        self.end = end
        self.weight = weight
    
    def __repr__(self):
        """返回字符串表示，便于调试和打印"""
        return f"{self.name}: [{self.start}, {self.end}] (权重={self.weight})"


def Weighted_Activity_Selector(S, weights):
    """
    带权重的活动选择问题动态规划解法（二分查找优化版）
    
    参数:
        S: 字典，键为活动名，值为[开始时间, 结束时间]
        weights: 字典，键为活动名，值为权重
    
    返回:
        max_weight: 最大权重和
        selected_names: 被选中的活动名称列表
    """
    
    # ------------------------------------------------------------------
    # 阶段1: 将字典转换为Activity对象列表（添加哨兵活动）
    # ------------------------------------------------------------------
    # 创建Activity对象列表，在索引0处添加哨兵活动（简化边界条件）
    # 哨兵活动: start=-1, end=-1, weight=0，确保DP数组从1开始
    activities = [Activity("dummy", -1, -1, 0)]  # 索引0的哨兵
    
    # 遍历字典创建实际活动对象
    for name, interval in S.items():
        activities.append(Activity(name, interval[0], interval[1], weights[name]))
    
    # 按结束时间排序（保持哨兵在开头，即索引0）
    activities = [activities[0]] + sorted(activities[1:], key=lambda act: act.end)
    
    n = len(activities) - 1  # 排除哨兵后的实际活动数量
    
    # ------------------------------------------------------------------
    # 阶段2: 使用二分查找计算前驱数组p[i]（优化核心）
    # ------------------------------------------------------------------
    # p[i]表示在i之前最后一个与i兼容的活动索引（包含哨兵）
    p = [0] * (n + 1)  # p[0] = 0
    
    # 二分查找辅助函数：查找最后一个满足end <= target的索引
    def find_predecessor(target_start, end_idx):
        """
        在activities[0:end_idx]中二分查找最后一个结束时间≤target_start的索引
        
        参数:
            target_start: 当前活动的开始时间
            end_idx: 查找范围的上界（不包含）
        
        返回:
            满足条件的最大索引（若不存在返回0，即哨兵）
        """
        left, right = 0, end_idx - 1
        result = 0  # 默认返回哨兵索引0
        
        while left <= right:
            mid = (left + right) // 2
            if activities[mid].end <= target_start:
                result = mid  # 记录候选答案
                left = mid + 1  # 向右继续查找更晚结束的活动
            else:
                right = mid - 1  # 向左查找
        
        return result
    
    # 为每个活动计算前驱（i从1到n）
    for i in range(1, n + 1):
        p[i] = find_predecessor(activities[i].start, i)
    
    # ------------------------------------------------------------------
    # 阶段3: 动态规划（自底向上）
    # ------------------------------------------------------------------
    # DP[i]表示前i个活动（索引1到i）能获得的最大权重和
    DP = [0] * (n + 1)
    
    # chosen[i]记录第i个活动是否被选中
    chosen = [False] * (n + 1)
    
    for i in range(1, n + 1):
        # 情况1：不选择第i个活动
        not_choose = DP[i - 1]
        
        # 情况2：选择第i个活动
        # 收益 = 当前活动权重 + 前驱活动的DP值
        choose = activities[i].weight + DP[p[i]]
        
        # 选择收益更大的方案
        if choose > not_choose:
            DP[i] = choose
            chosen[i] = True
        else:
            DP[i] = not_choose
            chosen[i] = False
    
    # ------------------------------------------------------------------
    # 阶段4: 回溯找出选中的活动
    # ------------------------------------------------------------------
    selected_names = []
    idx = n
    
    # 从后往前回溯，根据chosen数组判断哪些活动被选中
    while idx > 0:
        if chosen[idx]:
            # 如果选择了第idx个活动
            selected_names.append(activities[idx].name)
            idx = p[idx]  # 跳转到其前驱活动
        else:
            idx -= 1  # 继续检查前一个活动
    
    # 恢复按开始时间排序的顺序
    selected_names.reverse()
    
    return DP[n], selected_names


# ------------------------------------------------------------------
# 测试数据（注意：weight中补充了a11）
# ------------------------------------------------------------------
S = {
    'a1': [1, 4], 'a2': [3, 5], 'a3': [0, 6], 'a4': [4, 7],
    'a5': [3, 9], 'a6': [5, 9], 'a7': [6, 10], 'a8': [8, 11],
    'a9': [8, 12], 'a10': [2, 14], 'a11': [12, 16]
}

weights = {
    'a1': 1, 'a2': 6, 'a3': 4, 'a4': 7, 'a5': 3, 'a6': 12, 
    'a7': 2, 'a8': 9, 'a9': 11, 'a10': 8, 'a11': 5
}

# ------------------------------------------------------------------
# 执行算法并打印结果
# ------------------------------------------------------------------
if __name__ == "__main__":
    max_weight, selected = Weighted_Activity_Selector(S, weights)
    
    print("="*60)
    print("带权重的活动选择问题（二分查找优化）")
    print("="*60)
    print(f"总活动数: {len(S)}")
    print(f"最大权重和: {max_weight}")
    print("-"*60)
    print("选中的活动方案:")
    
    # 按时间顺序显示
    total_weight = 0
    for name in selected:
        interval = S[name]
        weight_val = weights[name]
        total_weight += weight_val
        print(f"  {name}: 时间 [{interval[0]}, {interval[1]}], 权重={weight_val}")
    