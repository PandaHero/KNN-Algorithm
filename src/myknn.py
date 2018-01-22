from numpy import *
import operator


# 训练样本数据
def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ["A", "A", "B", "B"]
    return group, labels

# KNN算法
def classify(int_x, data_set, labels, k):
    '''
    # int_x,      分类数据
    # data_set,   训练样本集
    # labels,     标签向量
    # K,          用于选择最近邻居的数目
    '''
    # 训练样本的行数
    data_set_size = data_set.shape[0]
    # 通过tile函数把输入数据扩展成和训练数据相同行数的矩阵，列数不需要扩展(列数==1)
    # 计算差值矩阵
    diffMat = tile(int_x, (data_set_size, 1)) - data_set
    # 计算差值矩阵的平方值
    sqDiffMat = diffMat ** 2
    # print(sqDiffMat)
    # 计算差值平方矩阵中每一行元素的和
    sqDistance = sqDiffMat.sum(axis=1)
    # print(type(sqDistance))
    # 计算距离平方矩阵的平方根
    distance = sqDistance ** 0.5
    # 每一行元素从小到大排序。返回每个元素对应的下标
    # argsort()函数：将数组排序，返回对应元素下标
    # argsort()[index]:下标元素值
    sortSistanceIndex = distance.argsort()
    # 统计前k个结果的投票数
    classCount = {}
    for i in range(k):
        # 获取排序后的前K个下标值
        index = sortSistanceIndex[i]
        # 对应下标值的标签
        voteLabels = labels[index]
        # 计算求和标签的个数，并保存到字典
        classCount[voteLabels] = classCount.get(voteLabels, 0) + 1
    # 对字典中的value进行排序(从大到小)
    sortClassCount = sorted(classCount.items(), key=lambda x: x[1], reverse=True)
    return sortClassCount[0][0]


if __name__ == '__main__':
    k = 3
    group, labels = createDataSet()
    x = array([0, 0])
    print(classify(x, group, labels, k))
