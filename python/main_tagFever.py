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
    #start within the aTag offset, 
    #or end within the aTag offset
    def within(self,aTag):
        if self.start<=aTag.start and self.start>aTag.end:
            return True
        elif self.end<=aTag.start and self.end>=aTag.end:
            return True
        else:
            return False
                
class TagSent(Tag):
    def __init__(self,start, end, text):
        Tag.__init__(self, start, end, text)
        self.l_times=[]
        self.l_fevers=[]
class TagTime(Tag):
#     def __init(self,start,end,text,timex3_value):
#         Tag.__init__(self, start, end, text);
#         self.value=timex3_value

    def __init(self,start,end,text):
        Tag.__init__(self, start, end, text);
        self.value=None

class Timex3():
    pass
        
  
class TagFever(Tag):
    def __init__(self,start, end, text):
        Tag.__init__(self, start, end, text)
        self.curr_sent=None#TagSent
        self.q_preSents=None#deque
        self.q_nextSents=None#deque
        self.time=None#TagTime
        
class Med_notes:
    def __init__(self,note_text):
        self.note_text=note_text
        self.l_fevers=[]
        self.l_sents=[]
        self.l_times=[]
        self.pd_fever_tags=None
        self.pd_fever_json=None
        


    def initSentTags(self,sentFName):
        #{START,END,TEXT}
        with open(sentFName,'rb') as csvfile:
            sentReader=csv.reader(csvfile)
            for row in sentReader:
                start=row[0]
                end=row[1]
                text=row[3]
                self.l_sents.append(TagSent(start,end,text))
    
    def initTimeTags(self,timeFName):
        #enum MED_TIME_HEADER{START,END,TIMEXINSANCE,TIMEXTYPE,TIMEXVALUE,TIMEXQUANT,TIMEXFREQ,TIMEXMOD}
        with open(timeFName,'rb') as csvfile:
            timeReader=csv.reader(csvfile)
            for row in timeReader:
                start=row[0]
                end=row[1]
                timexinsance=row[2]
                timextype=row[3]
                timexvalue=row[4]
                timexquant=row[5]
                timexreq=row[6]
                timexmod=row[7]
                self.l_times.append(TagTime(start,end,self.note_text[start,end]))
                


    def initSent_time_fever(self):
        i_time=0
        i_fever=0
        for sent in self.l_sents:
            if i_time<len(self.l_times):
                if self.l_times[i_time].within(sent):
                    sent.l_times.append(self.l_times[i_time])
                    i_time+=1
            if i_fever<len(self.l_fevers):
                if self.l_fevers[i_fever].within(sent):
                    sent.l_fevers.append(self.l_fevers[i_fever])
                    i_fever+=1
           

#there might be overlap of context between adjacent FEVER_TAG
#if multiple FEVER in one sentence, only get the first FEVER context
    def initFever_contexts(self,n):
        if self.l_fevers is not None and len(self.l_fevers)>0:
            i=0
            pre_fever=None
            fever=self.l_fevers[i]
            fever.q_preSents=collections.deque(maxlen=n)
            fever.q_nextSents=collections.deque(maxlen=n)
            for sent in self.l_sents:
                if fever is not None and fever.within(sent):
                    fever.curr_sent=sent
                    ##next fever
                    pre_fever=fever
                    i+=1
                    if i<len(self.l_fevers):
                        fever=self.l_fevers[i]
                        fever.q_preSents=collections.deque(maxlen=n)
                        fever.q_nextSents=collections.deque(maxlen=n)
                    else:
                        fever=None
                else:
                    if fever is not None:
                        fever.q_preSents.append(sent)
                    if pre_fever is not None and len(pre_fever.q_nextSent)<n:
                        pre_fever.q_nextSent.append(sent)
            
        
    def resolveNeg(self):
        pass
    
    def resovleFever_time(self):
        for fever in self.l_fevers:
            pre_times=[]
            next_times=[]
            for sent in fever.q_preSents:
                pre_times.extend(sent.l_times)
            for sent in fever.q_nextSents:
                next_times.extend(sent.l_times)
            if len(pre_times)>0:
                fever.time=pre_times[-1]
            elif len(next_time)>0:
                fever.time=next_time[0]       
            
    
    #39C (102F) and in many cases .40C (104F)  
    #http://www.regular-expressions.info/numericranges.html
    def tagFevers(self):
        xx=self.note_text
        x=self.note_text
        x=x.lower()
        keyWords='(fever|febrile|chill|low-grade|low grade|fuo)'
        temp='(temp|temperature|temp of|temperature of|around|tm|tmax)'
        
        dc=u'\W([3][9](\.[0-9])?|[4][0-9](\.[0-9])?)\s*(\u00B0)?c\b'  
        tc=unicode(temp+'\s*'+'([3][9](\.[0-9])?|[4][0-9](\.[0-9])?)\s*(\u00B0)?\b')   
        
        df=u'([1]0[2-9](\.[0-9])?)\s*(\u00B0)?f'
        tf=unicode(temp+'\s*'+'([1]0[2-9](\.[0-9])?)\s*(\u00B0)?')
    
        b='\b'
        
        
    #     cTemp=b+c+b
    #     fTemp=b+f+b
    #     cRange=b+c+'.'+c+b
    #     fRange=b+f+'.'+f+b
        
    #     cTemp=b+tc+b
    #     fTemp=b+tf+b
    #     cRange=b+tc+'.'+tc+b
    #     fRange=b+tf+'.'+tf+b
    
        cTemp='('+tc+'|'+dc+')'
        fTemp='('+tf+'|'+df+')'
        cRange=tc+'\W'+'('+tc+'|'+dc+')'
        fRange=tf+'\W'+'('+tf+'|'+df+')'
        
        
        
        patterns=unicode(keyWords+'|'+cTemp+'|'+fTemp+'|'+cRange+'|'+fRange)
        matches=re.compile(patterns,re.U).finditer(x)
        for aM in matches:
            start=aM.start()
            end=aM.end()
            text=xx[start:end]
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
                aline=timeIndex+'\t'+'FEVER_TIME'+' '+str(aTag.time.start)+' '+str(aTag.time.start)+'\t'+aTag.time.text+'\n'
                outAnn.write(aline)
            index+=1
            
            if aTag.time is not None:
                aline='R'+str(index_rel)+'\t'+'REL'+' Arg1:'+timeIndex+' '+'Arg2:'+feverIndex+'\n'
                outAnn.write(aline)
            index+=1
            

        
            
    def outBrat(self,outTxtName,outAnnName):
        outAnn=codecs.open(outAnnName,'w','utf-8')
        outTxt=codecs.open(outTxtName,'w','utf-8')
        mNotes.print_bratAnn(outAnn,outTxt)
        outAnn.close()
        outTxt.close()
        print outFNameAnn, outFNameTxt
        
            

    
def resolveFName(dir,fileName,suffix):
    dotP=fileName.rfind('.')
    fileName=fileName[0:dotP]+"."+suffix
    fileName1=fileName.replace("%20"," ")
    fileName2=fileName.repalce(" ","%20")
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
            sentFName=resolveFName(dirInSent,fileName,'csv')
            mNotes.initSentTags(sentFName)
            timeFName=resolveFName(dirInTime,fileName,'csv')
            mNotes.initTimeTags(timeFName)
            mNotes.initSent_time_fever()
            n=1
            mNotes.initFever_contexts(n)
            mNotes.resovleFever_time()
            
            outTxtBrat=resolveFName(dirOutBrat,fileName,'txt')
            outAnnBrat=resolveFName(dirOutBrat,fileName,'ann')
            mNotes.outBrat(outTxtBrat,outAnnBrat)
         
    
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



