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

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def addAllfiles(dirIn,dirOut):
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
            tree = ET.parse(f)
            root=tree.getroot()
            smokeTag=root.find('TAGS').find('SMOKER')
            smokeTag.set("start","0")
            smokeTag.set("end","0")
            outFileName=dirOut+filename
            outFile=codecs.open(outFileName,'w','utf-8')
            outFile.write(prettify(root))
            outFile.close()
            print outFileName

    print 'files created'

    
if __name__=="__main__":
    dirIn = sys.argv[1]
    dirOut=sys.argv[2]
    addAllfiles(dirIn,dirOut)
    

