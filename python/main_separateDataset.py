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
    
    outFile5=sys.argv[6]
    outFile6=sys.argv[7]
    outFile7=sys.argv[8]

    
    f=open(inFile,'r')
    o1=open(outFile1,'w')
    o2=open(outFile2,'w')
    o3=open(outFile3,'w')
    o4=open(outFile4,'w')
    
    o5=open(outFile5,'w')
    o6=open(outFile6,'w')
    o7=open(outFile7,'w')

    
    outFiles=[o1,o2,o3,o4,o5,o6,o7]
    
    
#     num_before=0
#     num_during=0
#     num_after=0
#     num_before_during=0
#     num_before_after=0
#     num_during_after=0
#     num_continue=0#before_during_after
    
    for line in f:
        line=line.strip()
        feature_label=re.split('\,',line)
        labels=feature_label[-4:]
        features=feature_label[:-4]
        
        labels[-1]=str('1' if labels[0]=='1' and labels[1]=='1' and labels[2]=='1' else '-1' )
        labels.append('1' if labels[0]=='1' and  labels[1]=='1' else '-1')
        labels.append('1' if labels[0]=='1' and  labels[2]=='1' else '-1')
        labels.append('1' if labels[1]=='1' and  labels[2]=='1' else '-1')
        
        for i,out in enumerate(outFiles):
            out.write(",".join([labels[i]]+features)+"\n")
        
              
    f.close()
    for out in outFiles:
        out.close()
        

        
#     print     num_before,num_during,num_after,num_before_during,num_before_after,num_during_after,num_continue

