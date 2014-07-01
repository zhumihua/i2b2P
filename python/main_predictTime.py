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


from sentTags import aReport


def predictTime(dirIn,dirOut,dirContinue,dirBefore,dirDuring,dirAfter):
        #create folder
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
            oReport.loadReport_tags()
            oReport.predictTimes(dirContinue,dirBefore,dirDuring,dirAfter)
            outFileName=dirOut+re.split('\.',oReport.id)[0]+'.xml'
            outFile=open(outFileName,'w')
            oReport.writeGOLDXML(outFile)
            outFile.close()
            print outFileName

            
            
    print 'files created'

    
if __name__=="__main__":
    dirIn = sys.argv[1]
    dirOut=sys.argv[2]
    dirContinue=sys.argv[3]
    dirBefore=sys.argv[4]
    dirDuring=sys.argv[5]
    dirAfter=sys.argv[6]
    
    predictTime(dirIn,dirOut,dirContinue,dirBefore,dirDuring,dirAfter)
    

