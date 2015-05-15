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

if __name__=="__main__":
    
#     i1=Instance(1,2,3,4,5,6,7,8,'1')
#     print i1.id
    
    
    f=open('tryCorpus')
    fy=open('tryCorpusY')
    ft=open('tryCorpusTest')
    fty=open('tryCorpusYTest')
    
    corpus=f.read().splitlines()
    corpusY=fy.read().splitlines()
    test=ft.read().splitlines()
    testY=fty.read().splitlines()
    
    bigram_vectorizer = CountVectorizer(ngram_range=(1,2),token_pattern=r'\b\w+\b', min_df=1)
    X_train = bigram_vectorizer.fit_transform(corpus)
    X_test = bigram_vectorizer.transform(test)
    print X_train
    featureNames = bigram_vectorizer.get_feature_names()
    
    

    tfidf = TfidfTransformer(norm="l2")
    X_train = tfidf.fit_transform(X_train)
    X_test = tfidf.transform(X_test)
    print X_train
    
    ch2=SelectKBest(chi2,k=20)
    X_train=ch2.fit_transform(X_train,testY)
    X_test=ch2.transform(X_test)
    #print X_train
    print X_test
    
    Y_train=[1,1,0,0]
    
    strbuffer= StringIO.StringIO()
    dump_svmlight_file(X_train, Y_train, strbuffer,zero_based=False)
    ret=strbuffer.getvalue()
    print ret
    strbuffer.close()
    rets=ret.split('\n')
    result=[]
    for astr in rets:
        print astr
        print '\n'
        if astr.find(' ')!=-1 and astr.index(' ')<len(astr)-1:
            result.append(astr[astr.index(' ')+1:])
        else:
            result.append('')
    
    
   
    
    
    
    

    
    

    

        
        
        
        
        