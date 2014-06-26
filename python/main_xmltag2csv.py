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


    
def xml2tagcsv(dirIn,dirOut):
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
            oReport.loadReport_tags()
            oReport.tagSection()
            oReport.make_df_tags()
            oReport.print_df_csv

            
            
    print 'files created'

    
if __name__=="__main__":
    dirIn = sys.argv[1]
    dirOut=sys.argv[2]
    xml2tagcsv(dirIn,dirOut)
    

