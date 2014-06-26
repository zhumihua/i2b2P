#!/bin/sh
#dirIn=../data/Track2-RiskFactors/complete
#dirIn=../data/test
dirIn=../data/training-RiskFactors-Complete-Set1/
dirOut=../csv/i2b2timeTag/

mkdir ${dirOut}

python2.7 main_xmltag2csv.py ${dirIn} ${dirOut}







