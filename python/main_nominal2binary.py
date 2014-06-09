import string
import os
import sys



from dataSet import ds
from sentTags import aReport



if __name__=="__main__":
    
    dd=ds(None)
    dd.DS2CSV_dependency(sys.argv[0])
