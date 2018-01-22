import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# 将文本转换成Numpy的array
def file2matrix(filename):
    # 打开文件
    fr = open(filename)
    # 获取文件的所有行
    arrayLines = fr.readlines()
    # 获取文件的行数
    numberLines = len(arrayLines)
    # 创建零矩阵
    retureMax = np.zeros([numberLines, 3])
    # 把文本转换成数字
    labelVector = {"largeDoses": 3, "smallDoses": 2, "didntLike": 1}
    # 保存训练数据的标签数据
    classLabelVector = []
    index = 0
    for line in arrayLines:
        # 删除首尾空行
        line = line.strip()
        # split函数通过"\t"分割字符串
        listFromLine = line.split("\t")
        # 把listFromLine中的前三个元素添加到returnMax中
        retureMax[index, :] = listFromLine[0:3]
        # 把listFromLine数组的最后一行标签添加到标签数组中
        classLabelVector.append(labelVector[listFromLine[-1]])
        # returnMax矩阵行数加1
        index += 1
    #     返回训练样本矩阵和类标签
    return retureMax, classLabelVector


# 数据可视化
def showDateSet_(datingDataMat, datingLabels):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:, 0], datingDataMat[:, 2], c=10 * np.array(datingLabels), s=10 * np.array(datingLabels),
               label='散点图')
    plt.xlabel('玩视频游戏所耗时间百分比', fontproperties='SimHei', fontsize='14')
    plt.ylabel('每周消费的冰淇淋公升数', fontproperties='SimHei', fontsize='14')
    plt.show()


# 归一化特征值
def autoNorm(dataSet):
    # 获取数据中每列的最大值(0:列)
    maxValues = dataSet.max(0)
    # 获取数据中每列的最小值
    minValues = dataSet.min(0)
    # 计算最大值和最小值的差值
    ranges = maxValues - minValues
    # 创建一个与dataSet相同shape的0矩阵，用于存放归一化后的数据
    normDataSet = np.zeros(dataSet.shape)
    # 获取数据集的行数
    data_row = dataSet.shape[0]
    # 计算数据集和最小值矩阵的差值
    normDataSet = dataSet - np.tile(minValues, (data_row, 1))
    # 把最大值和最小值的差值扩充到与dataSet同shape的矩阵，计算商值
    normDataSet = normDataSet / np.tile(ranges, (data_row, 1))
    return normDataSet, ranges, minValues


# KNN算法
def classify0(intX, dataSet, labels, k):
    # intX:     输入测试样本(x,y)
    # dataSet:  训练样本集([a1,a2]...[n1,n2])
    # labels:   训练样本标签
    # k:        分类前k个值
    # 获取训练样本集的行数
    data_row = dataSet.shape[0]
    # 把测试样本转换成和训练样本同shape的数组，并计算差值
    diffMat = np.tile(intX, (data_row, 1)) - dataSet
    # 计算差值矩阵的平方值
    sqDiffMat = diffMat ** 2
    # 计算平方之后的数组每行的和
    sqDistance = sqDiffMat.sum(axis=1)
    # 计算平方之后差值矩阵的平方根
    distance = sqDistance ** 0.5
    # distance中的元素从大到小排序，得到排序之后的下标值
    sortDistance = distance.argsort()
    # 统计每个标签出现的次数
    labelsCount = {}
    for i in range(k):
        # 获取对应下标的标签属性
        voteLabels = labels[sortDistance[i]]
        # 若labelsCout中不存在该元素,则+1，否则再原基础+1
        labelsCount[voteLabels] = labelsCount.get(voteLabels, 0) + 1
    # 对labelsCount字典进行从大到小排序,sortLabelsCount是一个list，每个元素是一个tuple
    sortLabelsCount = sorted(labelsCount.items(), key=lambda x: x[1], reverse=True)
    return sortLabelsCount[0][0]


def dataingClassTest(normMat, dataLabels, k):
    # 测试数据，训练数据比例为1:9
    hoRatio = 0.1
    # 获取归一化之后数据集的行数
    m = normMat.shape[0]
    # 测试数据集行数
    numTestVecs = int(m * hoRatio)
    # 错误分类计数器
    errorCount = 0
    for i in range(numTestVecs):
        classifyResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], dataLabels[numTestVecs:m], k)
        if classifyResult != dataLabels[i]:
            errorCount += 1
    return errorCount / numTestVecs


if __name__ == '__main__':
    datingDataMat, datingLabels = file2matrix(r"C:\Users\chen\Desktop\datingTestSet.txt")
    # showDateSet_(datingDataMat, datingLabels)
    normMat, ranges, minValues = autoNorm(datingDataMat)
    errorRate = dataingClassTest(datingDataMat, datingLabels, 8)
    print(errorRate)
