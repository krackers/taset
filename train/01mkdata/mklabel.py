#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import itertools as it
from optparse import OptionParser

usage = u"""usage: %prog datafile labelfile
形態素解析 or 読みが間違っているものを取り除く
mkdata.py の出力をラベルに変えただけのプログラム"""
parser = OptionParser(usage=usage)
(options,args) = parser.parse_args()

if len(args) < 2:
    print >> sys.stderr, "Error: too few arguments\n"
    parser.print_help()
    exit()

datafile, labelfile = map(open, args[0:2])

# 使えるデータか使えないデータかのフラグ。
# 形態素の区切りと読みが、label.txt と一致したら使える。ずれていたら使えない。
useflag = 1

# 文（とラベルデータ）を保存するバッファ
sentence = ""

# データはここで全部読んでおく
labellines = labelfile.readlines()
datalines = datafile.readlines()

# labellines, datalines のどこを呼んでいるかを示すカウンタ
label_count = -1
feature_count = -1

# labellines, datalines どちらか最後まで読むまで続ける
while( label_count+2 <= len(labellines) and feature_count+2 <= len(datalines) ):

    # label も feature もカウンタを回す
    label_count += 1
    feature_count += 1

    # データを読む
    labelline = labellines[label_count].strip()
    dataline = datalines[feature_count].strip()
    
    if len(labelline) == 0 or len(dataline) == 0:
        # どちらかが空行（EOS）だったとき

        # labelline も dataline もどちらも EOS まで読み進める。
        # ズレがなければ、len(labelline) も len(dataline) も 0 になっている。
        # ズレがあるなら、useflag = 0 となる。
        while( len(labelline) != 0 ):
            label_count += 1
            labelline = labellines[label_count].strip()
            useflag = 0
        while( len(dataline) != 0 ):
            feature_count += 1
            dataline = datalines[feature_count].strip()
            useflag = 0

        # この時点で useflag == 1 なら、使える sentence なので、print する
        if useflag == 1:
            print sentence

        # 初期化して次の行へ。sentence を空に、 useflag を 1 にする。
        sentence = ""
        useflag = 1
    else:
        # データがある場合
        
        # 書字形, 【正しい】発音形, 文内正解アクセント, 文内正解アクセント句境界
        orth, pron, accent, boundary = labelline.split()
        
        # 0.orth, 1.pron, 2.pos1-pos2-pos3-pos4, 3.cType, 4.cForm, 5.lemma-lForm,
        # 6.goshu, 7.iType-iForm-iConType, 8.aType, 9.aConType, 10.aModType,
        # 11.IREX, 12 bunsetsu
        # 　と、いう順で dataline にかかれている。
        features = dataline.split()
        
        # cabocha による発音形（features[1]）と、正しい発音形 pron が違う場合、
        # useflag を 0 に。後にデータは破棄される。
        if not features[1] == pron:
            useflag = 0

        # ラベルのデータを sentence に書く
        for f in orth, pron, accent, boundary:
            sentence += f + " "
        sentence += "\n"
