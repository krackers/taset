#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pickle
from optparse import OptionParser

usage = u"""usage: %prog outfile
noun-gram を読み込んで outfile に保存"""
parser = OptionParser(usage=usage)
(options,args) = parser.parse_args()

# 1-gram.txt, 2-gram.txt は，wikipedia データから学習した名詞連続のみの n-gram．
gram1file = open( "1-gram.txt" )
gram2file = open( "2-gram.txt" )

# read 1gram
gram1 = {}
for line in gram1file:
    elems = line.split()
    gram1[ elems[1] ] = int(elems[0])

# read 2gram
# *1: 両方の 1-gram で正規化
# *2: 前方の 1-gram で正規化
# *3: 後方の 1-gram で正規化
# *4: 正規化なし
gram21 = {}
gram22 = {}
gram23 = {}
gram24 = {}
score1s = []
score2s = []
score3s = []
score4s = []

for line in gram2file:
    elems = line.split()
    string = "%s %s" % (elems[1], elems[2])

    if gram1.has_key( elems[1] ) and gram1.has_key( elems[2] ):

        # 3 回以上観測されていないものはデータに入れない
        if int(elems[0]) < 3: continue

        score1 = float( elems[0] ) / gram1[ elems[1] ] / gram1[ elems[2] ]
        score2 = float( elems[0] ) / gram1[ elems[1] ]
        score3 = float( elems[0] ) / gram1[ elems[2] ]
        score4 = float( elems[0] ) 

        gram21[ string ] = score1
        gram22[ string ] = score2
        gram23[ string ] = score3
        gram24[ string ] = score4

        score1s.append( score1 )
        score2s.append( score2 )
        score3s.append( score3 )
        score4s.append( score4 )

# scores をソート
score1s.sort()
score2s.sort()
score3s.sort()
score4s.sort()

# とりあえず、5段階評価にする。
unit1 = int( len(score1s) / 5.0 )
th1_1 = score1s[ unit1 ]
th1_2 = score1s[ unit1*2 ]
th1_3 = score1s[ unit1*3 ]
th1_4 = score1s[ unit1*4 ]

unit2 = int( len(score2s) / 5.0 )
th2_1 = score2s[ unit2 ]
th2_2 = score2s[ unit2*2 ]
th2_3 = score2s[ unit2*3 ]
th2_4 = score2s[ unit2*4 ]

unit3 = int( len(score3s) / 5.0 )
th3_1 = score3s[ unit3 ]
th3_2 = score3s[ unit3*2 ]
th3_3 = score3s[ unit3*3 ]
th3_4 = score3s[ unit3*4 ]

unit4 = int( len(score4s) / 5.0 )
th4_1 = score4s[ unit4 ]
th4_2 = score4s[ unit4*2 ]
th4_3 = score4s[ unit4*3 ]
th4_4 = score4s[ unit4*4 ]

print th1_1, th1_2, th1_3, th1_4
print th2_1, th2_2, th2_3, th2_4
print th3_1, th3_2, th3_3, th3_4
print th4_1, th4_2, th4_3, th4_4

for key in gram21.keys():
    score1 = gram21[ key ]
    score2 = gram22[ key ]
    score3 = gram23[ key ]
    score4 = gram24[ key ]
    
    if score1 < th1_1:
        gram21[ key ] = 1        
    elif score1 < th1_2:
        gram21[ key ] = 2
    elif score1 < th1_3:
        gram21[ key ] = 3
    elif score1 < th1_4:
        gram21[ key ] = 4
    else:
        gram21[ key ] = 5

    if score2 < th2_1:
        gram22[ key ] = 1        
    elif score2 < th2_2:
        gram22[ key ] = 2
    elif score2 < th2_3:
        gram22[ key ] = 3
    elif score2 < th2_4:
        gram22[ key ] = 4
    else:
        gram22[ key ] = 5

    if score3 < th3_1:
        gram23[ key ] = 1        
    elif score3 < th3_2:
        gram23[ key ] = 2
    elif score3 < th3_3:
        gram23[ key ] = 3
    elif score3 < th3_4:
        gram23[ key ] = 4
    else:
        gram23[ key ] = 5

    if score4 < th4_1:
        gram24[ key ] = 1        
    elif score4 < th4_2:
        gram24[ key ] = 2
    elif score4 < th4_3:
        gram24[ key ] = 3
    elif score4 < th4_4:
        gram24[ key ] = 4
    else:
        gram24[ key ] = 5

outfile1 = open("2gram1.dat", "w")
outfile2 = open("2gram2.dat", "w")
outfile3 = open("2gram3.dat", "w")
outfile4 = open("2gram4.dat", "w")

pickle.dump( gram21, outfile1 )
pickle.dump( gram22, outfile2 )
pickle.dump( gram23, outfile3 )
pickle.dump( gram24, outfile4 )
