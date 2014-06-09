# Pipeline for 2014 i2b2 challenge
# RUN for each individual files
# RUN:
# python pipeline2014.py ../../2014working/  ../../2014tag-med/

import os,sys
import re

def main():

        inputDir = sys.argv[1]
        targetDir = sys.argv[2]

        MedNER = './Challenge_2014.py'

        for item in os.listdir(inputDir):
                if item.endswith('orig'):
                        orig = inputDir + '/' + item
                        sent = inputDir + '/' + item + '.sent'

                        cmd = 'python ' + MedNER + ' ' + orig + ' ' + sent + ' ' + targetDir
                        print cmd
                        os.system(cmd)

if __name__=="__main__":

        main()