from typing import List

def quickSort(arr: List[int], p: int, r: int) -> None:
    """
    快速排序主函数（原地排序）
    
    参数:
        arr: 待排序的数组（原地修改）
        p:   排序区间的左边界索引（包含）
        r:   排序区间的右边界索引（包含）
    
    算法思路：
    1. 如果区间有效（p < r），选择基准元素
    2. 通过partition函数将数组划分为两部分
    3. 递归排序左半部分 [p, q-1]
    4. 递归排序右半部分 [q+1, r]
    """
    if p < r:
        # 划分数组，q是基准元素的最终位置
        q = partition(arr, p, r)
        
        # 递归排序左半部分（所有小于基准的元素）
        quickSort(arr, p, q - 1)
        
        # 递归排序右半部分（所有大于基准的元素）
        quickSort(arr, q + 1, r)
        
  

def partition(arr: List[int], p: int, r: int) -> int:
    """
    分区函数（Lomuto方案）
    
    功能：
    选择arr[r]作为基准（pivot），重新排列数组，
    使得所有小于基准的元素都在其左侧，大于基准的在右侧
    
    参数:
        arr: 待分区的数组（原地修改）
        p:   分区区间的左边界索引（包含）
        r:   分区区间的右边界索引（包含）
    
    返回:
        基准元素的最终索引位置
    """
    # 选择最后一个元素作为基准
    x = arr[r]
    
    # i指向小于基准区域的最后一个元素
    i = p - 1
    
    # j遍历从p到r-1的所有元素
    for j in range(p, r):
        # 如果当前元素小于基准
        if arr[j] < x:
            # 将其与i+1位置的元素交换，扩展到"小于区域"
            arr[j], arr[i + 1] = arr[i + 1], arr[j]
            i += 1  # "小于区域"扩大
    
    # 循环结束后，arr[p..i]都小于基准，arr[i+1..r-1]都大于等于基准
    
    # 将基准元素放到正确位置（i+1）
    arr[i + 1], arr[r] = arr[r], arr[i + 1]
    
    # 返回基准的最终位置
    q = i + 1
    return q


# ============= 测试代码 =============
if __name__ == "__main__":
    # 测试用例
    arr = [4, 1, 2, 5, 6, 3]
    print(f"排序前: {arr}")
    
    quickSort(arr, 0, len(arr) - 1)
    
    print(f"排序后: {arr}")
    