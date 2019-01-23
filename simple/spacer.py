#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser

        
usage = u"""usage: %prog featurefile 
/ を改行に変える"""
parser = OptionParser(usage=usage)
(options,args) = parser.parse_args()

if len(args) < 1:
    print >> sys.stderr, "Error: too few arguments\n"
    parser.print_help()
    exit()

featurefile = open( args[0] )

for line in featurefile:

    # タブで区切る
    features = line.strip("\n").split("\t")
    
    if features[0] == "": 
        print ""
        continue
    
    if features[1] == "/": print ""
    print features[0],
