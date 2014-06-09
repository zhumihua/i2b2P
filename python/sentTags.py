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
from nltk.tokenize.punkt import PunktWordTokenizer
from nltk.tokenize import WordPunctTokenizer
from nltk.tokenize import WhitespaceTokenizer

from dataSet import ds

#    f=open(path+fileName,"w")
#    call(["perl","Sent1.pl",filePath],stdout=f)
#

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def collect(l,index):
    return map(itemgetter(index),l)

def splitSentences_nltk(text):
    from nltk import tokenize
    return tokenize.sent_tokenize(text)

def tag_sentToken(dirIn,dirOut):
        #create folder
    printHeadLine=True
    if os.path.exists(dirOut) == False:    
            os.mkdir(dirOut)
            
    #Explore Directories
    for dirname, dirnames, filenames in os.walk(dirIn):
        for filename in filenames:
            if filename.strip()[0]=='.' :
                continue
            f = os.path.join(dirname, filename)            
           # print "f: ",f
            oReport = aReport(f)

            oReport.orig2SentReport_method(splitSentences_nltk)
            #oReport.writeXMLReport("adfa")
            #oReport.reDupTag()
            
            ads=ds(oReport)
            dsCSV=ads.DS2CSV(printHeadLine)
            printHeadLine=False
            #####todo write to file
#             outName=os.path.join(dirOut,'time.csv')
#             fout=open(outName,'w')
#             fout.write(dsCSV)
#             fout.close()
            
            
    print 'files created'
    
def writeCSVFiles(dirIn,dir2014working, dirOut):
    #create folder
    printHeadLine=True
    if os.path.exists(dirOut) == False:    
            os.mkdir(dirOut)
            
    #Explore Directories
    for dirname, dirnames, filenames in os.walk(dirIn):
        for filename in filenames:
            if filename.strip()[0]=='.' :
                continue
            f = os.path.join(dirname, filename)            
           # print "f: ",f
            oReport = aReport(f)
            sentFileName=dir2014working+re.split('\.',filename)[0]+'.orig.sent'
            #print "sent: ",sentFileName
            
            oReport.orig2SentReport(sentFileName)
            oReport.tagSection()
            #oReport.orig2SentReport_method(splitSentences_nltk)
            #oReport.writeXMLReport("adfa")
            #oReport.reDupTag()
            
            ads=ds(oReport)
            dsCSV=ads.DS2CSV(printHeadLine)
            printHeadLine=False
            #####todo write to file
            outName=os.path.join(dirOut,'time.csv')
            fout=open(outName,'w')
            fout.write(dsCSV)
            fout.close()
            
            
    print 'files created'

#d = enchant.Dict("en_US")

#lambdas
#[\t\s\.,;:\(\)]+
# numbSpace = lambda s:len(re.split('[\t\s]+',s.strip()))-1 #number of space of string s
# wordPunctToken = lambda s:re.split('[\t\s\.,;:\(\)]+',s.strip())# return word list of string s

numbSpace = lambda s:len(nltk.word_tokenize(s.strip()))-1

#PunktWordTokenizer uses a regular expression to divide a text into tokens, leaving all periods attached to words, but separating off other punctuation:
punctWordToken = lambda s:PunktWordTokenizer().tokenize(s)
#Tokenize a text into a sequence of alphabetic and non-alphabetic characters, using the regexp \w+|[^\w\s]+
wordPunctToken = lambda s:WordPunctTokenizer().tokenize(s)
wordToken = lambda s:nltk.word_tokenize(s)
whitespaceToken = lambda s:WhitespaceTokenizer().tokenize(s)
removePunct = lambda s:''.join([i for i in s if i not in string.punctuation])


#removeLineBreak = lambda s:s.replace('\n',' ')


getETAttr = lambda e, s:e.get(s)  #return the value of attribute s of element e
getETTime = lambda e: getETAttr(e,'time')
getETStart = lambda e: int(getETAttr(e,'start'))
getETEnd = lambda e: int(getETAttr(e,'end'))
getETLineNum = lambda e: int(getETAttr(e,'lineNum'))

setETAttr = lambda e, s, v : e.set(s,str(v)) #set value of attribute s of element e
setETTime = lambda e,v: setETAttr(e,'time',v)
setETStart = lambda e,v: setETAttr(e,'start',v)
setETEnd = lambda e,v: setETAttr(e,'end',v)
setETLineNum = lambda e,v: setETAttr(e,'lineNum',v)

removeDuplicate = lambda l: list(OrderedDict.fromkeys(l))





#class
class Tag:
    type=''
    start=-1
    end=-1
    text=''
    comment=''
    treeNode=None
    lineNum=-1
    
    sec_id=''
    
    def __init__(self,start, end, text,comment,treeNode):
        self.start = start
        self.end = end
        self.text = text
        self.comment = comment
        self.treeNode=treeNode
        self.type=treeNode.tag
    
    def __eq__(self,other):
        if other==None:
            return False
        else:
            return self.start==other.start and self.end==other.end and self.lineNum==other.lineNum
    def __hash__(self):
        return hash((self.start,self.end,self.lineNum))
        
    
    def setStart(self,newStart):
        #print "old start: ",self.start
        self.start=newStart
        setETStart(self.treeNode,newStart)
    def setEnd(self,newEnd):
        #print "old end: ", self.end
        self.end=newEnd
        setETEnd(self.treeNode,newEnd)
    def setLineNum(self,lineNum):
        #print "lineNum: ",lineNum
        self.lineNum=lineNum
        setETLineNum(self.treeNode,lineNum)
    def setLineStartEnd(self,lineNum,newStart,newEnd):
        self.setLineNum(lineNum)
        self.setStart(newStart)
        self.setEnd(newEnd)
        
    def setSecID(self,secName):
        self.sec_id=secName
        self.treeNode.set('secName',secName)
        
        
#DIABETES CAD HYPERTENSION HYPERLIPIDEMIA OBESE  
class Tag_Disease(Tag):
    indicator=''
    time=''
    def __init__(self,start, end, text,comment,treeNode, indicator, time):
        Tag.__init__(self, start, end, text,comment,treeNode)
        self.indicator=indicator
        self.time=time
    def __eq__(self,other):
        return Tag.__eq__(self,other)and self.time==other.time
    def __hash__(self):
        return hash((self.start,self.end,self.lineNum,self.time))
 
class Tag_Medication(Tag):
    type1=''
    type2=''
    time=''
    def __init__(self, start, end, text,comment,treeNode, type1, type2, time):
        Tag.__init__(self, start, end, text,comment,treeNode)
        self.type1=type1
        self.type2=type2
        self.time=time
    def __eq__(self,other):
        return Tag.__eq__(self,other)and self.time==other.time
    def __hash__(self):
        return hash((self.start,self.end,self.lineNum,self.time))
    

class Tag_Smoke(Tag):
    status=''
    ## TODO

class Tag_Family(Tag):
    indicator=''
    ## TODO



class aReport:
    root=None
    text=''
    id=''
    dct=None
    tree_medications=None
    tree_obeses=None
    tree_diabetes=None
    tree_cad=None
    tree_hypertension=None
    tree_hyperlipidemia=None
    tree_smoke=None
    tree_family=None
    
    tree_secName=None
    
    tag_medications=[]
    tag_disease=[]
    tags=[]
    tag_secName=[]
    
    textLines=[]
    
    def __init__(self,fileName):
        self.id=os.path.basename(fileName)
        tree = ET.parse(fileName)
        self.root = tree.getroot() 
        #self.loadAReport() 
        
    def setXMLText(self,newText):
        #replace < with &lt
        self.root.find('TEXT').text=newText
    def setTextLines(self,newTextLines):
        self.textLines=newTextLines
        
    def setText(self,newText):
        self.text=newText
    
    def setText_lines(self,newText,newTextLine):
        self.setText(newText)
        self.setTextLines(newTextLine)
        
    def makeDiseaseTag(self,treeDisease):
        for subDisease in treeDisease:
            start=int(subDisease.get('start'))
            end=int(subDisease.get('end'))
            text=subDisease.get('text')
            comment=subDisease.get('comment')
            indicator=subDisease.get('indicator')
            time=subDisease.get('time')
        #(self, type, start, end, text,comment,treeNode, indicator, time)  
            tag_temp=Tag_Disease(start, end, text,comment,subDisease,indicator,time) 
            self.tag_disease.append(tag_temp) 
            self.tags.append(tag_temp)
    def makeMedicationTag(self,treeMedicaiton):
        for subMedication in treeMedicaiton:
            start=int(subMedication.get('start'))
            end=int(subMedication.get('end'))
            text=subMedication.get('text')
            comment=subMedication.get('comment')
            type1=subMedication.get('type1')
            type2=subMedication.get('type2')
            time=subMedication.get('time')
            #self, type,  start, end, text,comment,treeNode, type1, type2, time
            tag_temp=Tag_Medication(start,end,text,comment,subMedication,type1,type2,time)
            self.tag_medications.append(tag_temp)
            self.tags.append(tag_temp)  
            
    def getTagLine(self,tag):
        if tag.lineNum<0:
            return ""
        elif tag.lineNum<len(self.textLines):
            
            return self.textLines[tag.lineNum]
           # return ' '.join(whitespaceToken(self.textLines[tag.lineNum]))
        else: 
            return ''
           
        
    
    def getContextLine(self,tag,window):
        pass
    def getContextTag(self,tag,window):
        pass

    def getTagSentText(self,tag):
        return tag.text
    
    def reDupTag(self):
        self.tags=removeDuplicate(self.tags)
    def reDupMed(self):
        self.tag_medications=removeDuplicate(self.tag_medications)
    def reDupDisease(self):
        self.tag_disease=removeDuplicate(self.tag_disease)
        
    
    def getTagTense(self,tag):
        words=whitespaceToken(self.getTagLine(tag))
        print words, tag.start,tag.end, tag.text, ' '.join(words[tag.start:tag.end+1])
        return " ".join(words[tag.start:tag.end+1])
                
  
    def orig2SentReport(self,sentFileName):
        self.loadAReport()
        self.tree2Tag()
        self.alignTags_sentFile(sentFileName)
        
    def orig2SentReport_method(self,sentFunction):
        self.loadAReport()
        self.tree2Tag()
        self.alignTags_method(sentFunction)

    def writeXMLReport(self,outputName):
#         f=open(outputName,'w')
#         f.write(prettify(self.root))
#         f.close()
        
        print prettify(self.root)
          
    ##TODO add new tags for temporal expression, or PHI
    ##TODO do nothing to "SMOKER" and "FAMILY_HIST"
    def loadAReport(self):   
        self.text = self.root.find('TEXT').text
        self.dct=self.parseDCT()
        tags=self.root.find('TAGS')  
        self.tree_medications=tags.findall('MEDICATION')
        self.tree_obeses=tags.findall('OBESE')
        self.tree_diabetes=tags.findall('DIABETES')
        self.tree_cad=tags.findall('CAD')
        self.tree_hypertension=tags.findall('HYPERTENSION')
        self.tree_hyperlipidemia=tags.findall('HYPERLIPIDEMIA')
        self.tree_smoke=tags.findall('SMOKER')
        self.tree_family=tags.findall('FAMILY_HIST')
        
        self.textLines=self.text.splitlines()
        
    def parseDCT(self):
        sentences=self.text.splitlines()
        for aSen in sentences:
            aSen_trimed=aSen.strip().lower()
            if aSen_trimed.startswith('record date:'):
                m=re.search("\d",aSen_trimed)
                if m:
                    return aSen_trimed[m.start():]
                    
        print "file "+self.id+" different dct format"
        return ""
   

        
       
   ##TODO only have disease(diabetes, cad, hypertension, hyperlipidemia), medication
   ##TODO need to add ... 
    def tree2Tag(self):
        map(self.makeMedicationTag,self.tree_medications)
        map(self.makeDiseaseTag,self.tree_obeses)
        map(self.makeDiseaseTag,self.tree_diabetes)
        map(self.makeDiseaseTag,self.tree_cad)
        map(self.makeDiseaseTag,self.tree_hypertension)
        map(self.makeDiseaseTag,self.tree_hyperlipidemia)
        
        self.tags.sort(key=lambda x:x.start, reverse=False)
#         for tag in self.tags:
#             print prettify(tag.treeNode)
    
        
    def alignTags(self,sentLines):
        old_tagStart=-1
        old_tagEnd=-1
        pre_tag=None
        lineNum=0
        origOffset=0
        origTokens=[]
        origTokenOffset=0
        sentTokens=whitespaceToken(sentLines[lineNum])
        sentTokenOffset=0

#         for sent in sentLines:
#             print sent
        for aTag in self.tags:
#             print aTag.text
            if aTag.start==old_tagStart and aTag.end<=old_tagEnd:
                    aTag.setLineStartEnd(pre_tag.lineNum,pre_tag.start,pre_tag.end)
                    
            elif (aTag.start==old_tagStart and aTag.end>old_tagEnd):
                    tagTokens_pre=whitespaceToken(self.text[old_tagStart:old_tagEnd])
                    old_tagEnd=aTag.end
                    tagTokens=whitespaceToken(self.text[old_tagStart:old_tagEnd])
                    diff=len(tagTokens)-len(tagTokens_pre)
                    aTag.setLineStartEnd(lineNum,pre_tag.start,pre_tag.end+diff)
                    origOffset=old_tagEnd
                    sentTokenOffset+=diff
            elif (aTag.start>old_tagStart and aTag.start<old_tagEnd and aTag.end>old_tagEnd):
                pass         
            elif (aTag.start>old_tagStart and aTag.start<old_tagEnd and aTag.end<=old_tagEnd):
                pass      
            elif aTag.start>old_tagStart and aTag.end<=old_tagEnd:
                pass
                #aTag.setLineStartEnd(pre_tag.lineNum,pre_tag.start,pre_tag.end)
            else:
                old_tagStart=aTag.start
                old_tagEnd=aTag.end
                tagTokens=whitespaceToken(self.text[old_tagStart:old_tagEnd])
                origTokens=whitespaceToken(' '.join(splitSentences_nltk(self.text[origOffset:old_tagStart])))
#                 if origOffset>0:
#                     if self.text[origOffset-1].isalpha() and self.text[origOffset].isalpha():
#                         if len(origTokens)>0:
#                             origTokens=origTokens[1:]
#                         else:
#                             continue
                
                origTokenOffset=0
                
                while origTokenOffset<len(origTokens):
                    while sentTokenOffset>=len(sentTokens):
                        sentTokenOffset=sentTokenOffset-len(sentTokens)
                        lineNum+=1
                        if lineNum>=len(sentLines):
                            return
                        sentTokens=whitespaceToken(sentLines[lineNum])
                    
                    #print sentTokens,sentTokenOffset,aTag.text
                    if origTokens[origTokenOffset]==sentTokens[sentTokenOffset]:
                        origTokenOffset+=1
                        sentTokenOffset+=1
                        
                    else:
                        origTokenOffset+=1
#                         print "not match"
#                         print origTokens
#                         print sentTokens
#                         print origTokens[origTokenOffset]
#                         print sentTokens[sentTokenOffset]
#                         print aTag.text
#                         sys.exit()

                
                aTag.setLineStartEnd(lineNum,sentTokenOffset,sentTokenOffset+len(tagTokens)-1)
                origOffset=old_tagEnd
                sentTokenOffset+=len(tagTokens)
                
#                 print '==============',tagTokens              
            pre_tag=aTag
           
             

                
    def alignTags_sentFile(self,sentFilename):
        if len(self.tags)<=0:
            print 'no tags'
            return
        sentFile=open(sentFilename)
        sentText=sentFile.read()
        self.setXMLText(sentText)
        sentFile.close()
        sentLines=sentText.splitlines()
        self.alignTags(sentLines)
        self.textLines=sentLines
        self.text='\n'.join(sentLines)
        
    def alignTags_method(self,sentFunction):
        sentText=sentFunction(self.text)
        self.alignTags(sentText)
        
    def testAlign(self):
        for tag in self.tags:
            tagText=' '.join(whitespaceToken(self.textLines[tag.lineNum])[tag.start:tag.end+1])
            if removePunct(tagText)!=tag.text:
                print tagText,tag.text
                print self.textLines[tag.lineNum]

            else:
                print 'true'
            

    def addSecTag(self,lineIndex,line,secName):
        treeNode=ET.Element('SecIndicator')
        treeNode.set('lineNum',str(lineIndex))
        treeNode.set('text',line)
        treeNode.set('secName',secName)
        self.root.append(treeNode)
        aTag=Tag(0,0, line,'',treeNode)
        aTag.lineNum=lineIndex
        aTag.type=treeNode.tag
        aTag.sec_id=secName
        self.tag_secName.append(aTag)
        #self.tags.append(aTag)
        
        
    def tagSection(self,refFile='./sec_Names.txt'):
        secFile=open(refFile)
        secNames=secFile.read().splitlines()
        
        for lineIndex, line in enumerate(self.textLines):
            for sec in secNames:
                if sec.lower() in line.lower():
                    self.addSecTag(lineIndex,line,sec)
                    
        secTagIndex=0
        currSec='UNKNOWN'    
        for atag in self.tags:
            while secTagIndex<len(self.tag_secName) and atag.lineNum>=self.tag_secName[secTagIndex].lineNum:
                    currSec=self.tag_secName[secTagIndex].sec_id
                    secTagIndex+=1
            atag.setSecID(currSec)
            

        
        
        
        
        
        
                
            
#main

# dirIn=sys.argv[1]
# dirOut=sys.argv[2]
# #outName=sys.argv[3]
# dirIn='../data/Track2-RiskFactors/complete'
# #dirIn= '../data/training-RiskFactors-Complete-Set1'
# dirIn='../data/test'
# dirOut='../csv'
# 
# # oReport=aReport(dirIn+'/320-01.xml')
# # oReport.orig2SentReport_method(splitSentences_nltk)
# # oReport.tagSection()
# # oReport.writeXMLReport("adfa")
# 
# oReport=aReport(dirIn+'/320-01.xml')
# sentFilename=('../data/2014working/320-01.orig.sent')
# oReport.orig2SentReport(sentFilename)
# oReport.testAlign()
# oReport.tagSection()
# oReport.writeXMLReport("adfa")




# print "============="
# for tag in oReport.tags:
#    # print prettify(tag.treeNode)
#     #oReport.getTagSentText(tag)
#     print tag.text,oReport.getTagLine(tag)
    
# oReport.reDupTag()
# for tag in oReport.tags:
#     print prettify(tag.treeNode)
    
    
# ads=ds(oReport)
# ads.DS2CSV(True)
  
# print "============="    
# for drugTag in oReport.tag_medications:
#     print prettify(drugTag.treeNode)
# print "============="
# for diseaseTag in oReport.tag_disease:
#     print prettify(diseaseTag.treeNode)


# dir2014working='../data/2014working/'
# writeCSVFiles(dirIn,dir2014working,dirOut)

# print 'sss'
# dd=ds(None)
# dd.DS2CSV_dependency(dd)




    





