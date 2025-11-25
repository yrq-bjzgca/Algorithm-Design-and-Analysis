import math
from typing import List

def MaxSubArray(arr: List[int], left: int, right: int) -> int:
    """
    使用分治法找出数组 arr[left..right] 中的最大子数组和。
    
    算法思路：
    1. 将数组分为左右两半
    2. 最大子数组和要么完全在左半部分，要么完全在右半部分，
       要么跨越中间点（同时包含左右两部分）
    3. 递归求解左右两部分，单独处理跨越情况，最后取三者最大值
    
    参数:
        arr: 输入数组
        left: 左边界索引（包含）
        right: 右边界索引（包含）
    
    返回:
        该区间内的最大子数组和（int 类型）
    """
    # 基本情况：当区间只有一个元素时，直接返回该元素
    if left == right:
        return arr[left]
    
    # 计算中间索引，将数组分为左右两个子区间
    mid = (left + right) // 2
    
    # 递归计算左半部分 [left, mid] 的最大子数组和
    S1 = MaxSubArray(arr, left, mid)
    
    # 递归计算右半部分 [mid+1, right] 的最大子数组和
    S2 = MaxSubArray(arr, mid + 1, right)
    
    # 计算跨越中间点的最大子数组和（必须同时包含左右两部分的元素）
    S3 = CrossingSubArray(arr, left, mid, right)
    
    # 返回三种情况中的最大值
    return max(S1, S2, S3)


def CrossingSubArray(arr: List[int], left: int, mid: int, right: int) -> int:
    """
    计算跨越中间点的最大子数组和。
    该子数组必须包含 arr[mid] 和 arr[mid+1]。
    
    算法思路：
    1. 从中间点向左扫描，找出包含 arr[mid] 的最大子数组和
    2. 从中间点+1向右扫描，找出包含 arr[mid+1] 的最大子数组和
    3. 返回左右两部分之和
    
    参数:
        arr: 输入数组
        left: 左边界索引（包含）
        mid: 中间索引
        right: 右边界索引（包含）
    
    返回:
        跨越中间点的最大子数组和
    """
    # 初始化左半部分的最大和为负无穷，用于追踪最大值
    left_max = -math.inf
    # 初始化左半部分的当前和为0
    left_sum = 0
    
    # 从中间点向左遍历，找出包含 arr[mid] 的最大子数组和
    # range(mid, left-1, -1) 确保包含 left 到 mid 的所有索引
    for i in range(mid, left - 1, -1):
        left_sum += arr[i]
        left_max = max(left_sum, left_max)
    
    # 初始化右半部分的最大和为负无穷
    right_max = -math.inf
    # 初始化右半部分的当前和为0
    right_sum = 0
    
    # 从中间点+1向右遍历，找出包含 arr[mid+1] 的最大子数组和
    # range(mid+1, right+1) 确保包含 mid+1 到 right 的所有索引
    for j in range(mid + 1, right + 1):
        right_sum += arr[j]
        right_max = max(right_sum, right_max)
    
    # 返回左右两部分之和，即跨越中间点的最大子数组和
    return left_max + right_max


# 测试代码
if __name__ == "__main__":
    # 测试用例：最大子数组是 [1, 8, -4, 5]，和为 10
    arr = [-1, -3, -5, 1, 8, -4, 5]
    print(f"输入数组: {arr}")
    
    max_sum = MaxSubArray(arr, 0, len(arr) - 1)
    print(f"最大子数组和: {max_sum}")
    
