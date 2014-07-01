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

def TF2binary(x):
    if str(x) == 'False' or str(x) == '0':
        return str(0)
    elif str(x) == '-1':
        return str(-1)
    else:
        return str(1)

def collect(l,index):
    return map(itemgetter(index),l)

labelSeq=['during DCT','before DCT','after DCT','continuing', ]
posSeq=['VB','VBD','VBG','VBN','VBP','VBZ','MD']
lexiconSeq=re.split(',','before,after,cause,causedBy,during,starting,continuing,ending,suddenly,now,says')
#dependencySeq=re.split(',','gov,gov_POS')
disease_factors=re.split(' ','DIABETES CAD HYPERTENSION HYPERLIPIDEMIA OBESE')


secFile=open('sec_Names.txt','r')
secNameSeq=secFile.read().splitlines()
secFile.close()

relWordDict=open('wordDict.txt','r')
relWordSeq=relWordDict.read().splitlines()
relWordDict.close()

dictFeature=dict()
features=posSeq+lexiconSeq+secNameSeq+relWordSeq
for index, val in enumerate(features):
    dictFeature[val]=index+1
 

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
          
    
class TestDS:
    #2    170/84    physical exam    high bp    VBN
    DICT_HEAD={'timeValue':0,'annoText':1,"secName":2, "indicator":3,"POS":4}
    #label, id of the instance
    def __init__(self,dirIn,dirOut):
        self.loadFile(dirIn,dirOut)
        
    def loadFile(self,dirIn,dirOut):
        for dirname, dirnames, filenames in os.walk(dirIn):
            for filename in filenames:
                if filename.strip()[0]=='.' :
                    continue
                f = os.path.join(dirname, filename)
                ff=open(f) 
                lines=ff.read().splitlines()
                fout=open(dirOut+filename+".data","w")
                for line in lines:
                    self.createInstance(line,fout)
                fout.close()
                ff.close()

   
    def createInstance(self,line,fout):
                featureColumns=[] 
                values=re.split("\t", line)
                alineDS=values[0]
                for value in values[1:]:
                    column=dictFeature.get(value)
                    if column is not None and column not in featureColumns:
                        featureColumns.append(column)
                featureColumns.sort()
                for aCol in featureColumns:
                    alineDS+=" "+str(aCol)+":1"
                fout.write(alineDS+'\n')
                        
                        

    
           
    
if __name__=="__main__":
    dirIn = sys.argv[1]
    dirOut=sys.argv[2]
    a=TestDS(dirIn,dirOut)

    

        
        
        
        
        