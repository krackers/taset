#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser

# ""で囲まれたものを除くコンマ区切り形式（csv形式）の string を分割する
def csvsplit( string ):
    quote_flag = 0
    buf = ""
    outlist = []
    for letter in string:
        if letter == '"':
            if quote_flag == 0:
                quote_flag = 1
            else:
                quote_flag = 0
        elif letter == "," and quote_flag == 0:
            outlist.append( buf )
            buf = ""
        else:
            buf += letter
    outlist.append( buf )
    return outlist
        
usage = u"""usage: %prog featurefile 
cabocha -O2 の output（featurefile）を整形する"""
parser = OptionParser(usage=usage)
(options,args) = parser.parse_args()

if len(args) < 1:
    print >> sys.stderr, "Error: too few arguments\n"
    parser.print_help()
    exit()

# cabocha -O2 で出力したファイルを読む
featurefile = open( args[0] )

# 文節境界は、featurefile の * で始まる行で表される。
# bunsetsu_flag == "-" で境界なし、"/" で境界ありを示す。
bunsetsu_flag = "-"

for line in featurefile:

    # タブで区切る
    features = line.strip("\n").split("\t")

    if len(features) == 1 and features[0] == "EOS":
        # End Of Sentence なら空行を出力
        print
    elif len(features) == 1 and features[0][0] == "*":
        # 文節境界ならフラグをたてる
        bunsetsu_flag = "/"
    else:
        # データ行
        
        # cabocha -O2 のメイン部分のデータ（csv形式）を読む
        f = csvsplit( features[1] )

        for ii in range(0,len(f)):
            # なにもデータが入っていないものには "*" を入力する
            if f[ii] == "": f[ii] = "*"
        
        if len(f) == 25:
            # 0.orth, 1.pron, 2.pos1-pos2-pos3-pos4, 3.cType, 4.cForm, 5.lemma-lForm,
            # 6.goshu, 7.iType-iForm-iConType, 8.aType, 9.aConType, 10.aModType,
            # 11.IREX, 12 bunsetsu
            # 　と、なるように print する。
            print "%s %s %s-%s-%s-%s %s %s %s-%s %s %s-%s-%s %s %s %s %s %s" \
                  % (f[8],f[9],f[0],f[1],f[2],f[3],f[4],f[5],f[7],f[6],f[11], \
                     f[16],f[17],f[18],f[22],f[23],f[24],features[2],bunsetsu_flag)
        else:
            # 情報がすべて含まれないもの（OOV）だったら、適当な値をいれておく
            print "o o o-o-o-o o o o-o o-o-o o o-o o o o"

        # 文節境界フラグをもとに戻す
        bunsetsu_flag = "-"
