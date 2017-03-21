from numpy import *
import operator

def createDataSet():
    gp  = array([1.0,1.1][1.0,1.0][0,0][0,0.1])
    lbs = ['a','a','b','b']
    return gp,lbs

def clsfy(vectorx,datast,lbs,k):
    datasz = datast.shape[0]
    difmt = tile(vectorx ,(datasz,1)) - datast      #tile是矩阵维数倍增的函数
    difmtf = difmt ** 2     #**2表示每个元素都成原来的平方
    sqd = difmtf.sum(axis = 1)      #sum()是对所有元素求和,axis = 0是对每列求和 axis是对每行求和
    dsts = sqd ** 0.5       #同理
    sortdsa = dsts.argsort()        #排序
    classcount = {}
    for i in range(k):
        vtlbs = lbs[sortdsa[i]]
    classcount[vtlbs] = classcount.get(vtlbs,0) + 1
    stcls = sorted(classcount.iteritems(),key = operator.itemgetter(1),reverse=True)
    return stcls[0][0]

def filedeal(filename):
    fr = open(filename)
    arry = fr.readlines()
    numberline = len(arry)
    remat = zeros((numberline,3))
    classvt = []
    index = 0
    for line in arry:
        line = line.strip()
        s = line.split('\t')
        remat[index,:] = s[0:3]
        classvt.append(int(s[-1]))
        index += 1
    return remat,classvt