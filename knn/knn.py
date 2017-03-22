from numpy import *
import operator

def autonormal(datast):
        min = datast.min(0)
        '''column's min'''
        max = datast.max(0)
        '''column's max'''
        dis = max - min
        '''normalmat = zeros(shape(datast))'''
        m = datast.shape[0]
        '''columns'''
        normalmat = datast - tile(min,(m,1))
        normalmat = normalmat/tile(dis,(m,1))
        return normalmat,dis,min

def clstest():
    bili = 0.1
    datamat,datalbs = filedeal('1.txt')
    normalmat,dis,min = autonormal(datamat)
    m = normalmat.shape[0]
    numtest = int(m * bili)
    errorcount = 0.0
    for r in range(numtest):
        result = clsfy(normalmat[r,:],normalmat[numtest:m,:],datalbs[numtest:m,3])
        print "Hello World!%d %d"%(result,datalbs[r])
        if(result != datalbs[r]):
            errorcount += 0.1
    print "total number is %f" %(errorcount/float(numtest))

def createDataSet():
    gp  = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    lbs = ['a','a','b','b']
    return gp,lbs

def clsfy(vectorx,datast,lbs,k):
    datasz = datast.shape[0]
    difmt = tile(vectorx ,(datasz,1)) - datast
    difmtf = difmt ** 2
    sqd = difmtf.sum(axis = 1)
    dsts = sqd ** 0.5
    sortdsa = dsts.argsort()
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

if __name__=="__main__":
    gp,lbs = createDataSet()
    print clsfy([0,0],gp,lbs,3)