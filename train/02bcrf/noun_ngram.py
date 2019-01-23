#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-n", dest="n", type="int", default=3)
(options, args) = parser.parse_args()
n = options.n

renoun = re.compile("^名詞")
words = []

for line in sys.stdin:
	elems = line.split()

	if len(elems) == 1 or renoun.search(elems[1]) is None:
		# EOS や名詞じゃなかった場合
		for i in range(len(words)-n):
			print " ".join(words[i:i+n])
		words = []
	else:
		# 名詞だった
		words.append(elems[0])

"""
usage:
 --- | mecab | noun_ngram.py -n 3 | sort | uniq -c > trigram.txt
"""
