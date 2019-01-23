#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
from optparse import OptionParser

usage = u"""usage: %prog
data.txt を改行ごとに別ファイルに出力する
"""
parser = OptionParser(usage=usage)
(options,args) = parser.parse_args()

if len(args) < 0:
    print >> sys.stderr, "Error: too few arguments\n"
    parser.print_help()
    exit()

file = open( "./data.txt" )

# 何番目のセンテンスをよんでいるかのカウンタ
count = 1

buf = ""
for line in file:

    if len(line) == 1:
        outfile = open( "./data/s%d.txt" % count, "w" )
        outfile.write( buf )
        outfile.close()
        count += 1
        buf = ""
    else:
        buf += line
        
