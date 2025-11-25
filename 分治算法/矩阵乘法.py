from typing import List

def poly_multiply(a: List[int], b: List[int]) -> List[int]:
    """
    使用分治算法（Karatsuba）计算两个多项式的乘积
    
    多项式表示：数组索引i对应x^i的系数
    例如：[1,2,3] 表示 1 + 2x + 3x²
    
    参数:
        a: 多项式A的系数数组（长度 ≥ 1）
        b: 多项式B的系数数组（长度 ≥ 1）
    
    返回:
        乘积多项式的系数数组
    
    示例:
        (1 + 2x) * (3 + 4x) = 3 + 10x + 8x²
        [1,2] * [3,4] = [3,10,8]
    """
    # 基础情况：长度为1时直接相乘
    n = len(a)
    m = len(b)
    
    if n == 1 and m == 1:
        return [a[0] * b[0]]
    
    # 使两个数组长度相同（补零）
    max_len = max(n, m)
    a = a + [0] * (max_len - n)
    b = b + [0] * (max_len - m)
    
   
    
    # 分割点
    k = max_len // 2
    
    # 分割多项式为高低两部分
    a0 = a[:k]          # 低次项
    a1 = a[k:]          # 高次项
    b0 = b[:k]
    b1 = b[k:]
    
    # Karatsuba算法：3次递归乘法
    U = poly_multiply(a0, b0)          # U = a0 * b0
    Z = poly_multiply(a1, b1)          # Z = a1 * b1
    
    # Y = (a0 + a1) * (b0 + b1)
    a01 = add_arrays(a0, a1)
    b01 = add_arrays(b0, b1)
    Y = poly_multiply(a01, b01)
    
    # 计算中间项：Y - U - Z
    middle = subtract_arrays(subtract_arrays(Y, U), Z)
    
    # 合并结果：U + middle*x^k + Z*x^(2k)
    result = [0] * (n + m - 1)  # 结果最大长度为n+m-1
    
    # 添加U（低次项）
    for i in range(len(U)):
        result[i] += U[i]
    
    # 添加middle（中次项，偏移k位）
    for i in range(len(middle)):
        result[i + k] += middle[i]
    
    # 添加Z（高次项，偏移2k位）
    for i in range(len(Z)):
        result[i + 2 * k] += Z[i]
    
    return result




def add_arrays(a: List[int], b: List[int]) -> List[int]:
    """数组加法（对应系数相加）"""
    n, m = len(a), len(b)
    max_len = max(n, m)
    result = [0] * max_len
    
    for i in range(n):
        result[i] += a[i]
    
    for i in range(m):
        result[i] += b[i]
    
    return result


def subtract_arrays(a: List[int], b: List[int]) -> List[int]:
    """数组减法（对应系数相减）"""
    n, m = len(a), len(b)
    max_len = max(n, m)
    result = [0] * max_len
    
    for i in range(n):
        result[i] += a[i]
    
    for i in range(m):
        result[i] -= b[i]
    
    return result


# ============= 测试代码 =============
if __name__ == "__main__":
    # 示例1: (1 + 2x) * (3 + 4x) = 3 + 10x + 8x²
    a1 = [1, 2]      # 1 + 2x
    b1 = [3, 4]      # 3 + 4x
    result1 = poly_multiply(a1, b1)
    print(f"{a1} × {b1} = {result1}")

    # 示例2: [1,2,3] × [3,2,2] = [3,8,13,10,6]
    a2 = [1, 2, 3]   # 1 + 2x + 3x²
    b2 = [3, 2, 2]   # 3 + 2x + 2x²
    result2 = poly_multiply(a2, b2)
    print(f"{a2} × {b2} = {result2}")
 
