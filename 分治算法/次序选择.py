from typing import List
import random
def quickselect(arr: List[int], p: int, r: int, k: int) -> int:
    """
    QuickSelect算法：在未排序数组中找到第k小的元素（基于快速排序的分区思想）
    
    参数:
        arr: 待查找的数组（原地修改）
        p:   查找区间的左边界索引（包含）
        r:   查找区间的右边界索引（包含）
        k:   目标元素在[p, r]区间内的顺序（从1开始）
    
    返回:
        第k小的元素值
    
    示例：
        arr = [5, 2, 4, 1, 3]，找第3小元素
        返回值为3
    
    时间复杂度：
        - 平均：O(n)
        - 最坏：O(n²)
    """
    # 对数组进行分区，返回基准元素的最终位置
    if p <= r:
        # q = partition(arr, p, r)
        
        q = random_partition(arr, p, r)
        # 计算基准元素在[p, r]区间内的顺序
        # q-p+1 表示 arr[q] 是第(q-p+1)小的元素
        rank = q - p + 1
        
        if k == rank:
            # 基准元素正好是目标元素
            return arr[q]
        elif k < rank:
            # 目标元素在左半部分
            return quickselect(arr, p, q - 1, k)
        else:
            # 目标元素在右半部分
            # 注意：k-rank 是相对于右半部分的新顺序
            return quickselect(arr, q + 1, r, k - rank)


def partition(arr: List[int], p: int, r: int) -> int:
    """
    Lomuto分区方案（与快速排序相同）
    
    将数组分为两部分：
    - arr[p..i] 的所有元素 < arr[r]
    - arr[i+1..r-1] 的所有元素 >= arr[r]
    
    参数:
        arr: 待分区数组（原地修改）
        p:   分区左边界（包含）
        r:   分区右边界（包含）
    
    返回:
        基准元素的最终索引
    """
    # 选择最右边的元素作为基准
    pivot = arr[r]
    
    # i指向"小于基准区域"的最后一个元素
    i = p - 1
    
    # j遍历 [p, r-1]
    for j in range(p, r):
        if arr[j] < pivot:
            # 将小于基准的元素交换到左侧
            arr[j], arr[i + 1] = arr[i + 1], arr[j]
            i += 1
    
    # 将基准元素放到正确位置（i+1）
    arr[r], arr[i + 1] = arr[i + 1], arr[r]
    
    return i + 1

def random_partition(arr: List[int], p: int, r: int) -> int:
    """
    Lomuto分区方案（与快速排序相同）
    
    将数组分为两部分：
    - arr[p..i] 的所有元素 < arr[r]
    - arr[i+1..r-1] 的所有元素 >= arr[r]
    
    参数:
        arr: 待分区数组（原地修改）
        p:   分区左边界（包含）
        r:   分区右边界（包含）
    
    返回:
        基准元素的最终索引
    """
    # 选择随机数作为主元
    if p<r:
        print("p:",p,"r:",r)
        s = random.randrange(p,r)
        arr[r],arr[s] = arr[s],arr[r]
    pivot = arr[r]
    
    # i指向"小于基准区域"的最后一个元素
    i = p - 1
    
    # j遍历 [p, r-1]
    for j in range(p, r):
        if arr[j] < pivot:
            # 将小于基准的元素交换到左侧
            arr[j], arr[i + 1] = arr[i + 1], arr[j]
            i += 1
    
    # 将基准元素放到正确位置（i+1）
    arr[r], arr[i + 1] = arr[i + 1], arr[r]
    
    return i + 1

# ============= 测试代码 =============
if __name__ == "__main__":
    # 测试用例1：基本查找
    arr1 = [5, 2, 4, 1, 3]
    print(f"数组: {arr1}")
    
    kth = quickselect(arr1, 0, len(arr1) - 1, 3)
    print(f"第3小的元素: {kth}")
  
    
    # 测试用例2：边界情况（找最小值）
    arr2 = [7, 3, 5, 2, 9]
    min_val = quickselect(arr2, 0, len(arr2) - 1, 1)
    print(f"数组: {arr2}")
    print(f"第1小的元素（最小值）: {min_val}")

    # 测试用例3：边界情况（找最大值）
    arr3 = [4, 8, 2, 6]
    max_val = quickselect(arr3, 0, len(arr3) - 1, 4)
    print(f"数组: {arr3}")
    print(f"第{len(arr3)}小的元素（最大值）: {max_val}")
  
    
    # 测试用例4：单元素数组
    arr4 = [5]
    single = quickselect(arr4, 0, 0, 1)
    print(f"单元素数组: {arr4}")
    print(f"第1小的元素: {single}")

    
