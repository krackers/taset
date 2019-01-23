#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import itertools as it
import re
from optparse import OptionParser

usage = u"""usage: %prog resultfile
アクセント型推定の結果集計
crfの出力ファイルから正解率を出す．"""
parser = OptionParser(usage=usage)
(options,args) = parser.parse_args()

if len(args) < 1:
    print >>sys.stderr, "error: too few arguments\n"
    parser.print_help()
    exit()

resultfile = open(args[0])

#総形態素
Nmorph = 0
#正解形態素
Ncorrect = 0
#アクセント句正解判定フラグ
flag = 0
#単純なアクセント句フラグ
fsimple = 0
#名詞連続フラグ
fnoun = 0
fnoun_ok= 0
#総アクセント句
#Nphrase = -1
Nphrase = 0
#正解アクセント句
#Ncorrectp = -1
Ncorrectp = 0
#単純なアクセント句
simple = 0
#正解した単純なアクセント句
simplecorrect = 0
#名詞連続
noun = 0
#名詞連続の正解
nouncorrect = 0
#主核フラグ，主核正解フラグ
fcore=0
corecorrect=0
#主核のみの正解数
correct_core=0
nouncorrect_core=0
simplecorrect_core=0

#アクセント句をいれるリスト
resultplist = [] 

#エラーアクセント句の数
errorc = 0

p1 = re.compile('名詞')
p2 = re.compile('動詞')
p3 = re.compile('形容詞')
p4 = re.compile('形状詞')
q1 = re.compile('助詞')
q2 = re.compile('助動詞')

i=0
boundary_flag = 0

for resultline in resultfile:
    if len(resultline.strip()) == 0:
        boundary_flag = 1
        continue

    hyp, ans, hinsi = resultline.split()[-1], resultline.split()[-2], resultline.split()[2]

    # 発音形の無いもの（読まないもの）はカウントしない．
    if resultline.split()[1] == "*":
        continue
    #アクセント句境界がきたとき
    if boundary_flag == 1:
        boundary_flag = 0
        #単純なアクセント句
        if fsimple == 2:
            if corecorrect == 1:
                simplecorrect_core += 1
            if flag == 0 and fcore == 0:
                simplecorrect_core += 1
            if flag == 0:
                simplecorrect += 1
            simple += 1
        fsimple = 0
        
        #名詞連続
        if fnoun_ok == 1:
            if corecorrect == 1:
                nouncorrect_core += 1
            if flag == 0 and fcore == 0:
                nouncorrect_core += 1 
            if flag == 0:
                nouncorrect += 1
            noun += 1
        fnoun_ok=0
        fnoun=0

        #アクセント句中の核が全て合っていたら(flag==0の場合)正解
        if flag == 0:
            Ncorrectp += 1
        Nphrase += 1

        if corecorrect == 1:
            correct_core += 1
        elif flag == 0 and fcore == 0:
            correct_core += 1
        else:
            errorc += 1

        corecorrect = 0
        fcore=0
        flag = 0
        resultplist=[]
        
        #単純なアクセント句か判定
        if p1.match(hinsi) is not None or p2.match(hinsi) is not None or p3.match(hinsi) is not None or p4.match(hinsi) is not None:
            fsimple = 1

    #アクセント句境界でない場合
    else:
        if fsimple == 1:
            if q1.match(hinsi) is not None or q2.match(hinsi) is not None:
                fsimple=2
            else:
                fsimple=0
        else:
            fsimple=0

    #名詞句連続があるか判定
    if p1.match(hinsi) is not None:
        if fnoun == 0:
            fnoun = 1
        elif fnoun == 1:
            fnoun_ok = 1    
    else:
        fnoun=0

    #形態素単位で正解判定
    if hyp == ans:
        Ncorrect += 1
    else:
        flag = 1
    Nmorph += 1
    
    #当該形態素が主核か判定。更に正解しているか判定
    if hyp != 0:
        fcore += 1
        if hyp == ans and fcore == 1:
            corecorrect=1
    resultplist.append(resultline)
        
#最後のアクセント句用
if corecorrect == 1:
    correct_core += 1
elif flag == 0 and fcore == 0:
    correct_core += 1
else:
    errorc+=1

if flag == 0:
    Ncorrectp += 1
Nphrase += 1

if fsimple == 2:
    if corecorrect == 1:
        simplecorrect_core += 1
    if flag == 0 and fcore == 0:
        simplecorrect_core += 1
    if flag == 0:
        simplecorrect += 1
    simple += 1

if fnoun_ok == 1:
    if corecorrect == 1:
        nouncorrect_core += 1
    if flag == 0 and fcore == 0:
        nouncorrect_core += 1
    if flag == 0:
        nouncorrect += 1
    noun += 1


print "正答数:%d, 総形態素数:%d, 正解率:%f%%," \
      % (Ncorrect, \
         Nmorph, \
         100.0 * Ncorrect / Nmorph)

print "総アクセント句数:%d, 正解アクセント句数:%d, 正解率:%f%%" \
      % (Nphrase, \
         Ncorrectp, \
         100.0 * Ncorrectp / Nphrase)

print "単純なアクセント句総数:%d, 正解した単純なアクセント句:%d, 正解率:%f%%" \
      % (simple, \
         simplecorrect, \
         100.0 * simplecorrect / simple)

print "名詞連続総数:%d, 正解した名詞連続:%d, 正解率:%f%%" \
      % (noun, \
         nouncorrect, \
         100.0 * nouncorrect / noun)

print "主核正解(全て):%d, 正解率:%f%%" \
      % (correct_core, \
         100.0 * correct_core / Nphrase)

print "主核正解(単純):%d, 正解率:%f%%" \
      % (simplecorrect_core, \
         100.0 * simplecorrect_core / simple)

print "主核正解(名詞連続):%d, 正解率:%f%%" \
      % ( nouncorrect_core, \
          100.0 * nouncorrect_core / noun )
