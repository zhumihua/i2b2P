#!/bin/sh
dirTestIn=../data/Track2-RiskFactors/complete/
dirTestToEx=../csv/i2b2timeTagTest/

mkdir ${dirTestToEx}
python2.7 main_xmltag2csv.py ${dirTestIn} ${dirTestToEx}


cd ../../CTAKES/apache-ctakes-3.1.1-src/ctakes-clinical-pipeline/

#use ctakes to generate xmi files

cd ../ctakes-core
mvn -Dmaven.test.skip=true install
cd ../ctakes-type-system
mvn install
cd ../ctakes-clinical-pipeline
mkdir /data/i2b2/2014i2b2/tools/CTAKES/data/outputTest
mvn clean compile -PrunClinicalPipeline -DargInput=/home/sisi/i2b2P/csv/i2b2timeTagTest/  -DargOutput=/data/i2b2/2014i2b2/tools/CTAKES/data/outputTest/

#use ctakes to extract features
mkdir /data/i2b2/2014i2b2/tools/CTAKES/data/testdsOutput/
mvn clean compile -PrunGetDataset -DinputXMI=/data/i2b2/2014i2b2/tools/CTAKES/data/outputTest/ -DoutputDS=/data/i2b2/2014i2b2/tools/CTAKES/data/testdsOutput/


cd ~/i2b2P/python/
dirCtakesOut=../../CTAKES/data/testdsOutput/
dirDataSetTestOut=../csv/test/

mkdir ${dirCtakesOut}
mkdir ${dirDataSetTestOut}

#ctakes result to dataSet.py

python2.7 TestDS.py ${dirCtakesOut} ${dirDataSetTestOut}



#models
continueModel="../csv/continue.model"
beforeModel="../csv/before.model"
duringModel="../csv/during.model"
afterModel="../csv/after.model"

#pridict
predictContinue="../csv/pre_continue.ret"
predictBefore="../csv/pre_before.ret"
predictDuring="../csv/pre_during.ret"
predictAfter="../csv/pre_after.ret"

../libsvm-3.18/svm-predict  "${dirDataSetTestOut}continue.data"  "${continueModel}" "${predictContinue}"
../libsvm-3.18/svm-predict  "${dirDataSetTestOut}before.data"  "${beforeModel}" "${predictBefore}"
../libsvm-3.18/svm-predict  "${dirDataSetTestOut}during.data"  "${duringModel}" "${predictDuring}"
../libsvm-3.18/svm-predict  "${dirDataSetTestOut}after.data"  "${afterModel}" "${predictAfter}"