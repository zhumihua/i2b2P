#!/bin/sh


dirBase="/home/sisi/i2b2P/python"
dirInText="${dirBase}/kd_data_text/"
dirSentIn="${dirBase}/kd_sent_csv/"
dirTimeIn="${dirBase}/kd_time_csv/"
dirOut="${dirBase}/kd_fever/"
dirOutJson="${dirBase}/kd_fever_json/"
dirOuthtml="${dirBase}/kd_fever_html/"
dirOutBrat="${dirBase}/kd_fever_brat/"


rm -rf  ${dirOut}  ${dirOutJson} ${dirOuthtml}  ${dirOutBrat}

mkdir ${dirOut}  ${dirOutJson} ${dirOuthtml}  ${dirOutBrat}

python2.7 main_tagFever.py ${dirInText} ${dirSentIn} ${dirTimeIn} ${dirOut} ${dirOutJson} ${dirOuthtml} ${dirOutBrat}

#scp -P 9221 ${dirOutBrat}* ss@idash-phnds-dev:/data/tools/brat-v1.3_Crunchy_Frog/data/test/kd_fever_brat/.




