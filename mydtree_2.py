import math


# 计算数据集的信息熵
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
        shannoEnt -= prob * math.log(prob, 2)
    return shannoEnt


# 按照给定的特征和特征值返回指定数据集(删除指定特征值的数据集)
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
            reducedFeatureVec = feature[:column]
            reducedFeatureVec.extend(feature[column + 1:])
            retDataSet.append(reducedFeatureVec)
    return retDataSet


# 选择数据集划分方式(选出最优的划分方式)第一次特征选择
def chooseBestFeatureToSplit(dataSet):
    # 原始数据集的长度(不包含标签)
    numFeatures = len(dataSet[0]) - 1
    # 计算原始数据集的信息熵
    baseShannoEnt = calcshannoEnt(dataSet)
    # 设置初始分类信息增益值为0
    bestInfoGain = 0
    # 设置初始分类信息增益特征列值为-1
    bestFeature = -1
    for i in range(numFeatures):
        # 获取数据集中的列元素(特征值)(列表推导)
        featureList = [example[i] for example in dataSet]
        # 列元素(特征值)去重
        uniqueVals = set(featureList)
        # 设置特征的信息熵
        newShannoEnt = 0
        # 遍历每一个特征值计算每一个特征值的信息熵
        for value in uniqueVals:
            # 获取包含该特征值的数据集(数据集中remove该特征值)
            subDataSet = splitDataSet(dataSet, i, value)
            # 计算包含该特征值的所有样本占原始数据集合的比例(概率)
            prob = len(subDataSet) / float(len(dataSet))
            # 计算该特征值下的信息熵
            newShannoEnt += prob * calcshannoEnt(subDataSet)
        # 计算该特征下的信息增益
        infoGain = baseShannoEnt - newShannoEnt
        if infoGain > bestInfoGain:
            bestInfoGain = int(infoGain)
            bestFeature = i
    return bestFeature


if __name__ == '__main__':
    trainData = [[1, 1, "yes"],
                 [1, 0, "yes"],
                 [1, 0, "no"],
                 [0, 1, "no"],
                 [1, 0, "no"]]
    featureFirst = chooseBestFeatureToSplit(trainData)
    print(featureFirst)
