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

from sentTags import aReport


def com2xmls(dirIn1,dirInName2,dirOut):
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
            f2=os.path.join(dirInName2,filename)           
           # print "f: ",f
            oReport = aReport(f)
            oReport.loadReport_tags()
            
            report2=aReport(f2)
            report2.loadReport_tags()
            
            outf=os.path.join(dirOut,fileName)
            outFile=codecs.open(outf,'w','utf-8')
            oReport.writeXMLReport(outFile)
            outFile.close()
            print outFileName

            
            
    print 'files created'

    
if __name__=="__main__":
    dirIn = sys.argv[1]
    dirIn2= sys.argv[2]
    dirOut=sys.argv[3]
    com2xmls(dirIn,dirIn2,dirOut)
    

