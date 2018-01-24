import numpy as np
from os import listdir


def img2Vector(filename):
    # 创建一个1行1024列的零数组
    returnVect = np.zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        # 把数组转换成一行(0...1023)
        for j in range(32):
            returnVect[0, i * 32 + j] = int(lineStr[j])
    return returnVect


def handwritingClassTest():
    hwLabels = []
    # 训练数据集的文件名称
    trainingFileList = listdir(r"C:\Users\chen\Desktop\trainingDigits")
    # 训练数据集的文件长度
    m = len(trainingFileList)
    # 创建训练零数据
    trainingMat = np.zeros((m, 1024))
    # 训练零数组指针
    count = 0
    for item in trainingFileList:
        # 字符串切片，获取第一个元素，表示该图片所对应的数字(切片之后为list)
        classNumStr = int(item.split("_")[0])
        # 把图片对应数字保存到标签列表中(文件名称)
        hwLabels.append(classNumStr)
        # 调用img2Vector函数，把训练数据保存到零数组
        trainingMat[count, :] = img2Vector(r"C:\Users\chen\Desktop\trainingDigits\%s" % item)
        count += 1
    # 误差计数
    errorCount = 0
    # 测试数据集文件名称
    testFileList = listdir(r"C:\Users\chen\Desktop\testDigits")
    # 训练数据集的文件长度
    n = len(testFileList)
    for item in testFileList:
        # 测试数据对应的数字
        fileNumStr = int(item.split("_")[0])
        # 测试数据集数据
        testMat = img2Vector(r"C:\Users\chen\Desktop\testDigits\%s" % item)
        classfiyResult = classify0(testMat, trainingMat, hwLabels, 3)
        print(fileNumStr,classfiyResult)
        if fileNumStr!=classfiyResult:
            errorCount += 1
    return float(errorCount / n)


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


if __name__ == '__main__':
    errorRate = handwritingClassTest()
    print(errorRate)
