#!/bin/sh
#dirIn=../data/Track2-RiskFactors/complete
#dirIn=../data/test
dirIn=/data/i2b2/2014i2b2/tools/CTAKES/data/dsOutput/
dirOut=../csv/


python2.7 dataSet.py ${dirIn} ${dirOut}
cd ../libsvm-3.18/
make clean
make
cd ../python
../libsvm-3.18/svm-train -t 0 -v 10 -h 0 "${dirOut}continue.data" > "${dirOut}result_continue.txt"
../libsvm-3.18/svm-train -t 0 -v 10 -h 0 "${dirOut}before.data" > "${dirOut}result_before.txt"
../libsvm-3.18/svm-train -t 0 -v 10 -h 0 "${dirOut}during.data" > "${dirOut}result_during.txt"
../libsvm-3.18/svm-train -t 0 -v 10 -h 0 "${dirOut}after.data" > "${dirOut}result_after.txt"


../libsvm-3.18/svm-train -t 0 -h 0 "${dirOut}continue.data"  "${dirOut}continue.model"
../libsvm-3.18/svm-train -t 0 -h 0 "${dirOut}before.data"  "${dirOut}before.model"
../libsvm-3.18/svm-train -t 0 -h 0 "${dirOut}during.data"  "${dirOut}during.model"
../libsvm-3.18/svm-train -t 0 -h 0 "${dirOut}after.data"  "${dirOut}after.model"


