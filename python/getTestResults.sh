#!/bin/sh
#predict ouput xml files finalOUtput
predictXML="../xml/"
rm ${predictXML}*
mkdir ${predictXML}

#dirTestIn=/data/i2b2/2014i2b2/src/dev_output/
dirTestIn=/data/i2b2/2014i2b2/data/training-RiskFactors-Complete-Set2/
#dirTestIn=/data/i2b2/2014i2b2/data/training-RiskFactors-Complete-Set1/
#dirTestIn=/data/i2b2/2014i2b2/data/Track2-RiskFactors/complete
#dirTestIn=../data/Track2-RiskFactors/complete/
dirTestToEx=../csv/i2b2timeTagTest/

rm ${dirTestToEx}*
mkdir ${dirTestToEx}
python2.7 main_xmltag2csvTest.py ${dirTestIn} ${dirTestToEx}


cd ../../CTAKES/apache-ctakes-3.1.1-src/ctakes-clinical-pipeline/

#use ctakes to generate xmi files

cd ../ctakes-core
mvn -Dmaven.test.skip=true install
cd ../ctakes-type-system
mvn install
cd ../ctakes-clinical-pipeline

argOutput=/data/i2b2/2014i2b2/tools/CTAKES/data/outputTest/
rm ${argOutput}*
mkdir /data/i2b2/2014i2b2/tools/CTAKES/data/outputTest
mvn clean compile -PrunClinicalPipeline -DargInput=/home/sisi/i2b2P/csv/i2b2timeTagTest/  -DargOutput=/data/i2b2/2014i2b2/tools/CTAKES/data/outputTest/

#use ctakes to extract features
outputDS=/data/i2b2/2014i2b2/tools/CTAKES/data/testdsOutput/
rm ${outputDS}*
mkdir /data/i2b2/2014i2b2/tools/CTAKES/data/testdsOutput/
mvn clean compile -PrunGetDataset -DinputXMI=/data/i2b2/2014i2b2/tools/CTAKES/data/outputTest/ -DoutputDS=/data/i2b2/2014i2b2/tools/CTAKES/data/testdsOutput/


cd ~/i2b2P/python/
dirCtakesOut=../../CTAKES/data/testdsOutput/
dirDataSetTestOut=../csv/test/
rm ${dirDataSetTestOut}*

mkdir ${dirCtakesOut}
mkdir ${dirDataSetTestOut}

#ctakes result to dataSet.py

python2.7 TestDs.py ${dirCtakesOut} ${dirDataSetTestOut}



#models
continueModel="../csv/continue.model"
beforeModel="../csv/before.model"
duringModel="../csv/during.model"
afterModel="../csv/after.model"

#pridict
predictContinue="../csv/pre_continue/"
predictBefore="../csv/pre_before/"
predictDuring="../csv/pre_during/"
predictAfter="../csv/pre_after/"

rm ${predictContinue}*
rm ${predictBefore}*
rm ${predictDuring}*
rm ${predictAfter}*
mkdir ${predictContinue}
mkdir ${predictBefore}
mkdir ${predictDuring}
mkdir ${predictAfter}

#make libsvm
cd ../libsvm-3.18/
make clean
make
cd ../python



for dataFile in `ls ${dirDataSetTestOut}`;do
../libsvm-3.18/svm-predict  "${dirDataSetTestOut}${dataFile}"  "${continueModel}" "${predictContinue}${dataFile}"
../libsvm-3.18/svm-predict  "${dirDataSetTestOut}${dataFile}"  "${beforeModel}" "${predictBefore}${dataFile}"
../libsvm-3.18/svm-predict  "${dirDataSetTestOut}${dataFile}"  "${duringModel}" "${predictDuring}${dataFile}"
../libsvm-3.18/svm-predict  "${dirDataSetTestOut}${dataFile}"  "${afterModel}" "${predictAfter}${dataFile}"
done

#predict ouput xml files
#predictXML="../xml/"
#mkdir ${predictXML}

python2.7 main_predictTime.py ${dirTestIn} ${predictXML} ${predictContinue} ${predictBefore} ${predictDuring} ${predictAfter}