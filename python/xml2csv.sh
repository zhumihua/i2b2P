#!/bin/sh
#dirIn=../data/Track2-RiskFactors/complete
#dirIn=../data/test
dirIn=../data/training-RiskFactors-Complete-Set1
dirOut=../csv
dir2014working=../data/2014working/

python2.7 main_xml2CSV1.py ${dirIn} ${dir2014working} ${dirOut}

#get dependency features
JAVA_DF_SRC=../i2b2Features/src/
JAVA_DF_LIB=../i2b2Features/lib/
JAVA_DF_BIN=../i2b2Features/bin/
JAVA_CP=${JAVA_DF_BIN}:${JAVA_DF_LIB}*:${JAVA_HOME}
JAVA_CLASS_NAME=DependencyFeatures


INCSVFILE=${dirOut}/time.csv
OUTCSVFILE=${dirOut}/time_depen.csv

make -C ${JAVA_DF_SRC}
java -cp ${JAVA_CP} ${JAVA_CLASS_NAME} "${INCSVFILE}" "${OUTCSVFILE}"

#nominal features to binary features
#during DCT	before DCT	after DCT	continuing
OUTDEPENDENCY=${dirOut}/dependency_pos.csv


python2.7 main_nominal2binary.py ${OUTCSVFILE} >${OUTDEPENDENCY}

#10-fold cross validation
python2.7 main_train_libsvm.py ${OUTDEPENDENCY}





