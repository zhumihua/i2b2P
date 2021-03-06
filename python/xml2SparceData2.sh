#!/bin/sh
#dirIn=../data/Track2-RiskFactors/complete
#dirIn=../data/test
dirIn=../data/training-RiskFactors-Complete-Set1
dirOut=../csv/separateDS
dir2014working=../data/2014working/

mkdir ${dirOut}

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
OUTDEPENDENCY1=${dirOut}/dependency_pos1.csv
OUTDEPENDENCY2=${dirOut}/dependency_pos2.csv
OUTDEPENDENCY3=${dirOut}/dependency_pos3.csv
OUTDEPENDENCY4=${dirOut}/dependency_pos4.csv
OUTDEPENDENCY5=${dirOut}/dependency_pos5.csv
OUTDEPENDENCY6=${dirOut}/dependency_pos6.csv
OUTDEPENDENCY7=${dirOut}/dependency_pos7.csv

python2.7 main_nominal2binary.py ${OUTCSVFILE} >${OUTDEPENDENCY}

python2.7 main_separateDataset.py $OUTDEPENDENCY $OUTDEPENDENCY1 $OUTDEPENDENCY2 $OUTDEPENDENCY3 $OUTDEPENDENCY4 $OUTDEPENDENCY5 $OUTDEPENDENCY6 $OUTDEPENDENCY7

LIBSVMDATA1=${dirOut}/dependency_pos1.data
LIBSVMDATA2=${dirOut}/dependency_pos2.data
LIBSVMDATA3=${dirOut}/dependency_pos3.data
LIBSVMDATA4=${dirOut}/dependency_pos4.data
LIBSVMDATA5=${dirOut}/dependency_pos5.data
LIBSVMDATA6=${dirOut}/dependency_pos6.data
LIBSVMDATA7=${dirOut}/dependency_pos7.data
#csv to libsvm sparce matrix
python2.7 main_csv2libsvm.py $OUTDEPENDENCY1 $LIBSVMDATA1
python2.7 main_csv2libsvm.py $OUTDEPENDENCY2 $LIBSVMDATA2
python2.7 main_csv2libsvm.py $OUTDEPENDENCY3 $LIBSVMDATA3
python2.7 main_csv2libsvm.py $OUTDEPENDENCY4 $LIBSVMDATA4
python2.7 main_csv2libsvm.py $OUTDEPENDENCY5 $LIBSVMDATA5
python2.7 main_csv2libsvm.py $OUTDEPENDENCY6 $LIBSVMDATA6
python2.7 main_csv2libsvm.py $OUTDEPENDENCY7 $LIBSVMDATA7

#10-fold cross validation using libsvm command line
make clean -C ../libsvm-3.18/
make -C ../libsvm-3.18/
#../libsvm-3.18/svm-train -t 0 -v 10 -h 0 $LIBSVMDATA1 > ${dirOut}/result1.txt
#../libsvm-3.18/svm-train -t 0 -v 10 -h 0 $LIBSVMDATA2 > ${dirOut}/result2.txt
#../libsvm-3.18/svm-train -t 0 -v 10 -h 0 $LIBSVMDATA3 > ${dirOut}/result3.txt
#../libsvm-3.18/svm-train -t 0 -v 10 -h 0 $LIBSVMDATA4 > ${dirOut}/result4.txt

../libsvm-3.18/svm-train -t 0 -v 10 -h 0  -w1 1 -w-1 1 $LIBSVMDATA1 > ${dirOut}/result_before.txt
../libsvm-3.18/svm-train -t 0 -v 10 -h 0 -w1 1 -w-1 1 $LIBSVMDATA2 > ${dirOut}/result_during.txt
../libsvm-3.18/svm-train -t 0 -v 10 -h 0 -w1 1 -w-1 1  $LIBSVMDATA3 > ${dirOut}/result_after.txt

../libsvm-3.18/svm-train -t 0 -v 10 -h 0 $LIBSVMDATA4 > ${dirOut}/result_continue.txt

../libsvm-3.18/svm-train -t 0 -v 10 -h 0 $LIBSVMDATA5 > ${dirOut}/result_before_during.txt
../libsvm-3.18/svm-train -t 0 -v 10 -h 0 $LIBSVMDATA6 > ${dirOut}/result_before_after.txt
../libsvm-3.18/svm-train -t 0 -v 10 -h 0 $LIBSVMDATA7 > ${dirOut}/result_during_after.txt







