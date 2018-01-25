# python3.6后,math包已不存在
from cmath import log


# 计算数据集熵
def calcShannonEnt(dataSet):
    # 训练集行数
    numEntries = len(dataSet)
    # 字典,k:标签,v:标签出现的次数和
    labelCounts = {}
    for featVec in dataSet:
        # 获取训练集中的标签
        currentLabel = featVec[-1]
        # 保存标签和每个标签出现的次数
        labelCounts[currentLabel] = labelCounts.get(currentLabel, 0) + 1
        # if currentLabel not in labelCounts.keys():
        #     labelCounts[currentLabel] = 0
        # labelCounts[currentLabel] += 1
    # 初始化熵值
    shannonEnt = float(0.0)
    for key in labelCounts.keys():
        # 计算每个结果出现的概率
        prob = float(labelCounts[key] / numEntries)
        #  计算数据集的熵
        shannonEnt += (-prob * log(prob, 2))
    return shannonEnt


# 按照给定的特征划分数据集
def splitData(dataSet, axis, value):
    '''
    :param dataSet:要划分的数据集
    :param axis: 给定特征
    :param value:给定特征的具体值
    :return:
    '''
    subDataSet = []
    for data in dataSet:
        subData = []
        if data[axis] == value:
            # 取出data中的第0个到axis-1个数到subData
            subData = data[:axis]
            # 取出data中的第axis+1到-1的数到subData
            subData.extend(data[axis + 1:])
            subDataSet.append(subData)
    return subDataSet


# 创建数据集
def createDataSet():
    dataSet = [[1, 1, "yes"],
               [1, 2, "yes"],
               [1, 0, "no"],
               [0, 1, "no"],
               [0, 2, "no"]]
    labels = ["no surfacing", "flippers"]
    return dataSet, labels


if __name__ == '__main__':
    dataSet, labels = createDataSet()
    print(calcShannonEnt(dataSet))
    print(splitData(dataSet, 0, 0))
