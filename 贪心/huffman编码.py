class MinHeap:
    """
    手写最小堆（优先队列）实现
    
    核心性质：
    1. 完全二叉树结构
    2. 父节点值 ≤ 子节点值（最小堆性质）
    3. 用数组存储，索引i的父节点为(i-1)//2，左子节点为2*i+1，右子节点为2*i+2
    """
    
    def __init__(self):
        """初始化空堆"""
        self.heap = []  # 用列表存储堆元素
    
    def push(self, item):
        """
        插入元素并维持堆性质
        
        步骤：
        1. 将新元素添加到列表末尾
        2. 执行上浮操作（heapify_up）调整到正确位置
        """
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)
    
    def pop(self):
        """
        弹出最小元素并维持堆性质
        
        步骤：
        1. 将堆顶（最小）元素与末尾元素交换
        2. 弹出并保存原堆顶元素
        3. 对新的堆顶执行下沉操作（heapify_down）
        4. 返回原堆顶元素
        
        返回:
            堆中最小元素
        """
        if len(self.heap) == 0:
            raise IndexError("堆为空")
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        # 交换堆顶和末尾
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        # 弹出原堆顶
        min_item = self.heap.pop()
        # 对新的堆顶执行下沉
        self._heapify_down(0)
        
        return min_item
    
    def _heapify_up(self, idx):
        """
        上浮操作：将索引idx处的元素向上调整至满足堆性质
        
        原理：
        比较节点与其父节点，如果节点值更小则交换，直到根节点或不再满足交换条件
        """
        while idx > 0:
            parent_idx = (idx - 1) // 2  # 父节点索引
            # 如果当前节点比父节点小，交换
            if self.heap[idx] < self.heap[parent_idx]:
                self.heap[idx], self.heap[parent_idx] = self.heap[parent_idx], self.heap[idx]
                idx = parent_idx  # 继续向上检查
            else:
                break
    
    def _heapify_down(self, idx):
        """
        下沉操作：将索引idx处的元素向下调整至满足堆性质
        
        原理：
        比较节点与其左右子节点，如果子节点更小，与最小的子节点交换，直到叶子节点
        """
        n = len(self.heap)
        while True:
            left_idx = 2 * idx + 1  # 左子节点索引
            right_idx = 2 * idx + 2  # 右子节点索引
            smallest = idx  # 假设当前节点最小
            
            # 找到三者中最小的
            if left_idx < n and self.heap[left_idx] < self.heap[smallest]:
                smallest = left_idx
            if right_idx < n and self.heap[right_idx] < self.heap[smallest]:
                smallest = right_idx
            
            # 如果最小的是子节点，交换并继续下沉
            if smallest != idx:
                self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
                idx = smallest  # 继续向下检查
            else:
                break
    
    def __len__(self):
        """返回堆中元素数量"""
        return len(self.heap)
    
    def __repr__(self):
        """字符串表示，便于调试"""
        return f"MinHeap({self.heap})"


class Node:
    """
    哈夫曼树节点类
    
    属性:
        _name: 字符名称（叶子节点存储字符，内部节点为None）
        _value: 节点权值（字符频率）
        _left: 左子节点
        _right: 右子节点
    """
    def __init__(self, name=None, value=None):
        self._name = name
        self._value = value
        self._left = None
        self._right = None
    
    def __lt__(self, other):
        """定义比较规则，用于堆的排序（按权值value比较）"""
        return self._value < other._value
    
    def __repr__(self):
        """字符串表示，便于调试"""
        if self._name:
            return f"Node('{self._name}', {self._value})"
        else:
            return f"Node(*, {self._value})"


def Build_Huffman_Tree(F, names):
    """
    使用自定义的最小堆构建哈夫曼树
    
    参数:
        F: 频率列表，F[i]表示第i个字符的频率
        names: 字符列表，names[i]表示第i个字符
    
    返回:
        root: 哈夫曼树的根节点
    """
    # 创建最小堆并加入所有叶子节点
    heap = MinHeap()
    for i in range(len(F)):
        heap.push(Node(names[i], F[i]))
    
    # 当堆中节点数大于1时，不断合并最小的两个节点
    while len(heap) > 1:
        # 弹出两个权值最小的节点
        left = heap.pop()
        right = heap.pop()
        
        # 创建父节点，权值为两者之和
        parent = Node(None, left._value + right._value)
        parent._left = left
        parent._right = right
        
        # 将新节点加入堆
        heap.push(parent)
    
    # 返回根节点
    return heap.pop()


def Generate_Codes(root, current_code="", code_dict=None):
    """
    递归遍历哈夫曼树，为每个字符生成编码
    
    参数:
        root: 当前遍历的节点
        current_code: 从根到当前节点的路径编码（左0右1）
        code_dict: 存储编码结果的字典
    
    返回:
        code_dict: {字符: 编码} 映射字典
    """
    if code_dict is None:
        code_dict = {}
    
    # 叶子节点：记录字符编码
    if root._name is not None:
        code_dict[root._name] = current_code if current_code != "" else "0"
        return code_dict
    
    # 递归遍历左子树，路径添加'0'
    if root._left:
        Generate_Codes(root._left, current_code + "0", code_dict)
    
    # 递归遍历右子树，路径添加'1'
    if root._right:
        Generate_Codes(root._right, current_code + "1", code_dict)
    
    return code_dict


def Print_Tree(node, level=0, prefix="Root"):
    """
    可视化打印哈夫曼树结构（辅助函数）
    
    参数:
        node: 当前节点
        level: 节点深度（用于缩进）
        prefix: 节点描述（Root/Left/Right）
    """
    if node is None:
        return
    
    # 打印当前节点
    indent = "  " * level
    if node._name:
        print(f"{indent}{prefix}: '{node._name}' (freq={node._value})")
    else:
        print(f"{indent}{prefix}: * (freq={node._value})")
    
    # 递归打印子树
    if node._left:
        Print_Tree(node._left, level + 1, "Left")
    if node._right:
        Print_Tree(node._right, level + 1, "Right")


def Huffman(F, names):
    """
    完整的哈夫曼编码流程
    
    参数:
        F: 频率列表
        names: 字符列表
    
    返回:
        code_dict: 编码字典
        root: 哈夫曼树根节点
    """
    # 步骤1: 构建哈夫曼树
    root = Build_Huffman_Tree(F, names)
    
    # 步骤2: 生成编码表
    code_dict = Generate_Codes(root)
    
    return code_dict, root


# ------------------------------------------------------------------
# 主程序测试与演示
# ------------------------------------------------------------------
if __name__ == "__main__":
    # 测试数据：6个字符及其频率
    F = [5, 9, 12, 13, 16, 45]      # 频率
    names = ['f', 'e', 'c', 'b', 'd', 'a']  # 对应字符
    
    print("="*60)
    print("哈夫曼编码演示（手写优先队列版本）")
    print("="*60)
    
    # 执行哈夫曼编码
    code_dict, root = Huffman(F, names)
    
    # 打印哈夫曼树结构
    print("\n哈夫曼树结构:")
    print("-"*30)
    Print_Tree(root)
    
    # 打印编码表
    print("\n" + "="*60)
    print("哈夫曼编码表（按频率降序）:")
    print("-"*30)
    sorted_items = sorted(code_dict.items(), key=lambda x: F[names.index(x[0])], reverse=True)
    for char, code in sorted_items:
        freq = F[names.index(char)]
        print(f"  '{char}': {code:>6s}  (频率: {freq:2d})")
    
    # 编码示例
    print("\n" + "="*60)
    test_string = "fecbda"
    encoded = Encode_String(test_string, code_dict)
    print(f"\n字符串 '{test_string}' 的哈夫曼编码:")
    print(f"  编码结果: {encoded}")
    print(f"  编码长度: {len(encoded)} 位")
    
    # 性能与复杂度分析
    print("\n" + "="*60)
    print("复杂度分析:")
    print("-"*30)
    print(f"  字符种类数: {len(F)}")
    print(f"  优先队列版本时间复杂度: O(n log n)")
    print(f"  手写堆操作时间复杂度: O(n log n)")
    print(f"  空间复杂度: O(n)")
    print("="*60)
    
    # 验证前缀性质
    codes = list(code_dict.values())
    prefix_free = True
    for i in range(len(codes)):
        for j in range(len(codes)):
            if i != j and codes[i].startswith(codes[j]):
                prefix_free = False
                break
    print(f"\n前缀性质验证: {'✓ 满足' if prefix_free else '✗ 不满足'}")