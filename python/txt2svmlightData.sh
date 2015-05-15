#!/bin/sh
#dirIn=../data/Track2-RiskFactors/complete
#dirIn=../data/test
dirIn=/data/i2b2/2014i2b2/tools/CTAKES/data/dsOutput/
testDirIn=/data/i2b2/2014i2b2/tools/CTAKES/data/testdsOutput/
dirOut=../svmlightData/


python2.7 dataSetSVMLight.py ${dirIn} ${dirOut} ${testDirIn}



