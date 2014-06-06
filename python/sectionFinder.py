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
from sentTags import aReport
import nltk
from sentTags import punctWordToken


def headLineOfPara(text):
    paras=re.split('[\s*\n]{2,}',text)
    for para in paras:
        if para!='':
            sent = para.splitlines()[0]
            tokens=punctWordToken(sent)
            if ':' in tokens:
                tokens=tokens[:tokens.index(':')]
            if '(' in tokens:
                tokens=tokens[:tokens.index('(')]
            if len(tokens)<4:
                print ' '.join(tokens)
                print
             
        #print para
#     tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
#     tokenizer.tokenize(text)

def getHeadLines(dirIn,dirOut):
    for dirName,dirNames,fileNames in os.walk(dirIn):
        for filename in fileNames:
            if filename.strip()[0]=='.':
                continue
            f = os.path.join(dirName,filename)
            print "f: ",f
            oReport=aReport(f)
            oReport.loadAReport()
            headLineOfPara(oReport.text)
            
dirIn='../data/Track2-RiskFactors/complete'
dirIn='../data/training-RiskFactors-Complete-Set1'
dirOut='../csv'
getHeadLines(dirIn,dirOut)