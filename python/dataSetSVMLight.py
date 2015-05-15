import string
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys
import time
from datetime import date
import re
from subprocess import call
from collections import OrderedDict
from operator import itemgetter
import nltk
import lexicons
from nltk.tag.stanford import NERTagger

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2

from sklearn.datasets import dump_svmlight_file
import StringIO


#constant values
indicatorTestSeq=re.split(",","test,high bp,high chol.,high LDL,BMI,waist circum.,A1C,glucose")
#the key is the indicatorValues in i2b2, the value are the mapping lexicon
mapIndicatorName={'mention':'mention','symptom':'symptom','event':'event'}
for aTest in indicatorTestSeq:
    mapIndicatorName[aTest]='test'
    
indicatorNames=re.split(',','test,high bp,high chol.,high LDL,BMI,waist circum.,A1C,glucose,mention,symptom,event' )
indicatorSeq=list(set(mapIndicatorName.values()))

#########################

labelSeq=['during DCT','before DCT','after DCT','continuing' ]
#########################
###TODO, don't know what to do with grouping POS
posValues=['VB','VBD','VBG','VBN','VBP','VBZ','MD']
mapPOS={'VB':'VB','VBD':'VBD', 'VBG':'VBG','VBN':'VBN','VBP':'VBP','VBZ':'VBZ','MD':'MD'}
posSeq=list(set(mapPOS.values()))

#########################################
lexiconSeq=re.split(',','before,after,cause,causedBy,during,starting,continuing,ending,suddenly,now,says')

timexSeq=re.split(',','DCT_BEFORE,DCT_AFTER,DCT_DURING,TIMEX_END,TIMEX_MID,TIMEX_START,TIMEX_DURING,TIMEX_BEFORE,TIMEX_DURING,TYPE_DURING,TYPE_SET')

#lexiconSeq=re.split(',','before,after,during,starting,continuing,ending,suddenly,now,says')
#dependencySeq=re.split(',','gov,gov_POS')
disease_factors=re.split(' ','DIABETES CAD HYPERTENSION HYPERLIPIDEMIA OBESE')
medication=['MEDICATION']


secFile=open('sec_Names.txt','r')
secNameSeq=secFile.read().splitlines()
secFile.close()

relWordDict=open('wordDict.txt','r')
relWordSeq=relWordDict.read().splitlines()
relWordDict.close()

dictFeature=dict()
features=posSeq+lexiconSeq+timexSeq+secNameSeq+relWordSeq+medication+disease_factors+indicatorSeq
for index, val in enumerate(features):
    dictFeature[val]=index+1
 
            

class Instance:
    def __init__(self,id,dependencyC,pennTree,pathSubtree,newSent,aroundWords,oldSent,tagText,fvector):
        self.dependencyC=dependencyC
        self.pennTree=pennTree
        self.pathSubtree=pathSubtree
        self.newSent=newSent
        self.aroundWords=aroundWords
        self.oldSent=oldSent
        self.tagText=tagText
        self.fvector=fvector
        self.y=int(re.split("\t",fvector)[0])
        self.id=id
    
    def getY(self):
        return self.y
         
'''
features_pos, include the POS of verb and modal within the sentence
features_lexicon, 
features_dependencyTree, include govening word and its POS tag, length of the path through
the dependency from each entity to their common ancestor and the path between the two entities
... the agreement of different dependency parser

features_pathLEngth

'''
'''
first column is the tag_id,the last four column is the time attribute value(four values in the dtd)
time ( before DCT | during DCT | after DCT | continuing ) 
'''
# class Features:
#     TAG_ID==0
#     BEFORE_DCT,DURING_DCT,AFTER_DCT,CONTINUING=
          
#DICT_HEAD={'timeValue':0,'annoText':1,"secName":2, "indicator":3,"POS":4}  
class ds:
    #label, id of the instance
    K=150
    def __init__(self,dirIn):
        self.instances={0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
        self.catFiles(dirIn)
        
#         for i in range(8):
#             print len(self.instances.get(i))
        #t11=self.instances.get(3)
        #print "\n".join(t11)
    def catFiles(self,dirIn):
        for dirname, dirnames, filenames in os.walk(dirIn):
            for filename in filenames:
                if filename.strip()[0]=='.' :
                    continue
                f = os.path.join(dirname, filename)
                ff=open(f) 
                lines=ff.read().splitlines()
                for i in range(0,len(lines),8):
                    instance=Instance(i,lines[i],lines[i+1],lines[i+2],lines[i+3],lines[i+4],lines[i+5],lines[i+6],lines[i+7])
                    self.instances[instance.getY()].append(instance)


#get dataset for before, during, after
def binaryDS(ds,posList,negList):
    x_ds=[]
    y_ds=[]
    c_aroundWords=[]
    c_newSent=[]
    
    for p in posList:
        for instance in ds.instances.get(p):
            y_ds.append(1)
            x_ds.append(instance)
            c_aroundWords.append(instance.aroundWords)
            c_newSent.append(instance.newSent)
    for n in negList:
        for instance in ds.instances.get(n):
            y_ds.append(-1)
            x_ds.append(instance)
            c_aroundWords.append(instance.aroundWords)
            c_newSent.append(instance.newSent)
    return x_ds,y_ds,c_aroundWords,c_newSent

#get the bigram model, normarized by tfidf
def ngramModel(corpus,test,Y_train):
    bigram_vectorizer = CountVectorizer(ngram_range=(1,2),token_pattern=r'\b\w+\b', min_df=1)
    X_train = bigram_vectorizer.fit_transform(corpus)
    X_test = bigram_vectorizer.transform(test)
    #featureNames = bigram_vectorizer.get_feature_names()
    
    tfidf = TfidfTransformer(norm="l2")
    X_train = tfidf.fit_transform(X_train)
    X_test = tfidf.transform(X_test)
    #print X_train
    
    ch2=SelectKBest(chi2,k=ds.K)
    X_train=ch2.fit_transform(X_train,Y_train)
    X_test=ch2.transform(X_test)
    #print X_train
    #print X_test
    return X_train,X_test

#return libsvm format for ngram
def ngram2sparseStr(X_train, Y_train):
    strbuffer= StringIO.StringIO()
    dump_svmlight_file(X_train, Y_train, strbuffer,zero_based=False)
    ret=strbuffer.getvalue()
    strbuffer.close()

    rets=ret.split('\n')
    result=[]
    for astr in rets:
        if astr.find(' ')!=-1 and astr.index(' ')<len(astr)-1:
            result.append(astr[astr.index(' '):])
        else:
            result.append('')   
    return result

#return the libsvm format for vector
def binaryfeatures(x_train):
    rets=[]
    for instance in x_train:
            featureColumns=[] 
            values=re.split("\t", instance.fvector)
            values=getLexiconValues(values)
            for value in values[1:]:
                column=dictFeature.get(value)
                if column is not None and column not in featureColumns:
                    featureColumns.append(column)
            featureColumns.sort()
            alineDS=''
            for aCol in featureColumns:
                #alineDS+=" "+str(aCol+ds.K)+":1"
                alineDS+=" "+str(aCol)+":1"
            rets.append(alineDS)
    return rets

def getLexiconValues(values):
    ret=[]
    for value in values:
        value=value.strip().lower()
        if mapIndicatorName.has_key(value):
            ret.append(mapIndicatorName[value])
        elif mapPOS.has_key(value):
            ret.append(mapPOS[value])
        else:
            ret.append(value)
    return list(set(ret))

#return the tree string
def treeData(x_train):
    rets=[]
    for instance in x_train:
        tempStr=' |BT| '+instance.dependencyC+' |BT| '+instance.pennTree+' |BT| '+instance.pathSubtree+' |ET|'
        rets.append(tempStr)
    return rets

#write to file, a single group of features
def printSingle(x,y,filePath):
    print filePath
    f=open(filePath,'w')
    for i in range(len(y)):
        f.write(str(y[i])+x[i]+'\n')
    f.close()
    
def printVectors2(x1,x2,y,filePath):
    print filePath
    f=open(filePath,'w')
    for i in range(len(y)):
        f.write(str(y[i])+x1[i]+' |BV|'+x2[i]+' |EV|'+'\n')
    f.close()
    
def printVectors3(x1,x2,x3,y,filePath):
    print filePath
    f=open(filePath,'w')
    for i in range(len(y)):
        f.write(str(y[i])+x1[i]+' |BV|'+x2[i]+' |BV|'+x3[i]+' |EV|'+'\n')
    f.close()

def printVectorTree1(x1,t1,y,filePath):
    print filePath
    f=open(filePath,'w')
    for i in range(len(y)):
        f.write(str(y[i])+t1[i]+x1[i]+' |EV|'+'\n')
    f.close()

def printVectorTree2(x1,x2,t1,y,filePath):
    print filePath
    f=open(filePath,'w')
    for i in range(len(y)):
        f.write(str(y[i])+t1[i]+x1[i]+' |BV|'+x2[i]+' |EV|'+'\n')
    f.close() 

def printVectorTree3(x1,x2,x3,t1,y,filePath):
    print filePath
    f=open(filePath,'w')
    for i in range(len(y)):
        f.write(str(y[i])+t1[i]+x1[i]+' |BV|'+x2[i]+' |BV|'+x3[i]+' |EV|'+'\n')
    f.close() 
    


def generateDs(posList,negList,partialPath):
    x_train,y_train,train_aroundWords,train_newSent=binaryDS(train,posList,negList)
    x_test,y_test,test_aroundWords,test_newSent=binaryDS(test,posList,negList)
    
    #build n-gram data
    #vector index from 1 to ds.K
    ngram_train,ngram_test=ngramModel(train_aroundWords,test_aroundWords,y_train)
    newSent_train,newSent_test=ngramModel(train_newSent,test_newSent,y_train)
    
    ngram_train_x=ngram2sparseStr(ngram_train, y_train)
    ngram_test_x=ngram2sparseStr(ngram_test, y_test)
    newSent_train_x=ngram2sparseStr(newSent_train, y_train)
    newSent_test_x=ngram2sparseStr(newSent_test, y_test)
    
    #vector data
    bv_train_x=binaryfeatures(x_train)
    bv_test_x=binaryfeatures(x_test)
    
    #tree data
    tree_train_x=treeData(x_train)
    tree_test_x=treeData(x_test)
    
    #output dataset
    #single group of data
    filePath=partialPath+"ngram."
    printSingle(ngram_train_x,y_train,filePath+"train.data")
    printSingle(ngram_test_x,y_test,filePath+"test.data")
    
    filePath=partialPath+"newSent."
    printSingle(newSent_train_x,y_train,filePath+"train.data")
    printSingle(newSent_test_x,y_test,filePath+"test.data")
    
    filePath=partialPath+"bv."
    printSingle(bv_train_x,y_train,filePath+"train.data")
    printSingle(bv_test_x,y_test,filePath+"test.data")
    
    filePath=partialPath+"tree."
    printSingle(tree_train_x,y_train,filePath+"train.data")
    printSingle(tree_test_x,y_test,filePath+"test.data")
    
    #two group of data
    filePath=partialPath+"ngns."
    printVectors2(ngram_train_x,newSent_train_x,y_train,filePath+"train.data")
    printVectors2(ngram_test_x,newSent_test_x,y_test,filePath+"test.data")
    
    filePath=partialPath+"ngbv."
    printVectors2(ngram_train_x,bv_train_x,y_train,filePath+"train.data")
    printVectors2(ngram_test_x,bv_test_x,y_test,filePath+"test.data")
    
    filePath=partialPath+"nsbv."
    printVectors2(newSent_train_x,bv_train_x,y_train,filePath+"train.data")
    printVectors2(newSent_test_x,bv_test_x,y_test,filePath+"test.data")
    
    #two groups: vector and tree
    filePath=partialPath+"ngtr."
    printVectorTree1(ngram_train_x,tree_train_x,y_train,filePath+"train.data")
    printVectorTree1(ngram_test_x,tree_test_x,y_test,filePath+"test.data")
    
    filePath=partialPath+"nstr."
    printVectorTree1(newSent_train_x,tree_train_x,y_train,filePath+"train.data")
    printVectorTree1(newSent_test_x,tree_test_x,y_test,filePath+"test.data")
    
    filePath=partialPath+"bvtr."
    printVectorTree1(bv_train_x,tree_train_x,y_train,filePath+"train.data")
    printVectorTree1(bv_test_x,tree_test_x,y_test,filePath+"test.data")
    
    #three group of data
    filePath=partialPath+"ngnsbv."
    printVectors3(ngram_train_x,newSent_train_x,bv_train_x,y_train,filePath+"train.data")
    printVectors3(ngram_test_x,newSent_test_x,bv_test_x,y_test,filePath+"test.data")
    
    #three group: two vectors and a tree
    filePath=partialPath+"ngnstr."
    printVectorTree2(ngram_train_x,newSent_train_x,tree_train_x,y_train,filePath+"train.data")
    printVectorTree2(ngram_test_x,newSent_test_x,tree_test_x,y_test,filePath+"test.data")
    
    filePath=partialPath+"ngbvtr."
    printVectorTree2(ngram_train_x,bv_train_x,tree_train_x,y_train,filePath+"train.data")
    printVectorTree2(ngram_test_x,bv_test_x,tree_test_x,y_test,filePath+"test.data")
    
    filePath=partialPath+"nsbvtr."
    printVectorTree2(newSent_train_x,bv_train_x,tree_train_x,y_train,filePath+"train.data")
    printVectorTree2(newSent_test_x,bv_test_x,tree_test_x,y_test,filePath+"test.data")

    #four group of data
    filePath=partialPath+"ngnsbvtr."
    printVectorTree3(ngram_train_x,newSent_train_x,bv_train_x,tree_train_x,y_train,filePath+"train.data")
    printVectorTree3(ngram_test_x,newSent_test_x,bv_test_x,tree_test_x,y_test,filePath+"test.data")

    
    
    
def continueData(train,test,dirOut):
    posList=[7]
    negList=[0,1,2,3,4,5,6]
    partialPath=dirOut+"continue."
    generateDs(posList,negList,partialPath)

    
def beforeData(train,test,dirOut):
    posList=[1,3,5,7]
    negList=[0,2,4,6]
    partialPath=dirOut+"before."
    generateDs(posList,negList,partialPath)

    
def duringData(train,test,dirOut):
    posList=[2,3,6,7]
    negList=[0,1,4,5]
    partialPath=dirOut+"during."
    generateDs(posList,negList,partialPath)

    
def afterData(train,test,dirOut):
    posList=[4,5,6,7]
    negList=[1,2,3]
    partialPath=dirOut+"after."
    generateDs(posList,negList,partialPath)
           
    
if __name__=="__main__":
    dirIn = sys.argv[1]
    dirOut=sys.argv[2]
    dirInTest = sys.argv[3]
    train=ds(dirIn)
    test=ds(dirInTest)
    
    continueData(train,test,dirOut)
    beforeData(train,test,dirOut)
    duringData(train,test,dirOut)
    afterData(train,test,dirOut)
    

    

        
        
        
        
        