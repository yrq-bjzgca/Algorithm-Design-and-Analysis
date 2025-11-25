from typing import List

def merge_sort(arr: List[int], left: int, right: int) -> None:
    """
    对数组 arr 的 [left, right] 区间进行原地归并排序。
    
    参数:
        arr: 待排序的列表（原地修改）
        left: 排序区间的左边界索引（包含）
        right: 排序区间的右边界索引（包含）
    """
    # 递归终止条件：区间长度为0或1时已经有序
    if left >= right:
        return
    
    # 计算中间点，将区间分为左右两个子区间
    mid = (left + right) // 2
    
    # 递归排序左半部分 [left, mid]
    merge_sort(arr, left, mid)
    
    # 递归排序右半部分 [mid+1, right]
    merge_sort(arr, mid + 1, right)
    
    # 合并两个已排序的子区间
    merge(arr, left, mid, right)


def merge(arr: List[int], left: int, mid: int, right: int) -> None:
    """
    合并两个已排序的子数组 arr[left..mid] 和 arr[mid+1..right]。
    
    参数:
        arr: 待合并的列表（原地修改）
        left: 左子数组的起始索引
        mid: 左子数组的结束索引
        right: 右子数组的结束索引
    """
    # 创建临时数组，复制待合并区间的元素（避免被覆盖）
    temp = arr[left:right + 1].copy()
    
    # 初始化三个指针：
    # i: 遍历左子数组 [left, mid]
    # j: 遍历右子数组 [mid+1, right]
    # k: 临时数组中的偏移量（从0开始）
    i, j, k = left, mid + 1, 0
    
    # 比较两个子数组的元素，按升序合并到原数组
    # 使用 < 保证排序稳定性（相等时优先取左子数组的元素）
    while i <= mid and j <= right:
        if temp[i - left] < temp[j - left]:
            arr[k + left] = temp[i - left]
            i += 1
        else:
            arr[k + left] = temp[j - left]
            j += 1
        k += 1
    
    # 复制左子数组剩余的元素（如果有）
    while i <= mid:
        arr[k + left] = temp[i - left]
        i += 1
        k += 1
    
    # 复制右子数组剩余的元素（如果有）
    while j <= right:
        arr[k + left] = temp[j - left]
        j += 1
        k += 1


if __name__ == "__main__":
    # 测试用例
    arr = [4, 1, 2, 5, 6, 3]
    print(f"排序前: {arr}")
    
    merge_sort(arr, 0, len(arr) - 1)
    
    print(f"排序后: {arr}")