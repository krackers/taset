#!/bin/bash

#ここは適切に変えて下さい#################################
voice=/home/suzuki/src/MMDAgent_Example-1.1/Voice/mei_normal
dic=/home/suzuki/src/open_jtalk-1.05/mecab-naist-jdic
##########################################################

for file in convertedlab/*.lab; do
    hts_engine -s 48000 -p 240 -a 0.55 \
	-td $voice/tree-dur.inf \
	-tm $voice/tree-mgc.inf \
	-tf $voice/tree-lf0.inf \
	-md $voice/dur.pdf \
	-mm $voice/mgc.pdf \
	-mf $voice/lf0.pdf \
	-dm $voice/mgc.win1 \
	-dm $voice/mgc.win2 \
	-dm $voice/mgc.win3 \
	-df $voice/lf0.win1 \
	-df $voice/lf0.win2 \
	-df $voice/lf0.win3 \
	-em $voice/tree-gv-mgc.inf \
	-ef $voice/tree-gv-lf0.inf \
	-cm $voice/gv-mgc.pdf \
	-cf $voice/gv-lf0.pdf \
	-k  $voice/gv-switch.inf \
	-ow $(echo $file | sed -e "s;convertedlab;out;g" -e "s;\.lab;\.wav;g") \
	$file
done
