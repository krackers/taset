#!/bin/bash

# ここを適切に変更してください#############
voice="/home/suzuki/src/MMDAgent_Example-1.1/Voice/mei_normal"
dic="/home/suzuki/src/open_jtalk-1.05/mecab-naist-jdic"
###########################################

mkdir -p jtalk_out

s=1
tmpfile=$(mktemp)
for line in $(cat in/jnas_test.txt); do

    echo $line > $tmpfile
    open_jtalk -s 48000 -p 240 -a 0.55 \
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
	-x  $dic \
	-ot jtalk_out/s$s.trace \
	-ow jtalk_out/s$s.wav \
	$tmpfile
    ./trace2lab.py jtalk_out/s$s.trace > jtalk_out/s$s.lab

    s=$(($s+1))
done
