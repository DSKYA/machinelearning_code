from math import log
import operator

def storetree(inputtree,filename):
    import pickle
    fw = open(filename,'w')
    pickle.dump(inputtree,fw)
    fw.close()

def grabtree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

def clsf(inputtree,featlabels,testvec):
    firststr = inputtree.keys()[0]
    seconddict = inputtree[firststr]
    featindex = featlabels.index(firststr)
    for key in seconddict.keys():
        if testvec[featindex] == key:
            if type(seconddict[key]).__name__=='dict':
                classlbs = clsf(seconddict[key],featlabels,testvec)
            else:
                classlbs = seconddict[key]
    return classlbs

def getnumleaf(mytree):
    numleaf = 0
    firststr = mytree.keys()[0]
    seconddict = mytree[firststr]
    for key in seconddict.keys():
        if type(seconddict[key]).__name__ == 'dict':
            numleaf += getnumleaf(seconddict[key])
        else:
            numleaf += 1
    return numleaf

def retree(i):
    list = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},{'no surfacing': {0: 'no', 1: {'flippers': {0: {'head':{0:'no',1:'yes'}}, 1: 'no'}}}}]
    return list[i]


def gettreedepth(mytree):
    maxdepth = 0
    firststr = mytree.keys()[0]
    seconddict = mytree[firststr]
    for key in seconddict.keys():
        if type(seconddict[key]).__name__ == 'dict':
            thisdepth = 1 + gettreedepth(seconddict[key])
        else:
            thisdepth = 1
        if thisdepth > maxdepth:
            maxdepth = thisdepth
    return maxdepth

def majoritycnt(classlist):
    classcount = {}
    for vote in classlist:
        if vote not in classcount.keys():   classcount[vote] = 0
        classcount[vote] += 1
    sortedclasscount = sorted(classcount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedclasscount[0][0]

def createtree(dataset,lbs):
    classlist = [example[-1] for example in dataset]
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]
    if len(dataset[0]) == 1:
        return majoritycnt(classlist)
    bestfeat = chbstsplt(dataset)
    bestfeatlbs = lbs[bestfeat]
    mytree = {bestfeatlbs:{}}
    del(lbs[bestfeat])
    featvalues = [example[bestfeat] for example in dataset]
    uniquevals = set(featvalues)
    for value in uniquevals:
        sublbs = lbs[:]
        mytree[bestfeatlbs][value] = createtree(splitidataset(dataset,bestfeat,value),sublbs)
    return mytree

def calshang(dataset):
    sum = len(dataset)
    lbscount = {}
    for vec in dataset:
        currentlbs = vec[-1]
        if currentlbs not in lbscount.keys():lbscount[currentlbs] = 0
        lbscount[currentlbs] += 1
    sn = 0.0
    for key in lbscount:
        prob = float(lbscount[key])/sum
        sn -= prob * log(prob,2)
    return sn

def createdataset():
    dataset = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataset,labels

def splitidataset(dataset,axis,value):
    rdataset = []
    for vec in dataset:
        if  vec[axis]   ==  value:
            rvec = vec[:axis]
            rvec.extend(vec[axis +  1:])
            rdataset.append(rvec)
    return rdataset

def chbstsplt(dataset):
    num = len(dataset[0]) - 1
    baseshang = calshang(dataset)
    bestinfogain = 0.0; bestfeature = -1
    for i in range(num):
        featlist = [example[i] for example in dataset]
        uniquevals = set(featlist)
        newshang = 0.0
        for value in uniquevals:
            subdataset = splitidataset(dataset,i,value)
            prob = len(subdataset)/float(len(dataset))
            newshang += prob * calshang(subdataset)
        infogain = baseshang - newshang
        if(infogain > bestinfogain):
            bestinfogain = infogain
            bestfeature = i
    return bestfeature
if __name__ == "__main__":
    dataset,lbs = createdataset()
    print dataset
    print calshang(dataset)
    print splitidataset(dataset,0,0)
    print chbstsplt(dataset)
    dataset2,lbs2 = createdataset()
    mytree = createtree(dataset2,lbs2)
    print mytree
    print retree(1)
    mytree2 = retree(1)
    print getnumleaf(mytree)
    print getnumleaf(mytree2)
    print gettreedepth(mytree)
    print gettreedepth(mytree2)
    print lbs
    print clsf(mytree,lbs,[1,1])
    storetree(mytree,'tree.txt')
    mytree2 = grabtree('tree.txt')
    print mytree2