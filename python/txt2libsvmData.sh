#!/bin/sh
#dirIn=../data/Track2-RiskFactors/complete
#dirIn=../data/test
dirIn=/data/i2b2/2014i2b2/tools/CTAKES/data/dsOutput/
dirOut=../csv/


python2.7 dataSet.py ${dirIn} ${dirOut}

../libsvm-3.18/svm-train -t 0 -v 10 -h 0 ${dirOut}continue.data > ${dirOut}result_continue.txt


