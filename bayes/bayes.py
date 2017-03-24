from numpy import *
import re

def clsfyby(vecclsfy,p0vec,p1vec,pclass1):
    p1 = sum(vecclsfy * p1vec) + log(pclass1)
    '''becasue we get log,so we don't use *,rather than we use sum'''
    p0 = sum(vecclsfy * p0vec) + log(1.0 - pclass1)
    if p1 > p0:
        return 1
    else:
        return 0

def testingby():
    listpost,listclass = loaddataset()
    myvocablist = createvocablist(listpost)
    trainmat = []
    for k in listpost:
        trainmat.append(setofwordsvec(myvocablist,k))
    p0v,p1v,pab = trainby(array(trainmat),array(listclass))
    testentry = ['love','my','dalmation']
    thisdoc = array(setofwordsvec(myvocablist,testentry))
    print testentry,'classified as:',clsfyby(thisdoc,p0v,p1v,pab)
    testentry = ['stupid', 'garbage']
    thisdoc = array(setofwordsvec(myvocablist, testentry))
    print testentry, 'classified as:', clsfyby(thisdoc, p0v, p1v, pab)

def trainby(traindataset,trainclass):
    numtrain = len(traindataset)
    numword = len(traindataset[0])
    pabusive = sum(trainclass)/float(numtrain)
    p0num = ones(numword); p1num = ones(numword)
    p0denom = 2.0;  p1denom = 2.0
    for i in range(numtrain):
        if trainclass[i] == 1:
            p1num += traindataset[i]
            p1denom += sum(traindataset[i])
        else:
            p0num += traindataset[i]
            p0denom += sum(traindataset[i])
    p1vect = log(p1num/p1denom)
    p0vect = log(p0num/p0denom)
    return p0vect,p1vect,pabusive

def loaddataset():
    postinglist = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop','posting','stupid','worthless','garbage'],
                   ['mr','licks','ate','my','steak','how','to','stop','him'],
                   ['quit','buying','worthless','dog','food','stupid']]
    classvec = [0,1,0,1,0,1]
    return postinglist,classvec

def createvocablist(dataset):
    vocabset = set([])
    for document in dataset:
        vocabset = vocabset | set(document)
    return list(vocabset)

def bagofwordsvec(vocablist,inputset):
    revec = [0] * len(vocablist)
    for word in inputset:
        revec[vocablist.index(word)] += 1
    return revec

def setofwordsvec(vocablist,inputset):
    revec = [0] * len(vocablist)
    for word in inputset:
        if word in vocablist:
            revec[vocablist.index(word)] = 1
        else:   print "the word: %s is not in my vocabulary!" % word
    return revec

def textparse(bigstring):
    listtoken = re.split(r'\W*',bigstring)
    return [tok.lower() for tok in listtoken if len(tok) > 2]

def spamtest():
    doclist = [];
    classlist = [];
    fulltext = [];
    for i in range(1,26):
        wordlist = textparse(open('spam/%d.txt' % i).read())
        doclist.append(wordlist)
        fulltext.extend(wordlist)
        classlist.append(1)
        wordlist = textparse(open('ham/%d.txt' % i).read())
        doclist.append(wordlist)
        fulltext.extend(wordlist)
        classlist.append(0)
    vocablist = createvocablist(doclist)
    trainset = range(50);   testset =[]
    for i in range(10):
        randindex = int(random.uniform(0,len(trainset)))
        testset.append(trainset[randindex])
        del(trainset[randindex])
    trainmat = [];  trainclass = []
    for docindex in trainset:
        trainmat.append(setofwordsvec(vocablist,doclist[docindex]))
        trainclass.append(classlist[docindex])
    p0v,p1v,pspam = trainby(array(trainmat),array(trainclass))
    errorcount = 0
    for d in testset:
        wordvec = setofwordsvec(vocablist,doclist[docindex])
        if clsfyby(array(wordvec),p0v,p1v,pspam) != classlist[docindex]:
            errorcount += 1
    print 'the error rate is: ',float(errorcount)/len(testset)


if __name__=="__main__":
    listpost,listclass = loaddataset()
    myvocablist = createvocablist(listpost)
    print myvocablist
    print setofwordsvec(myvocablist,listpost[0])
    print setofwordsvec(myvocablist, listpost[1])
    print setofwordsvec(myvocablist, listpost[2])
    print setofwordsvec(myvocablist, listpost[3])
    trainmat = []
    for postdoc in listpost:
        trainmat.append(setofwordsvec(myvocablist,postdoc))
    p0v,p1v,pab = trainby(trainmat,listclass)
    print pab
    print p0v
    print p1v
    testingby()
    mysent = 'This book is the best book on Python or M.L. I have ever laid eyes upon.'
    print mysent.split()
    regex = re.compile('\\W*')
    listtoken = regex.split(mysent)
    print listtoken
    print [tok.lower() for tok in listtoken if len(tok) > 0]
    emailtext = open('1.txt').read()
    listtoken = regex.split(emailtext)
