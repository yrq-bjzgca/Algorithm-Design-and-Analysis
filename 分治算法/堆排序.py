def extra_min(arr):
    """
    堆排序的提取阶段：将已构建的最大堆转换为升序排列的数组。
    通过反复将堆顶元素（最大值）交换到当前未排序部分的末尾来实现排序。
    
    :param arr: 已构建好的最大堆数组（会被原地修改）
    :return: 排序后的数组
    """
    n = len(arr)
    
    # 从数组末尾开始，倒序遍历到第二个元素
    # 每次循环将当前堆的最大值移到数组的未排序部分末尾
    for i in range(n - 1, 0, -1):
        # 交换堆顶元素（最大值，索引0）与当前末尾元素（索引i）
        arr[0], arr[i] = arr[i], arr[0]
        
        # 对剩余堆（大小为i）重新堆化，恢复最大堆性质
        heapify(arr, i, 0)
    
    return arr

def heapify(arr, n, i):
    """
    递归维护最大堆性质的核心函数。
    确保以节点i为根的子树满足最大堆性质（父节点大于子节点）。
    
    :param arr: 待维护的数组
    :param n: 堆的有效大小（仅数组前n个元素属于堆）
    :param i: 当前需要堆化的节点索引
    """
    largest = i      # 初始化最大值为当前节点
    left = 2 * i + 1  # 左子节点的索引
    right = 2 * i + 2  # 右子节点的索引
    
    # 如果左子节点存在且大于当前最大值
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    # 如果右子节点存在且大于当前最大值
    # BUG修复：原代码缺少 arr[right] > arr[largest] 的比较条件
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    # 如果最大值不是当前节点，需要调整堆结构
    if largest != i:
        # 交换当前节点与最大值节点
        arr[i], arr[largest] = arr[largest], arr[i]
        
        # 递归地对受影响的子树进行堆化
        heapify(arr, n, largest)

def insert(arr):
    """
    构建最大堆：将无序数组转换为最大堆结构。
    从最后一个非叶子节点开始，自底向上构建堆。
    
    :param arr: 待构建的数组（会被原地修改）
    """
    n = len(arr)
    
    # 从最后一个非叶子节点（索引为 n//2 - 1）开始
    # 倒序遍历到根节点（索引0），确保每个节点都满足堆性质
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # 注意：该函数直接修改原数组，不返回任何值

if __name__ == "__main__":
    # 测试数据
    arr = [4, 5, 3, 2, 1]
    print("原始数组:", arr)
    
    # 步骤1：构建最大堆
    # 调用insert后，arr被原地修改为最大堆结构
    insert(arr)
    print("构建最大堆后:", arr)  # 预期输出: [5, 4, 3, 2, 1]
    
    # 步骤2：执行堆排序（提取阶段）
    # 调用extra_min后，arr变为升序排列
    sorted_arr = extra_min(arr)
    print("排序后数组:", sorted_arr)  # 预期输出: [1, 2, 3, 4, 5]