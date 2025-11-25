import random
from typing import List

def random_quickSort(arr: List[int], p: int, r: int) -> None:
    """
    随机化快速排序主函数（原地排序）
    
    算法特点：
    1. 通过随机选择基准元素，避免最坏情况O(n²)
    2. 期望时间复杂度始终为O(n log n)
    3. 原地排序，空间复杂度O(log n)
    
    参数:
        arr: 待排序数组（原地修改）
        p:   排序区间左边界（包含）
        r:   排序区间右边界（包含）
    """
    if p < r:
        # 随机划分，返回基准元素的最终位置
        q = random_partition(arr, p, r)
        
        # 递归排序左半部分 [p, q-1]
        random_quickSort(arr, p, q - 1)
        
        # 递归排序右半部分 [q+1, r]
        random_quickSort(arr, q + 1, r)
        

def random_partition(arr: List[int], p: int, r: int) -> int:
    """
    随机化分区函数（Lomuto方案）
    
    关键步骤：
    1. 随机选择 [p, r] 范围内的一个元素作为基准
    2. 将其与 arr[r] 交换（移到末尾）
    3. 执行标准Lomuto分区
    
    参数:
        arr: 待分区数组（原地修改）
        p:   分区左边界（包含）
        r:   分区右边界（包含）
    
    返回:
        基准元素的最终索引
    """
    # 随机选择基准元素索引（在[p, r]范围内等概率选择）
    s = random.randrange(p, r + 1)
    
    # 将基准交换到数组末尾（r位置）
    arr[s], arr[r] = arr[r], arr[s]
    
    # 以下为标准Lomuto分区逻辑（与之前相同）
    x = arr[r]          # 基准值
    i = p - 1           # "小于区域"的边界
    
    # 遍历 [p, r-1]，将小于基准的元素移到左侧
    for j in range(p, r):
        if arr[j] < x:
            # 扩展"小于区域"
            arr[j], arr[i + 1] = arr[i + 1], arr[j]
            i += 1
    
    # 将基准放到正确位置（i+1）
    arr[i + 1], arr[r] = arr[r], arr[i + 1]
    
    q = i + 1
    return q


# ============= 测试代码 =============
if __name__ == "__main__":
    # 测试用例
    arr = [4, 1, 2, 5, 6, 3]
    print(f"排序前: {arr}")
    
    random_quickSort(arr, 0, len(arr) - 1)
    
    print(f"排序后: {arr}")
    
    # 验证正确性
    assert arr == [1, 2, 3, 4, 5, 6], f"排序失败！"
    print("✓ 排序正确")