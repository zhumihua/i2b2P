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


from dataSet import ds
from sentTags import aReport

import codecs

    
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
            fout=codecs.open(outName,'w','utf-8')
            fout.write(dsCSV)
            fout.close()
            
            
    print 'files created'
    
if __name__=="__main__":
    dirIn = sys.argv[1]
    dir2014working = sys.argv[2]
    dirOut=sys.argv[3]
    writeCSVFiles(dirIn,dir2014working, dirOut)
    

