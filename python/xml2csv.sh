#!/bin/sh
dirIn=../data/Track2-RiskFactors/complete
dirIn=../data/test
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
OUTDEPENDENCY_1=${dirOut}/dependency_pos1.csv
OUTDEPENDENCY_2=${dirOut}/dependency_pos2.csv
OUTDEPENDENCY_3=${dirOut}/dependency_pos3.csv
OUTDEPENDENCY_4=${dirOut}/dependency_pos4.csv


python2.7 main_nominal2binary.py ${OUTCSVFILE} >${OUTDEPENDENCY}

#csv to libsvm format
LIBSVMDATA_1=${dirOut}/dependency_pos1.dat
LIBSVMDATA_2=${dirOut}/dependency_pos2.dat
LIBSVMDATA_3=${dirOut}/dependency_pos3.dat
LIBSVMDATA_4=${dirOut}/dependency_pos4.dat

python2.7 main_separateLables.py ${OUTDEPENDENCY} ${OUTDEPENDENCY_1} ${OUTDEPENDENCY_2} ${OUTDEPENDENCY_3} ${OUTDEPENDENCY_4}

python2.7 main_csv2libsvm.py ${OUTDEPENDENCY_1} ${LIBSVMDATA_1} 0 0
python2.7 main_csv2libsvm.py ${OUTDEPENDENCY_2} ${LIBSVMDATA_2} 0 0
python2.7 main_csv2libsvm.py ${OUTDEPENDENCY_3} ${LIBSVMDATA_3} 0 0
python2.7 main_csv2libsvm.py ${OUTDEPENDENCY_4} ${LIBSVMDATA_4} 0 0

#separate csv
#train
#test





