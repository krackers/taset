#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

buf = ""
error_flag = 0

for line in sys.stdin:
    elems = line.split()
    if len(elems) == 0:
        if error_flag == 1:
            print buf
        error_flag = 0
        buf = ""
        continue
    
    ans, hyp = elems[-2], elems[-1]
    if ans != hyp: error_flag = 1
    buf += line



