import sys
import re
import string
from svmutil import *

def loadDataset(csvFile):
    f=open(csvFile,'r')
    y1=[]
    y2=[]
    y3=[]
    y4=[]
    ys=[y1,y2,y3,y4]
    
    x=[]
    
    for line in f:
        line=line.strip()
        feature_label=re.split('\,',line)
        labels=feature_label[-4:]
        features=feature_label[:-4]
        x.append(map(float,features))
        for index_label,y in enumerate(ys):
            y+=map(float,labels[index_label])
              
    f.close()
    
    
    for label in ys:
        prob=svm_problem(label,x)
        param=svm_parameter('-t 0 -v 10 -h 0')
        m=svm_train(prob,param)
        
    
    
if __name__=="__main__":
    loadDataset(sys.argv[1])
    