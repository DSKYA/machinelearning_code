from math import log
import operator

def majoritycnt(classlist):
    classcount = {}
    for vote in classlist:
        if vote not in classcount.keys():   classcount[vote] = 0
        classcount[vote] += 1
    sortedclasscount = sorted(classcount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedclasscount[0][0]

def createtree(dataset,labels):
    classlist = [example[-1] for example in dataset]
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]
    if  len(dataset[0]) == 1:
        return majoritycnt(classlist)
    bestfeat = chbstsplt(dataset)
    bestfeatlbs = lbs[bestfeat]
    mytree = {bestfeatlbs:{}}
    del(lbs[bestfeat])
    featvalues = [example(bestfeat) for example in dataset]
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
