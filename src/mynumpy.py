import numpy as np

# 创建数组
a = np.array([2, 3, 4])
b = np.array([[1, 2, 3], [4, 5, 6]])
c = np.array([1, 2, 3], dtype=complex)
print(a, b, c)

# 创建一个0数组
d = np.zeros((3, 4))
print(d)

# 创建1数组,指定元素类型为int16
one_arr = np.ones((2, 3, 4), dtype="int16")
print(one_arr)

# 创建一个内容随机并且依赖内存状态的数组
emp_arr = np.empty((2, 3, 4))
print(emp_arr)

# 创建对角矩阵
print(np.eye(4))

# 创建一个随机数组
random_arr = np.random.rand(4, 4)
print(type(random_arr))
random_arr2 = np.random.random((4, 4))
print(random_arr, random_arr2, type(random_arr), type(random_arr2))
print("------------------------------")

# 打印数组
a = np.arange(6)
print(a)
b = np.arange(12).reshape(3, 4)
print(b)
c = np.arange(24).reshape(2, 3, 4)
print(c)

# 数组的行列数
print(b.shape)
# 数组的秩(跟矩阵秩定义一致|A|！=0)、列数
print(b.ndim, b.itemsize)
# 数组中元素的个数
print(b.size)
# 数组的类型，数组元素的类型
print(type(a), a.dtype)
# 将数组转换成矩阵
mat_rand = np.matrix(random_arr)
print(type(mat_rand))

# 矩阵求逆
inv_rand_mat = mat_rand.I
print(inv_rand_mat)
# mat_rand*inv_rand_mat=E
my_eye = mat_rand * inv_rand_mat
print(my_eye - np.eye(4))

# 数组计算(按照元素进行计算)
a = np.array([20, 21, 22, 23])
b = np.arange(4)
c = a - b
print(c ** 2)
print(c * np.sin(a))
print(c < 18)
a = np.array([[1, 2, 3], [4, 5, 6]])
b = np.arange(6).reshape(2, 3)
# 数组乘法(元素相乘)
print(a * b, a, b)
# 矩阵乘法
print(np.dot(a, np.matrix(b).I), type(np.matrix(b).I))
print(np.dot(a, b.T))
# 数组求和
print(a.sum())
# 数组最大小值
print(a.max(), a.min())
# 按照指定的轴进行计算
# 列求和
print(a.sum(axis=0))
# 行求和
print(b.sum(axis=1))
# 列聚合求和
print(a.cumsum(axis=1))
# 行聚合计算
print(a.cumsum(axis=0))
# 列乘积
print(a.prod(axis=0))
# 行乘积
print(a.prod(axis=1))
# 列聚合乘积
print(a.cumprod(axis=0))
# 行聚合乘积
print(a.cumprod(axis=1))

# 通用函数
b = np.arange(4)
print(b)
# 指数函数exp()
print(np.exp(b))
# 平方根函数
print(np.sqrt(b))
c = np.array([1, 2, 3, 4])
# 加函数add()
print(b + c)
print(np.add(b, c))
# 均值函数mean(),方差函数var()
print(np.mean(b), np.var(b))

# 索引、切片、迭代
a = np.arange(10) ** 2
print(a)
# 获取数组中的第一个元素/第三个元素(索引)
print(a[0], a[2])
# 获取数组中第三个元素到第5个元素
print(a[2:5])
# 给切片元素赋值
a[: 5: 2] = 100
print(a)
# 数组的反转
print(a[:: -1])


def f(x, y):
    return 10 * x + y


# 由模板创建数组
b = np.fromfunction(f, (5, 4), dtype=int)
print(b)
# 二维数组的切片
# 获取数组中的第二行第三列元素
print(b[2, 3], type(b[2, 3]))
# 获取二维数组中第二行的所有元素
print(b[2:3, :])
# 获取二维数组中的倒数第一行所有元素
print(b[-1])
# 获取二维数组中所有行的第一列元素
print(b[:, 1])
# 获取二维数组中倒数第一列的所有元素
print(b[:, -1])
# 获取二维数组中第一行到第五行的第一列元素
print(b[0:5, 0])

# 数组遍历
# 数组元素迭代器
for element in b.flat:
    print(element)
# 遍历数组的每一行
for row in b:
    print(row)
# 遍历数组的每一列
for col in b.T:
    print(col)

# 更改数组的形状
# floor()获取数字的整数部分
a = np.floor(10 * np.random.rand(3, 4))
print(a, a.shape)
# 把所有元素表示成一行元素(ravel不改变原数组)
print(a.ravel())
print(a.shape)
# reshape函数不改变原数组的形状
print(a.reshape(4, 3))
print(a.shape)
# shape函数更改原数组的形状
a.shape = (2, 6)
print(a)
# 数组的转置
print(a.transpose())

# 数组的组合
a = np.floor(10 * np.random.rand(4, 5))
b = np.floor(10 * np.random.rand(4, 5))
# 水平组合(horizontal stack)
c = np.hstack((a, b))
print(c)
print(np.column_stack((a, b)))
print(np.concatenate((a, b), axis=1))
# 上下组合(verital stack)
c = np.vstack((a, b))
print(c)
print(np.row_stack((a, b)))
print(np.concatenate((a, b), axis=0))
a = np.array([2, 3, 4])

# 数组切割
a = np.arange(12).reshape(3, 4)
b = np.arange(12).reshape(4, 3)
print(np.hsplit(a, 4))
print(np.hsplit(a, 2))
print(np.vsplit(b, 4))
print(np.vsplit(b, 2))
print("---------横向切割--------------")
print(np.split(a, 3))
c = a
print(c is a)
c.shape = (4, 3)
print(c.shape, c, a)
print(a is b)

# 视图和浅复制
print("--------视图和浅复制------------")
a = np.arange(12).reshape(3, 4)
b = np.arange(12).reshape(4, 3)
# c和a指向同一个数组，地址值不一样
c = a.view()
print(c is a)
print(id(c), id(a))
print(c.base is a)
# 更改c的形状，不改变a的形状
c.shape = (4, 3)
print(a.shape)
# 更改c中元素的值，a的值也发生改变
c[0, 2] = 12
print(a)
# 切片返回的是数组的视图，当修改视图中元素值时，原数组发生改变
s = a[:, 1:3]
s[:] = 100
print(a)

# 深复制
print("----------深复制-------------")
d = a.copy()
print(d is a)
print(d.base is a)
d[0, 0] = 99
print(a)
