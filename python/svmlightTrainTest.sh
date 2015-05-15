#!/bin/sh

../libsvm-3.18/svm-train -t 0 -h 0 "${dirOut}after.data"  "${dirOut}after.model"


#software
dirSoftware=/home/sisi/i2b2P/svm-light-TK-1.2.1/

#training data
dirTrainData=/home/sisi/i2b2P/svmlightData/train/
#model
dirModel=/home/sisi/i2b2P/svmlightModel/train/

#test data
dirTestData=/home/sisi/i2b2P/svmlightData/test/
#test result
dirTestResult=/home/sisi/i2b2P/svmlightModel/test/

#mkdir
mkdir ${dirModel} ${dirTestData} ${dirTestResult}

#train models
for dataFile in `ls ${dirTrainData}`;do
    ${dirSoftware}svm_learn -t 5 "${dirTrainData}${dataFile}" "${dirModel}${dataFile}"
    arr=`echo ${dataFile} | cut -d '.' -f 1-2`
    testFileName="${arr}.test.data"
    ${dirSoftware}svm_classify "${dirTestData}${testFileName}" "${dirModel}${dataFile}"
done

#predict results




