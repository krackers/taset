#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser
usage = ""
parser = OptionParser(usage=usage)
(options,args) = parser.parse_args()

file = open( args[0] )

flag = 0

for line in file:
    line = line.strip()
    features = line.split()

    if len(features) < 1 and flag == 0:
        flag = 1
        continue

    if len(features) < 1 and flag == 2:
        flag = 3
        continue

    if flag == 1:
        flag = 2
        continue
    
    if flag == 2:
        print line
        
