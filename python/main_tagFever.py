import string
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys
import time
from datetime import date
import re
from collections import OrderedDict
from operator import itemgetter

import codecs

from docx import Document

from lxml import etree

import zipfile
import pandas as pd
import csv
import json

import collections
from enum import Enum

#FEVER_TIME
#FEVER
#Patient #1

class Tag:
    def __init__(self,start,end,text):
        self.start=start
        self.end=end
        self.text=text
        
    def __eq__(self,other):
        return self.start==other.start and self.end==other.end
    
    def __key__(self):
        return (self.start,self.end)
    
    def __hash__(self):
        return hash(self.__key__())
    #start within the aTag offset, 
    #or end within the aTag offset
    def within(self,aTag):
        if (self.start>=aTag.start and self.start<aTag.end) or \
         (self.end>aTag.start and self.end<=aTag.end):
            return True
        else:
            return False
    def overlap(self,aTag):
        if (self.end>aTag.start and self.start<=aTag.start) or \
        (self.start>=aTag.start and self.start<aTag.end) :
           # print aTag.text, self.text
            return True
        else:
            return False
                
class TagSent(Tag):
    def __init__(self,start, end, text):
        Tag.__init__(self, start, end, text)
        self.l_times=[]
        self.l_fevers=[]
    def hasHyper(self):
        keyWords='(if|whether|as needed|given)'
        patterns=unicode(keyWords)
        matches=re.compile(patterns,re.U)
        if matches.search(self.text.lower()) is None:
            return False
        else:
            return True

    def hasNeg(self):
        keyWords='(fever\s*\W*\s*none|negative for fever|scarlet fever|rocky mountain spotted fever|fever free|fever resolved)'
        patterns=unicode(keyWords)
        matches=re.compile(patterns,re.U)
        if matches.search(self.text.lower()) is None:
            return False
        else:
            return True
class TagTime(Tag):
#     def __init(self,start,end,text,timex3_value):
#         Tag.__init__(self, start, end, text);
#         self.value=timex3_value

    def __init__(self,start,end,text):
        Tag.__init__(self, start, end, text);
        
    def setTimexValue(self,timexinsance,timextype,timexvalue,timexquant,timexreq,timexmod):
        self.timexinsance=timexinsance
        self.timextype=timextype
        self.timexvalue=timexvalue
        self.timexquant=timexquant
        self.timexreq=timexquant
        self.timexmod=timexmod
       # print self.text,self.timextype,self.timexvalue

        
  
class TagFever(Tag):
    def __init__(self,start, end, text):
        Tag.__init__(self, start, end, text)
        self.curr_sent=None#TagSent
        self.q_preSents=[]
        self.q_nextSents=[]
        self.time=None#TagTime
        
        self.q_preTimes=[]
        self.q_nextTimes=[]
        self.curr_time=[]
    def __eq__(self,other):
        return self.start==other.start and self.end==other.end
    
    def __key__(self):
        return (self.start,self.end)
    
    def __hash__(self):
        return hash(self.__key__())
        
        
class Med_notes:
    def __init__(self,note_text):
        self.note_text=note_text
        self.l_fevers=[]
        self.l_sents=[]
        self.l_times=[]
        self.l_pers=[]
        self.pd_fever_tags=None
        self.pd_fever_json=None
        


    def initSentTags(self,sentFName):
        #{START,END,TEXT}
        with open(sentFName,'rb') as csvfile:
            sentReader=csv.reader(csvfile)
            for row in sentReader:
                start=int(row[0])
                end=int(row[1])
                text=row[2]
                self.l_sents.append(TagSent(start,end,text))
    
    def initTimeTags(self,timeFName):
        #enum MED_TIME_HEADER{START,END,TIMEXINSANCE,TIMEXTYPE,TIMEXVALUE,TIMEXQUANT,TIMEXFREQ,TIMEXMOD}
        with open(timeFName,'rb') as csvfile:
            timeReader=csv.reader(csvfile)
            for row in timeReader:
                start=int(row[0])
                end=int(row[1])
                timexinsance=row[2]
                timextype=row[3]
                timexvalue=row[4]
                timexquant=row[5]
                timexreq=row[6]
                timexmod=row[7]
                
                tagtime=TagTime(start,end,self.note_text[start:end])
                tagtime.setTimexValue(timexinsance,timextype,timexvalue,timexquant,timexreq,timexmod)
                self.l_times.append(tagtime)
                


    def initSent_time_fever(self):
        i_time=0
        i_fever=0
        for sent in self.l_sents:
            while i_time<len(self.l_times) and self.l_times[i_time].within(sent):
                    sent.l_times.append(self.l_times[i_time])
                    i_time+=1
            while i_fever<len(self.l_fevers) and self.l_fevers[i_fever].within(sent):
                    sent.l_fevers.append(self.l_fevers[i_fever])
                    i_fever+=1
    
    def initFever_context_time(self,n):
        x=len(self.l_sents)
        for index,sent in enumerate(self.l_sents):
            for fever in sent.l_fevers:
                for i in range(1,n+1):
                    if index-i in range(0,x) and len(self.l_sents[index-i].l_fevers)<1:
                        fever.q_preTimes.extend(self.l_sents[index-i].l_times)
                        fever.q_preSents.append(self.l_sents[index-i])
                    else:
                        break
                for i in range(1,n+1):
                    if index+i in range(0,x) and len(self.l_sents[index+i].l_fevers)<1:
                        fever.q_nextTimes.extend(self.l_sents[index+i].l_times)
                        fever.q_nextSents.append(self.l_sents[index+i])
                    else:
                        break

                fever.curr_time=sent.l_times
                fever.curr_sent=sent
                
        
    def resolveNeg(self):
        for fever in self.l_fevers[:]:
            sents=[]
            sents.append(fever.curr_sent)
          #  sents.extend(fever.q_preSents)
          #  sents.extend(fever.q_nextSents)
            isNeg=False
            for sent in sents:
                isNeg|=sent.hasNeg()
            if len(fever.q_nextSents)>0:
                if fever.q_nextSents[0].text.strip().lower().startswith('none'):
                    isNeg=True
            if isNeg:
                self.l_fevers.remove(fever)
                self.l_pers.append(fever)
    def resolveHyper(self):
        for fever in self.l_fevers[:]:
            sents=[]
            sents.append(fever.curr_sent)
#             sents.extend(fever.q_preSents)
#             sents.extend(fever.q_nextSents)
            isHyper=False
            for sent in sents:
                isHyper|=sent.hasHyper()
            if isHyper:
                self.l_fevers.remove(fever)
                self.l_pers.append(fever)
            



#there might be overlap of context between adjacent FEVER_TAG
#if multiple FEVER in one sentence, only get the first FEVER context
#     def initFever_contexts(self,n):
#         if self.l_fevers is not None and len(self.l_fevers)>0:
#             i=0
#             pre_fever=None
#             fever=self.l_fevers[i]
#             fever.q_preSents=collections.deque(maxlen=n)
#             fever.q_nextSents=collections.deque(maxlen=n)
#             for sent in self.l_sents:
#                 if fever is not None and fever.within(sent):
#                    # print sent.text
#                     fever.curr_sent=sent
#                     ##next fever
#                     pre_fever=fever
#                     i+=1
#                     if i<len(self.l_fevers):
#                         fever=self.l_fevers[i]
#                         fever.q_preSents=collections.deque(maxlen=n)
#                         fever.q_nextSents=collections.deque(maxlen=n)
#                     else:
#                         fever=None
#                 else:
#                     if fever is not None:
#                         fever.q_preSents.append(sent)
#                     if pre_fever is not None and len(pre_fever.q_nextSents)<n:
#                         pre_fever.q_nextSents.append(sent)
            

            
    def resovleFever_time(self):
        for fever in self.l_fevers:
            pre_times=fever.q_preTimes
            next_times=fever.q_nextTimes
            this_times=fever.curr_time
            
            if len(this_times)>0:
                fever.time=findNearestTime(fever,this_times)
            elif len(pre_times)>0:
                fever.time=pre_times[-1]
            elif len(next_times)>0:
                fever.time=next_times[0] 

#             pre_times.extend(this_times)
#             pre_times.extend(next_times)
#             fever.time=findNearestTime(fever,pre_times)
            if fever.time is None:
                print fever.text,"****"
                if fever.curr_sent is not None:
                    print fever.curr_sent.text,'***'
                    for time in fever.curr_sent.l_times:
                        print time.text,"-----"

#     def resovleFever_time(self):
#         for fever in self.l_fevers:
#             pre_times=[]
#             next_times=[]
#             if fever.curr_sent is not None:
#                 this_times=fever.curr_sent.l_times
#             else:
#                 this_times=[]
#             for sent in fever.q_preSents:
#                 pre_times.extend(sent.l_times)
#             for sent in fever.q_nextSents:
#                 next_times.extend(sent.l_times)
#             if len(this_times)>0:
#                 fever.time=findNearestTime(fever,this_times)
#             elif len(pre_times)>0:
#                 fever.time=pre_times[-1]
#             elif len(next_times)>0:
#                 fever.time=next_times[0] 
#             if fever.time is None:
#                 print fever.text,"****"
#                 if fever.curr_sent is not None:
#                     print fever.curr_sent.text,'***'
            
    #38C (100F)
    #39C (102F) and in many cases .40C (104F)  
    #http://www.regular-expressions.info/numericranges.html
    def tagFevers(self):
        xx=self.note_text
        x=self.note_text
        x=x.lower()
        keyWords='(fever|\bfebrile|chill|low-grade|low grade|fuo)'
        temp='(temp|temperature|temp of|temperature of|around|tm|tmax)'
        
        nc=u'([3][8](\.[0-9])?|[4][0-9](\.[0-9])?)\s*(\u00B0|\u00B0c)?'
        dc=u'\W([3][8](\.[0-9])?|[4][0-9](\.[0-9])?)\s*(\u00B0|\u00B0c)'  
        tc=unicode(temp+'\s*'+'([3][9](\.[0-9])?|[4][0-9](\.[0-9])?)\s*(\u00B0)?\b')   
        
        nf=u'([1]0[0-9](\.[0-9])?)\s*(\u00B0|\u00B0f)?'
        df=u'([1]0[0-9](\.[0-9])?)\s*(\u00B0|\u00B0f)'
        tf=unicode(temp+'\s*'+'([1]0[2-9](\.[0-9])?)\s*(\u00B0)?')
    
          
        cTemp='('+tc+'|'+dc+')'
        fTemp='('+tf+'|'+df+')'
        cRange='('+tc+'|'+dc+')'+'(\W+|\s*to\s*)'+'('+tc+'|'+dc+'|'+nc+')'
        fRange='('+tc+'|'+dc+')'+'(\W+|\s*to\s*)'+'('+tf+'|'+df+'|'+nf+')'
        
        
        
        patterns=unicode(keyWords+'|'+cTemp+'|'+fTemp+'|'+cRange+'|'+fRange)
        matches=re.compile(patterns,re.U).finditer(x)
        for aM in matches:
            start=aM.start()
            end=aM.end()
            text=unicode(xx[start:end])
            self.l_fevers.append(TagFever(start,end,text))
            
        
    #     cNum=ur'([1]0[2-9](\.[0-9])?)(\u00B0)?f?'
    #     mNum=re.compile(cNum,re.U).finditer(x)
    #     for aM in mNum:
    #         start=aM.start()
    #         end=aM.end()
    #         aM.string[:start]
    #         aM.string[end:]

    def initPd_fever(self):
        texts=[]
        starts=[]
        ends=[]
        for atag in self.l_fevers:
            texts.append(atag.text.encode("ascii","ignore"))
            starts.append(atag.start)
            ends.append(atag.end)
        
        headNames=['b_text','a_start','a_end']
        columnValues=[ texts,starts,ends]
        adict=dict(zip(headNames, columnValues))
        
        self.pd_fever_tags=pd.DataFrame(adict)
    def initPd_fever_json(self):
        starts=[]
        ends=[]
        
        for atag in self.l_fevers:
            starts.append(atag.start)
            ends.append(atag.end)
        headNames=['start','end']
        columnValues=[starts,ends]
        adict=dict(zip(headNames, columnValues))
        self.pd_fever_json=pd.DataFrame(adict)
        types=['FEVER']*len(feverTags)
        self.pd_fever_json['type']=pd.Series(types)
        
    def print_fever_csv(self,file):
        self.initPd_fever()
        self.pd_fever_tags.to_csv(file,sep=',',quoting=csv.QUOTE_ALL,index=False)
            
    def print_fever_json(self,file):
        self.initPd_fever_json()
        file.write('{\"tags\":')
        self.pd_fever_tags.to_json(file,orient='records')
        file.write('}')
            
    def print_fever_html(self,file):
        COLOR=['red', 'blue', 'orange', 'violet', 'green']
        i=0
        output = '''<!DOCTYPE html>
                    <html>
                    <head><title></title></head>
                    <body>'''
        for m in self.l_fevers:
            output+="".join([self.note_text[i:m.start],
                           "<strong><span style='color:%s'>" % COLOR[0],
                           self.note_text[m.start:m.end],
                           "</span></strong>"])
            i = m.end
        htmlContents=unicode("".join([output, self.note_text[m.end:], "</body></html>"]))
        contentx='<br />'.join(htmlContents.split("\n"))
        file.write(contentx)
    
    def print_fever_bratAnn(self,outAnn,outTxt):
        outTxt.write(self.note_text)
        
        for index, aTag in enumerate(self.l_fevers):
            aline='T'+str(index)+'\t'+'PER'+' '+str(aTag.start)+' '+str(aTag.end)+'\t'+aTag.text+'\n'
            outAnn.write(aline)
            
            
    def print_json(self,outJson):
        
        starts=[]
        ends=[]
        types=[]
        
        for atag in self.l_fevers:
            starts.append(atag.start)
            ends.append(atag.end)
            types.append('FEVER')
            
            if atag.time is not None:
                starts.append(atag.time.start)
                ends.append(atag.time.end)
                types.append('FEVER_TIME')

        headNames=['start','end','type']
        columnValues=[starts,ends,types]
        adict=dict(zip(headNames,columnValues))
        
        pd_fever_json=pd.DataFrame(adict)

        outJson.write('{\"tags\":')
        pd_fever_json.to_json(outJson,orient='records')
        outJson.write('}')
        
    
    def print_bratAnn(self,outAnn,outTxt):
        outTxt.write(self.note_text)
        
        index=0
        index_rel=0
        for aTag in self.l_fevers:
            feverIndex='T'+str(index)
            aline=feverIndex+'\t'+'FEVER'+' '+str(aTag.start)+' '+str(aTag.end)+'\t'+aTag.text+'\n'
            outAnn.write(aline)
            index+=1
            
            if aTag.time is not None:
                timeIndex='T'+str(index)
                aline=timeIndex+'\t'+'FEVER_TIME'+' '+str(aTag.time.start)+' '+str(aTag.time.end)+'\t'+aTag.time.text+'\n'
                outAnn.write(aline)
                index+=1
    
                aline='R'+str(index_rel)+'\t'+'REL'+' Arg1:'+timeIndex+' '+'Arg2:'+feverIndex+'\n'
                outAnn.write(aline)
                index_rel+=1
        
        for aTag in set(self.l_pers):
            negFever='T'+str(index)
            aline=negFever+'\t'+'PER'+' '+str(aTag.start)+' '+str(aTag.end)+'\t'+aTag.text+'\n'
            outAnn.write(aline)
            index+=1
              
                
#         for aTag in self.l_times:
#             timeIndex='T'+str(index)
#             aline=timeIndex+'\t'+'PER'+' '+str(aTag.start)+' '+str(aTag.end)+'\t'+aTag.text+'\n'
#             outAnn.write(aline)
#             index+=1
            
            

        
            
    def outBrat(self,outTxtName,outAnnName):
        outAnn=codecs.open(outAnnName,'w','utf-8')
        outTxt=codecs.open(outTxtName,'w','utf-8')
        self.print_bratAnn(outAnn,outTxt)
        outAnn.close()
        outTxt.close()
        print outAnnName, outTxtName
        
    def outJson(self,outJsonName):
        outJson=codecs.open(outJsonName,'w','utf-8')
        self.print_json(outJson)
        outJson.close()
        print outJsonName
        
#find the nearest timeTag in the list
#thisTag and nearest tag in list l_tags
#using "start"
def findNearest(thisTag,l_tags):
    if len(l_tags)<1:
        return None
    if len(l_tags)==1:
        return l_tags[0]
       
    oldTag=l_tags[0]
    oldDiff=thisTag.start-oldTag.start
    for atag in l_tags:
        diff=thisTag.start-atag.start
        if oldDiff*diff<=0:
            a=abs(thisTag.start-oldTag.end)
            b=abs(thisTag.start-atag.start)
            if a>b:
                return atag
            else:
                return oldTag
        else:
            oldTag=atag
            oldDiff=diff            

#if the timeTag is needed or not
#return false, if type is SET and Value start with RP or Value == R; or type is Time
def isTimeValue(timeTag):
    if timeTag.timextype=='TIME' or \
    (timeTag.timextype=='SET' and timeTag.timexvalue=='R') or \
    (timeTag.timextype=='SET' and timeTag.timexvalue.startswith('RP')):
        return False
    else:
        return True
    
    
    
    
#find the nearest timeTag, remove type set
def findNearestTime(thisTag,l_tags):
    
    if len(l_tags)<1:
        return None
    if len(l_tags)==1:
        return l_tags[0]
    
    oldTag=l_tags[0]
    oldDiff=thisTag.start-oldTag.start
    for atag in l_tags[:]:
        if isTimeValue(atag) and not thisTag.overlap(atag):
            diff=thisTag.start-atag.start
            if oldDiff*diff<=0:
                a=abs(thisTag.start-oldTag.end)
                b=abs(thisTag.start-atag.start)
                if a>b:
                    return atag
                else:
                    return oldTag
            else:
                oldTag=atag
                oldDiff=diff
        else:
            l_tags.remove(atag)
            atag=None
            diff=sys.maxint
    return oldTag if abs(oldDiff)<=abs(diff) else atag
        

        
    
    
    
    
    
def resolveFName(dirname,fileName,suffix):
    dotP=fileName.rfind('.')
    fileName=fileName[0:dotP]+"."+suffix
    fileName1=fileName.replace("%20"," ")
    fileName2=fileName.replace(" ","%20")
    fullName1=os.path.join(dirname, fileName1)
    fullName2=os.path.join(dirname,fileName2)

    if os.path.isfile(fullName1):
        return fullName1
    elif os.path.isfile(fullName2):
        return fullName2
    else:
        return fullName1
    
   

    
def getFever_Time(dirIn,dirInSent,dirInTime,dirOut,dirOutJson,dirOuthtml,dirOutBrat):

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
            x=''
            file=codecs.open(f,'r','utf-8')
            x=file.read()
            file.close()
            mNotes=Med_notes(x)
            mNotes.tagFevers()
            sentFName=resolveFName(dirInSent,filename,'csv')
            mNotes.initSentTags(sentFName)
            timeFName=resolveFName(dirInTime,filename,'csv')
            mNotes.initTimeTags(timeFName)
            mNotes.initSent_time_fever()
            n=1
            
            mNotes.initFever_context_time(n)
            mNotes.resovleFever_time()
            mNotes.resolveNeg()
            mNotes.resolveHyper()
            
            
            outTxtBrat=resolveFName(dirOutBrat,filename,'txt')
            outAnnBrat=resolveFName(dirOutBrat,filename,'ann')
            mNotes.outBrat(outTxtBrat,outAnnBrat)
            
            outJson=resolveFName(dirOutJson,filename,'txt')
            mNotes.outJson(outJson)
            
         
    
def getFeverTags(dirIn1,dirOut,dirOutJson,dirOutHtml,dirOutBrat):
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
            x=''
            file=codecs.open(f,'r','utf-8')
            x=file.read()
            file.close()
            mNotes=Med_notes(x)
            mNotes.tagFevers()
            #feverTags=

            ###############################
            outName=re.split('\.',filename)[0]+'.csv'
            outf=os.path.join(dirOut,outName)
            outFile=open(outf,'w')
            mNotes.print_fever_csv(outFile,pd_fever_tags)
            outFile.close()
            print outName
            
            ###############################
            

            
            outName=re.split('\.',filename)[0]+'.txt'
            outf=os.path.join(dirOutJson,outName)
            outFile=open(outf,'w')
            mNotes.print_fever_json(outFile,pd_fever_json)
            outFile.close()
            print outName
            
            ###############################
            
            outName=re.split('\.',filename)[0]+'.html'
            outf=os.path.join(dirOutHtml,outName)
            outFile=codecs.open(outf,'w','utf-8')
            mNotes.print_fever_html(outFile)
            outFile.close()
            print outName
            
            
            ###############################
            
            outFNameAnn=re.split('\.',filename)[0]+'.ann'
            outFNameTxt=re.split('\.',filename)[0]+'.txt'
            outAnnName=os.path.join(dirOutBrat,outFNameAnn)
            outTxtName=os.path.join(dirOutBrat,outFNameTxt)
            outAnn=codecs.open(outAnnName,'w','utf-8')
            outTxt=codecs.open(outTxtName,'w','utf-8')
            mNotes.print_fever_bratAnn(outAnn,outTxt)
            outAnn.close()
            outTxt.close()
            print outFNameAnn, outFNameTxt
            


            
            
    print 'files created'

    
if __name__=="__main__":
#      dirIn = sys.argv[1]
#      dirIn2= sys.argv[2]
#      dirOut=sys.argv[3]
#      doc2text(dirIn,dirOut)

    
    dirIn= 'kd_data_text'
    dirOut = 'kd_fever'
    dirOutJson = 'kd_fever_json'
    dirOuthtml='kd_fever_html'
    dirOutBrat='kd_fever_brat'
    
    dirIn= sys.argv[1]
    dirInSent=sys.argv[2]
    dirInTime=sys.argv[3]
    dirOut = sys.argv[4]
    dirOutJson = sys.argv[5]
    dirOuthtml=sys.argv[6]
    dirOutBrat=sys.argv[7]
    
    getFever_Time(dirIn,dirInSent,dirInTime,dirOut,dirOutJson,dirOuthtml,dirOutBrat)
    
   # getFeverTags(dirIn,dirOut,dirOutJson,dirOuthtml,dirOutBrat)



