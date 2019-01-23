#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import itertools as it
import re
from optparse import OptionParser

def count_mora( pron ):
    nonMoraList = set(u"ァ ィ ゥ ェ ォ ャ ュ ョ".split())
    index_mora = 0
    mora = []
    for p in pron.decode("utf-8"):
        if p not in nonMoraList:
            mora.append(p.encode("utf-8"))
            index_mora += 1
        else:
            mora[index_mora-1] += p.encode("utf-8")
    return len(mora)
                                                                
usage = u"""usage: %prog labelfile resultfile
アクセント句境界を推定した結果のファイル（labelfile）、
アクセント核を推定した結果のファイル（resultfile）から
アクセント句ごとにアクセント核位置を書いたファイルに変換する
"""
parser = OptionParser(usage=usage)
(options,args) = parser.parse_args()

if len(args) < 2:
    print >> sys.stderr, "Error: too few arguments\n"
    parser.print_help()
    exit()
labelfile, resultfile = map(open, args[0:2])

resultlines = resultfile.readlines()

# resultfile の何行目を呼んでいるかの counter
count = 0

buf_orth = ""
buf_pron = ""
accent = 0
nmora = 0

for line in labelfile:

    elems = line.strip().split()

    # アクセント句境界もしくは空行の場合はデータを出力、初期化
    if (len(elems) < 1 or elems[3] == "/") and len(buf_pron) > 0:

        print buf_orth,
        print buf_pron,
        print nmora,
        print accent

        buf_orth = ""
        buf_pron = ""
        accent = 0
        nmora = 0

        # resultfile の方は、アクセント句境界ごとに空行が入っている
        count += 1
        
        # 空行の場合は、さらに改行して次へ
        if len(elems) < 1:
            print
            continue

    # データを読んで更新

    # 発音がないものは、resultfile には書かれていないので
    # buf_orth だけ更新して continue する（count や nmora を増やさない）
    if elems[1] == "*":
        buf_orth += elems[0]
        continue

    # アクセントの推定結果を読み、accent を更新。
    # ただし、一つ目のアクセント核しか利用しない。
    resultelems = resultlines[ count ].strip().split()
    if accent == 0 and resultelems[-1] != "0":
        accent = int(resultelems[-1]) + nmora
    # 読んだので、カウンターを回す
    count += 1

    # その他のデータの更新
    buf_orth += elems[0]
    buf_pron += elems[1]
    nmora += count_mora( elems[1] )

