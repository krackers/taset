#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import itertools as it
from optparse import OptionParser

usage = u"""usage: %prog resultfile labelfile
crf_test の出力ファイルと正解ラベルファイルから正解率を出す"""
parser = OptionParser(usage=usage)

(options,args) = parser.parse_args()

if len(args) < 1:
    print >> sys.stderr, "Error: too few arguments\n"
    parser.print_help()
    exit()

resultfile = open( args[0] )

# recall, precisionを計算する．

# すべてのカウント
count = 0
# 句境界が有ると推定された数
Ncorrect = 0
# 正しい句境界の数
Nboundary = 0
# 句境界が有ると推定され，かつ本当に句境界が有った場合
Ncorrect_correct = 0

for resultline in resultfile:
    if len(resultline.strip()) == 0:
        continue
    hyp, ans = resultline.split()[-1], resultline.split()[-2]

    # 発音形の無いもの（読まないもの）はカウントしない．
    if resultline.split()[1] == "*":
        continue
    if hyp == "/":
        Ncorrect += 1
    if ans == "/":
        Nboundary += 1
    if ans == "/" and hyp == "/":
        Ncorrect_correct +=1
    count += 1

recall = 100.0*(Ncorrect_correct)/ Nboundary
precision = 100.0*(Ncorrect_correct) / Ncorrect
Fmeasure = 2 * recall * precision / ( recall + precision)

print "すべて:%d/%d->%d：正答数:%d, 脱落誤り:%d, 挿入誤り:%d, Recall:%f, Precision:%f, F値:%f" \
      % ( Nboundary, count, Ncorrect, Ncorrect_correct, \
          Nboundary - Ncorrect_correct, \
          Ncorrect - Ncorrect_correct, \
          recall, precision, Fmeasure)

# -------------------------
# 名詞連続部分に関する集計
# -------------------------


count = 0
# 句境界が有ると推定された数
Ncorrect = 0
# 正しい句境界の数
Nboundary = 0
# 句境界が有ると推定され，かつ本当に句境界が有った場合
Ncorrect_correct = 0

renoun = re.compile("^名詞-")

prev_is_noun = False
curr_is_noun = False

resultfile.seek(0)
for resultline in resultfile:

    if len(resultline.strip()) == 0:
        prev_is_noun = False
        curr_is_noun = False
        continue

    pos, hyp, ans = resultline.split()[2], resultline.split()[-1], resultline.split()[-2]

    if renoun.search(pos) is not None:
        curr_is_noun = True
    else:
        curr_is_noun = False

    if curr_is_noun and prev_is_noun:
        # 発音形の無いもの（読まないもの）はカウントしない．
        if resultline.split()[1] == "*":
            continue
        if hyp == "/":
            Ncorrect += 1
        if ans == "/":
            Nboundary += 1
        if ans == "/" and hyp == "/":
            Ncorrect_correct +=1
        count += 1

    prev_is_noun = curr_is_noun

recall = 100.0*(Ncorrect_correct) / Nboundary
if Ncorrect == 0: 
    precision = 0.0
    Fmeasure = 0.0
else: 
    precision = 100.0*(Ncorrect_correct) / Ncorrect
    Fmeasure = 2 * recall * precision / ( recall + precision)

print "名詞連続:%d/%d->%d：正答数:%d, 脱落誤り:%d, 挿入誤り:%d, Recall:%f, Precision:%f, F値:%f" \
      % ( Nboundary, count, Ncorrect, Ncorrect_correct, \
          Nboundary - Ncorrect_correct, \
          Ncorrect - Ncorrect_correct, \
          recall, precision, Fmeasure)

