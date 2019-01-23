#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
from optparse import OptionParser

# モーラ数をカウントする
def x_mora_me( pron, x ):
    nonMoraList = set(u"ァ ィ ゥ ェ ォ ャ ュ ョ".split())
    index_mora = 0
    mora = []
    for p in pron.decode("utf-8"):
        if p not in nonMoraList:
            mora.append(p.encode("utf-8"))
            index_mora += 1
        else:
            mora[index_mora-1] += p.encode("utf-8")
    return mora[x]

usage = u"""usage: %prog datafile
openjtalk 規則でアクセント推定する"""
parser = OptionParser(usage=usage)
(options,args) = parser.parse_args()

if len(args) < 1:
    print >> sys.stderr, "Error: too few arguments\n"
    parser.print_help()
    exit()

re_keiyoshi = re.compile("^形容詞")
re_keijyoshi = re.compile("^形状詞")
re_doshi = re.compile("^動詞")
re_meishi = re.compile("^名詞")
re_setsubi = re.compile("^接尾辞")
re_fuzoku = re.compile("^助")
re_hojyokigou = re.compile("^補助記号")
re_fukushi = re.compile("^副詞")
re_fukushikano = re.compile("普通名詞-副詞可能")
re_setsuzoku = re.compile("^接続詞")
re_rentaishi = re.compile("^連体詞")
re_kigo = re.compile("^記号")

datafile = open(args[0])

prev_pos = ""

for line in datafile:
    
    elems = line.strip("\n").split(" ")

    if len(elems) == 1:
        prev_pos = ""
        print
        continue
        
    # データを読む
    data = {}
    data["orth"], data["pron"], data["pos"], data["cType"], data["cForm"], \
    data["lemma"], data["goshu"], data["iType"], data["aType"], data["aConType"], \
    data["aModType"], data["irex"], data["bunsetsu"], \
    data["nmora"], data["s2noungram1"], data["s2noungram2"], data["s2noungram3"], data["s2noungram4"], \
    data["L_boundary"] = elems
    
    now_pos = data["pos"]
    
    # デフォルトはバウンダリなし
    accent_boundary = "-"
    rule = 1
    
    # 最初は必ずバウンダリがある
    if prev_pos == "": 
        accent_boundary = "/"
        rule = 2

    if re_keiyoshi.search(prev_pos) is not None and re_meishi.search(now_pos) is not None: 
        accent_boundary = "/"
        rule = 3

    if re_keijyoshi.search(prev_pos) is not None and re_meishi.search(now_pos) is not None: 
        accent_boundary = "/"
        rule = 4

    if re_doshi.search(prev_pos) is not None and re_meishi.search(now_pos) is not None: 
        accent_boundary = "/"
        rule = 5

    if re_setsubi.search(prev_pos) is not None and re_meishi.search(now_pos) is not None: 
        accent_boundary = "/"
        rule = 6

    if re_doshi.search(prev_pos) is not None and re_keiyoshi.search(now_pos) is not None: 
        accent_boundary = "/"
        rule = 7
        
    # 補助記号「、」が後にきた場合には，アクセント句境界はないものとする．
    if re_fuzoku.search(prev_pos) is not None and re_fuzoku.search(now_pos) is None and re_hojyokigou.search(now_pos) is None: 
        accent_boundary = "/"
        rule = 8

    if re_fukushi.search(prev_pos) is not None or re_fukushi.search(now_pos) is not None: 
        accent_boundary = "/"
        rule = 9

    if re_setsuzoku.search(prev_pos) is not None or re_setsuzoku.search(now_pos) is not None: 
        accent_boundary = "/"
        rule = 10

    if re_rentaishi.search(prev_pos) is not None or re_rentaishi.search(now_pos) is not None: 
        accent_boundary = "/"
        rule = 11

    if re_kigo.search(prev_pos) is not None or re_kigo.search(now_pos) is not None: 
        accent_boundary = "/"
        rule = 12
        
    # 補助記号「、」が前にきた場合には，アクセント句境界があるものとする．
    if re_hojyokigou.search(prev_pos) is not None: 
        accent_boundary = "/"
        rule = 13
        
    # 読みがないやつはアクセント句境界がない
    if data["pron"] == "*":
        accent_boundary = "-"
        rule += 100

    # for debug
    #print rule,
        
    print data["orth"],
    print data["pron"],
    print data["pos"],
    print data["cType"],
    print data["cForm"],
    print data["lemma"],
    print data["goshu"],
    print data["iType"],
    print data["aType"],
    print data["aConType"],
    print data["aModType"],
    print data["irex"],
    print data["bunsetsu"],
    print data["nmora"],
    print data["s2noungram1"],
    print data["s2noungram2"],
    print data["s2noungram3"],
    print data["s2noungram4"],
    print data["L_boundary"],
    print accent_boundary

    prev_pos = now_pos
