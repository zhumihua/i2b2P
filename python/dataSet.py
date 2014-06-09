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


def collect(l,index):
    return map(itemgetter(index),l)

labelSeq=['during DCT','before DCT','after DCT','continuing']
posSeq=['VB','VBD','VBN','VBP','VBZ','MD']
lexiconSeq=re.split(',','before,after,cause,causedBy,during,starting,continuing,ending,suddenly,now,says')
#dependencySeq=re.split(',','gov,gov_POS')
disease_factors=re.split(' ','DIABETES CAD HYPERTENSION HYPERLIPIDEMIA OBESE')


secFile=open('sec_Names.txt','r')
secNameSeq=secFile.read().splitlines()
secFile.close()

relWordDict=open('wordDict.txt','r')
relWordSeq=relWordDict.read().splitlines()
relWordDict.close()

'''
features_pos, include the POS of verb and modal within the sentence
features_lexicon, 
features_dependencyTree, include govening word and its POS tag, length of the path through
the dependency from each entity to their common ancestor and the path between the two entities
... the agreement of different dependency parser

features_pathLEngth

'''

class TagInstance:
    i_type=''
    isMed=False
    i_id=''  
    
    sent='' 
    labels=None
    features_pos=None
    features_lexicon=None 
    features_relWords=None
    features_secName=None
    
    i_sec=''
#     sec_id=''
#     tag_text=''
#     tag_start=-1
#     tag_end=-1
    o_tag=None
    
    def __init__(self,i_id,i_type,sent,aTag):
        self.o_tag=aTag
        self.i_id=i_id
        self.i_type=i_type
        self.sent=sent
        
        self.labels=OrderedDict.fromkeys(labelSeq, 0)
    
        self.features_pos=OrderedDict.fromkeys(posSeq,0)
        self.setIsMed(i_type)
        
        self.features_lexicon=OrderedDict.fromkeys(lexiconSeq,0)
        
        self.features_relWords=OrderedDict.fromkeys(relWordSeq, 0)
        self.features_secName=OrderedDict.fromkeys(secNameSeq, 0)
        

    def setIsMed(self,i_type):
        self.isMed= not i_type.upper() in 'DIABETES CAD HYPERTENSION HYPERLIPIDEMIA OBESE'.split()
        
    def setLabel(self,time):
        self.labels[time]=1
    def setAFeature_pos(self,pos):
        if self.features_pos.has_key(pos):
            self.features_pos[pos]=1
    def setFeatures_pos(self):
        tokens=nltk.word_tokenize(self.sent)
        pos_list=collect(nltk.pos_tag(tokens),1)
        for pos in pos_list:
            self.setAFeature_pos(pos)
            
    def setFeatures_lexicon(self):
        pass
    def setFeatures_sent(self):
        pass
    
    def setAFeatures_relWord(self,aword):
        if self.features_relWords.has_key(aword):
            self.features_relWords[aword]=1
            

    def setFeatures_section(self,secName):
        if self.features_secName.has_key(secName):
            self.features_secName[secName]=1
    

    def getLabels(self):
        return self.labels.values()
    def getFeatures_pos(self):
        return self.features_pos.values()
    def getFeature_sec(self):
        return self.features_secName.values()
    def getFeature_rel(self):
        return self.features_relWords.values()
    def getAInstance(self):
        if self.o_tag==None:
            return [self.i_id,self.i_type,self.isMed]+self.getFeature_sec()+self.getFeature_rel()+self.getFeatures_pos()+self.getLabels()
        else:
            return [self.i_id,self.i_type,self.isMed,self.o_tag.text,self.o_tag.sec_id,self.o_tag.start,self.o_tag.end]+self.getFeatures_pos()+[self.sent]+self.getLabels()
    def getHeadline(self):
        ret=['id','type','isMed']
        ret+=posSeq
        ret+=lexiconSeq
        ret+=labelSeq
        return ['id','type','isMed','VB','VBD','VBN','VBP','VBZ','MD','during DCT','before DCT','after DCT','continuing']
    def loadLabel(self,values):
        for i,aLable in enumerate(labelSeq):
            self.labels[aLable]=values[i]
            
    def loadFeatures_pos(self,values):
        for i,aPos in enumerate(posSeq):
            self.features_pos[aPos]=values[i]
        
        
         
    
class ds:
    instances=OrderedDict()
    report=None
    #label, id of the instance
    def __init__(self,report):
        self.report=report

    def getHeadline(self):
        return ['id','type','isMed','VB','VBD','VBN','VBP','VBZ','MD','during DCT','before DCT','after DCT','continuing']        
    def getInstance(self,i_id):
        return self.instances[i_id]
    def hasInstance(self,i_id):
        return self.instances.has_key(i_id)
    def addInstance(self,tag):
        ########TODO, for incorrect lineNum, stag
        if tag.lineNum==-1:
            return
        tagId=self.report.id+"_"+str(tag.lineNum)+"_"+str(tag.start)+"_"+str(tag.end)
        aInstance=None
        if self.hasInstance(tagId):
            aInstance=self.getInstance(tagId)
            aInstance.setLabel(tag.time)
        else:
            sent=self.report.getTagLine(tag)
            tagType=tag.type
            #(self,i_id,i_type,sent)
            aInstance=TagInstance(tagId,tagType,sent,tag)
            aInstance.setLabel(tag.time)
            aInstance.setFeatures_pos()
            aInstance.setFeatures_sent()
            aInstance.setFeatures_section()
            self.instances[tagId]=aInstance
            
    def addAllInstances(self):
        for tag in self.report.tags:
            self.addInstance(tag)
            
    def printDS(self,headLine):
        ret=''
        if headLine:
            print '\t'.join(self.getHeadline())
            ret='\t'.join(self.getHeadline())+"\n"
        for key,value in self.instances.iteritems():
            print '\t'.join(map(str,value.getAInstance()))
            ret+='\t'.join(map(str,value.getAInstance()))+"\n"
        return ret
            
#     def separateTags(self,outDir):
#         for key,value in self.instances.iteritems():


    def DS2CSV(self,headLine=False):
        self.addAllInstances()
        return self.printDS(headLine)
    
    def DS2CSV_dependency(self,fileName='result.xls',headLine=False):
        csvFile=open(fileName,'r')
        lines=csvFile.read().splitlines()
        csvFile.close()
        
        for aline in lines:
            columns=re.split('\t',aline)
            tagId=columns[0]
            aInstance=None
            if self.hasInstance(tagId):
                aInstance=self.getInstance(tagId)
                aInstance.setAFeatures_relWord(columns[-1])
            else:
                tagType=columns[1]
                sent=columns[12]
                
                #(self,i_id,i_type,sent)
                aInstance=TagInstance(tagId,tagType,sent,None)
                aInstance.loadLabel(columns[13:17])
                aInstance.loadFeatures_pos(columns[6:12])
                #aInstance.loadFeatures_sent()
                aInstance.setFeatures_section(columns[4])
                aInstance.setAFeatures_relWord(columns[-1])
                self.instances[tagId]=aInstance
                
        return self.printDS(headLine)
        #return self.printLibSVM()

        
        
        
        
        