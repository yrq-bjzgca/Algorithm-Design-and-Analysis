from typing import List

def MergeCount(arr: List[int], left: int, right: int) -> int:
    """
    使用归并排序统计数组 arr[left..right] 中的逆序对总数。
    
    逆序对定义：对于数组中的两个元素 arr[i] 和 arr[j]，如果 i < j 且 arr[i] > arr[j]，
    则称 (i, j) 构成一个逆序对。
    
    算法思路（分治法）：
    1. 将数组分为左右两半
    2. 逆序对总数 = 左半部分的逆序对 + 右半部分的逆序对 + 跨越左右两部分的逆序对
    3. 递归计算左右两部分，在合并过程中统计跨越的逆序对
    
    参数:
        arr: 待统计的数组（会被修改成有序状态以辅助统计）
        left: 左边界索引（包含）
        right: 右边界索引（包含）
    
    返回:
        该区间内的逆序对总数（int 类型）
    """
    # 基本情况：区间长度为0或1时，不存在逆序对
    if left >= right:
        return 0
    
    # 计算中间索引，将数组分为左右两个子区间
    mid = (left + right) // 2
    
    # 递归计算左半部分 [left, mid] 的逆序对数量
    num_left = MergeCount(arr, left, mid)
    
    # 递归计算右半部分 [mid+1, right] 的逆序对数量
    num_right = MergeCount(arr, mid + 1, right)
    
    # 在合并过程中统计跨越左右两部分的逆序对数量
    num = CountInverse(arr, left, mid, right)
    
    # 返回三部分逆序对的总和
    return num_left + num_right + num


def CountInverse(arr: List[int], left: int, mid: int, right: int) -> int:
    """
    在合并两个已排序的子数组时，统计跨越左右两部分的逆序对数量。
    
    逆序对产生条件：
    当左子数组的当前元素 arr[i] > 右子数组的当前元素 arr[j] 时，
    左子数组中从 i 到 mid 的所有元素都大于 arr[j]，因此都与 arr[j] 构成逆序对。
    
    参数:
        arr: 输入数组
        left: 左子数组的起始索引
        mid: 左子数组的结束索引
        right: 右子数组的结束索引
    
    返回:
        跨越中间点的逆序对数量
    """
    # 创建临时数组，保存待合并区间的原始数据（避免被覆盖）
    temp = arr[left:right + 1].copy()
    
    # 初始化指针：
    # i: 遍历左子数组 [left, mid]
    # j: 遍历右子数组 [mid+1, right]
    # k: 在原数组中的写入位置
    i, j, k = left, mid + 1, left
    
    # count: 记录跨越逆序对的数量
    count = 0
    
    # 比较并合并两个子数组，同时统计逆序对
    while i <= mid and j <= right:
        if temp[i - left] <= temp[j - left]:
            # 左元素 <= 右元素，不构成逆序对，直接放入
            arr[k] = temp[i - left]
            i += 1
        else:
            # 左元素 > 右元素，构成逆序对
            # 左子数组中从 i 到 mid 的所有元素都大于当前右元素
            arr[k] = temp[j - left]
            j += 1
            # 统计新增的逆序对数量：mid - i + 1
            count += (mid - i + 1)
        k += 1
    
    # 复制左子数组剩余的元素（如果有）
    while i <= mid:
        arr[k] = temp[i - left]  
        k += 1
        i += 1
    
    # 复制右子数组剩余的元素（如果有）
    while j <= right:
        arr[k] = temp[j - left]  
        k += 1
        j += 1
    
    # 返回本次合并过程中统计的跨越逆序对数量
    return count


# 测试代码
if __name__ == "__main__":
    # 测试用例：逆序对包括 (2,1), (6,5)，共 2 个
    arr = [2, 1, 3, 4, 6, 5]
    print(f"输入数组: {arr}")
    
    # 统计逆序对数量（arr会被排序）
    inverse_count = MergeCount(arr, 0, len(arr) - 1)
    print(f"逆序对总数: {inverse_count}")
    print(f"排序后数组: {arr}")
