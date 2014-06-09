import string
import os
import sys
import re




if __name__=="__main__":
    inFile=sys.argv[1]
    outFile1=sys.argv[2]
    outFile2=sys.argv[3]
    outFile3=sys.argv[4]
    outFile4=sys.argv[5]
    
    f=open(inFile,'r')
    o1=open(outFile1,'w')
    o2=open(outFile2,'w')
    o3=open(outFile3,'w')
    o4=open(outFile4,'w')
    outFiles=[o1,o2,o3,o4]
    
    for line in f:
        feature_label=re.split('\,',line)
        labels=feature_label[-4:]
        features=feature_label[:-4]
        for i,out in enumerate(outFiles):
            out.write(",".join(labels[i]+features)+"\n")
              
    f.close()
    for out in outFiles:
        out.close()

