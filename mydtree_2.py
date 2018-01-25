from cmath import log


def calcshannoEnt(dataSet):
    # 训练集行数
    dataSetRow = len(dataSet)
    # 统计每个标签出现次数的数据集
    labelsCount = {}
    # 遍历数据集，计算每个标签出现的次数
    for item in dataSet:
        labelsCount[item[-1]] = labelsCount.get(item[-1], 0) + 1
    # 初始化信息熵值(熵值越大，表示数据越复杂)
    shannoEnt = float(0.0)
    for key in labelsCount.keys():
        # 计算正负面结果的概率值
        prob = labelsCount[key] / dataSetRow
        # 计算该分类条件下的信息熵值
        shannoEnt += (-prob * log(prob, 2))
    return shannoEnt


# 按照给定的特征和特征值返回指定数据集
def splitDataSet(dataSet, column, value):
    '''
    :param dataSet:训练集
    :param column: 特征值所在的列
    :param value: 特征值
    :return:
    '''
    retDataSet = []
    for feature in dataSet:
        # 判断该列表中是否存在该特征值
        if feature[column] == value:
            # 移除该特征值，并且把剩余数据保存到另一个列表中
            feature.remove(value)
            retDataSet.append(feature)
    return retDataSet


# 选择数据集划分方式(选出最优的划分方式)
def chooseBestFeatureToSplit(dataSet):
    numlen(dataSet[0])-1
    pass


if __name__ == '__main__':
    trainData = [[1, 1, "yes"],
                 [1, 2, "yes"],
                 [1, 0, "no"],
                 [0, 1, "no"],
                 [0, 2, "no"]]
    shanoEnt = calcshannoEnt(trainData)
    print(splitDataSet(trainData, 0, 0))
