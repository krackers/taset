#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
from optparse import OptionParser

usage = u"""usage: %prog datafile labelfile
アクセント句推定用に特徴量追加・アクセント句境界で切る・発音しないもの（。など）を削除
"""
parser = OptionParser(usage=usage)
(options,args) = parser.parse_args()

if len(args) < 1:
    print >> sys.stderr, "Error: too few arguments\n"
    parser.print_help()
    exit()
datafile = open( args[0] )

# データファイルのフォーマット
#
# 0.書字形, 1.発音形, 2.品詞, 3.活用型, 4.活用形, 5.語彙素-語彙素読み,
# 6.語種, 7.語頭変化結合型 8.アクセントタイプ, 9.アクセント結合型, 10.アクセント修飾型,
# 11.IREX, 12.文節
#
# 0.orth, 1.pron, 2.pos, 3.cType, 4.cForm, 5.lemma,
# 6.goshu, 7.iType, 8.aType, 9.aConType, 10.aModType,
# 11,irex, 12,bunsetsu

# ラベルファイルのフォーマット
# 0.書字形, 1.発音形, 2.文中アクセント, 3.アクセント句境界
# 0.orth, 1.pron, 2.accent 3.boundary

# 追加する素性
#
# 当該形態素のモーラ数、アクセント句内の一つ目か否か、アクセント句内の最後か否か、
# アクセント句の形態素数、数詞か否か、助数詞か否か
# 単独型種類ラベル、助数詞ラベル、2モーラ以下かどうか、重音節を含むか、
# 先頭モーラ、第二モーラ、単独発声アクセント核位置の一つ前、核位置、
# 核位置の一つ後のモーラ、末尾の１つ前のモーラ、末尾モーラ
# aType(8)の第一候補、
# aConTypeの助詞・助動詞タイプ（動詞）、同形容詞、同名詞
# アクセント修飾型を反映させたaType1
#
# nmora, morph1, morphl,
# nmorph, issushi, isjosushi,
# relAType, josushiType, two, juuon,
# mora1, mora2, mora3, mora4,
# mora5, mora6, mora7,
# aType1, aConTypeFV, aConTypeFA, aConTypeFN
# MaType1

# それ自身ではモーラ数にカウントされない読み一覧
nonMoraList = set(u"ァ ィ ゥ ェ ォ ャ ュ ョ".split())

josushi = re.compile("-助数詞")
sushi = re.compile("-数詞")
yayuyo = re.compile("ャ|ュ|ョ|ー|ン|ッ")
recomma = re.compile(",.*")
redoushi = re.compile("動詞%F")
rekeiyoshi = re.compile("形容詞%F")
remeishi = re.compile("名詞%F")
ref6 = re.compile("F6")

# アクセント句内のデータをためるバッファ
buf_data = []

for dataline in datafile:

    # 前の形態素と現在の形態素の間にアクセント句境界がある場合，もしくは文末の場合
    # anmora, ranmora, nmorph, index, rindex を計算、print、バッファの初期化
    if len(dataline.strip()) == 0:
        nmorph = len(buf_data)
        for ii in range( 0, nmorph ):
            data = buf_data[ii]

            # morph1, morphl
            if ii == 0:
                data["morph1"] = "1"
            else:
                data["morph1"] = "0"

            if ii == nmora-1:
                data["morphl"] = "1"
            else:
                data["morphl"] = "0"
                
            # nmorph
            data["nmorph"] = nmorph

            # CRF++ のデータ形式で出力する
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

            # nmora, morph1, morphl,
            # nmorph, issushi, isjosushi,
            # relAType, josushiType, two, juuon,
            # mora1, mora2, mora3, mora4,
            # mora5, mora6, mora7,
            # aType1, aConTypeFV, aConTypeFA, aConTypeFN
            # MaType1
            print data["nmora"],
            print data["morph1"],
            print data["morphl"],
            print data["nmorph"],
            print data["issushi"],
            print data["isjosushi"],
            print data["relAType"],
            print data["josushiType"],
            print data["two"],
            print data["juuon"],
            print data["mora1"],
            print data["mora2"],
            print data["mora3"],
            print data["mora4"],
            print data["mora5"],
            print data["mora6"],
            print data["mora7"],
            print data["aType1"],
            print data["aConTypeFV"],
            print data["aConTypeFA"],
            print data["aConTypeFN"],
            print data["MaType1"]

        buf_data = []

    # 空行のデータは読まない
    if len(dataline.strip()) == 0:
        print
        continue

    # データがある場合
    data = {}

    # データを読む
    data["orth"], data["pron"], data["pos"], data["cType"], data["cForm"], \
    data["lemma"], data["goshu"], data["iType"], data["aType"], data["aConType"], \
    data["aModType"], data["irex"], data["bunsetsu"] = dataline.split()
    
    # 読みが無い形態素は無視する
    if data["pron"] == "*": continue

    # 当該形態素のモーラ数、アクセント句内の一つ目か否か、アクセント句内の最後か否か、
    # アクセント句の形態素数、数詞か否か、助数詞か否か
    # 単独型種類ラベル、助数詞ラベル、2モーラ以下かどうか、重音節を含むか、
    # 先頭モーラ、第二モーラ、単独発声アクセント核位置の一つ前、核位置、
    # 核位置の一つ後のモーラ、末尾の１つ前のモーラ、末尾モーラ
    # aType(8)の第一候補、
    # aConTypeの助詞・助動詞タイプ（動詞）、同形容詞、同名詞
    #
    # nmora, morph1, morphl,
    # nmorph, issushi, isjosushi,
    # relAType, josushiType, two, juuon,
    # mora1, mora2, mora3, mora4,
    # mora5, mora6, mora7,
    # aType1, aConTypeFV, aConTypeFA, aConTypeFN
    # MaType1
    # 
    # を計算して保存する

    # 発音形をモーラごとに分ける
    index_mora = 0
    mora = []
    pron = data["pron"]
    for p in pron.decode("utf-8"):
        if p not in nonMoraList:
            mora.append(p.encode("utf-8"))
            index_mora += 1
        else:
            mora[index_mora-1] += p.encode("utf-8")

    # nmora
    nmora = len(mora)
    data["nmora"] = str(nmora)

    pos = data["pos"]
    # 数詞か否か、助数詞か否か
    if sushi.search(pos) is not None:
        data["issushi"] = "1"
    else:
        data["issushi"] = "0"
    if josushi.search(pos) is not None:
        data["isjosushi"] = "1"
    else:
        data["isjosushi"] = "0"

    aType = data["aType"]
    # 単独型種類ラベル：無核="non", 末尾に核="mora", 末尾の一つ前に核=末尾2モーラ自身, それ以外="else"
    # relAType
    if aType == str(0):
        relAType = "non"
    elif aType == data["nmora"]:
        relAType = "mora"
    elif aType == str(nmora-1):
        relAType = mora[-2] + mora[-1]
    else:
        relAType = "else"
    data["relAType"] = relAType

    orth = data["orth"]
    # 助数詞ラベル（小林修論参照）
    if josushi.search(pos) is not None:
        if orth=="個" or orth=="位" or orth=="時" or orth=="分" or orth=="時間" \
               or orth=="歳" or orth=="羽" or orth=="通り" or orth=="斤" or orth=="層" \
               or orth=="アール" or orth=="センチ"or orth=="キロ"or orth=="ドル" \
               or orth=="度" or orth=="階" or orth=="球" or orth=="巡" or orth=="乗" \
               or orth=="週" or orth=="人前" or orth=="敗" or orth=="着" or orth =="度目" \
               or orth=="代目" or orth=="貫目" or orth=="日目" or orth=="球目" \
               or orth=="丁目" or orth=="畳" or orth=="ヶ月":
            josushiType = "a"
        elif orth=="問" or orth=="台" or orth=="軒" or orth=="件" or orth=="票" \
                 or orth=="町" or orth=="艘" or orth=="代" or orth=="枚" or orth=="名" \
                 or orth=="面" or orth=="本" or orth=="杯" or orth=="丁":
            josushiType = "b"
        elif orth=="升":
            josushiType = "c"
        elif orth=="年" or orth=="段" or orth=="番":
            josushiType = "d"
        elif orth=="貫" or orth=="版" or orth=="銭" or orth=="回" or orth=="点" or orth=="巻":
            josushiType = "e"
        elif orth=="尺" or orth=="着" or orth=="角":
            josushiType = "f"
        elif orth=="円":
            josushiType = "g"
        elif orth=="曲" or orth=="石" or orth=="匹" or orth=="冊" or orth=="足" or orth=="拍" \
                 or orth=="脚" or orth=="局" or orth=="発" or orth=="室" or orth=="節":
            josushiType = "h"
        elif orth=="合":
            josushiType = "i"
        elif orth=="人":
            josushiType = "j"
        elif orth=="月" or orth=="日":
            josushiType = "k"
        elif orth=="寸":
            josushiType = "l"
        else:
            josushiType = "m"
    else:
        josushiType = "*"
    data["josushiType"] = josushiType

    #  2モーラ以下かどうか
    if nmora <=2 :
        two = "1"
    else:
        two = "0"
    data["two"] = two

    # 22. 重音節を含むかどうか
    if yayuyo.search(data["pron"]) is not None:
        juuon = "1"
    else:
        juuon = "0"
    data["juuon"] = juuon

    # 先頭モーラ、第二モーラ、単独発声アクセント核位置の一つ前、核位置、
    # 核位置の一つ後のモーラ、末尾の１つ前のモーラ、末尾モーラ
    # aType(8)の第一候補
    mora1 = mora[0]
    mora7 = mora[-1]
    if len(mora) >= 2:
        mora2 = mora[1]
        mora6 = mora[-2]
    else:
        mora2 = "*"
        mora6 = "*"

    aType1 = recomma.sub('', aType)
    if aType1 == "*":
        mora3 = "*"
        mora4 = "*"
        mora5 = "*"
    else:
        if 0 <= int(aType1)-2 < len(mora):
            mora3 = mora[int(aType1)-2]
        else:
            mora3 = "*"
        if 0 <= int(aType1)-1 < len(mora):
            mora4 = mora[int(aType1)-1]
        else:
            mora4 = "*"
        if  0<= int(aType1) < len(mora):
            mora5 = mora[int(aType1)]
        else:
            mora5 = "*"

    data["mora1"] = mora1
    data["mora2"] = mora2
    data["mora3"] = mora3
    data["mora4"] = mora4
    data["mora5"] = mora5
    data["mora6"] = mora6
    data["mora7"] = mora7
    data["aType1"] = aType1

    # aConTypeの助詞・助動詞タイプ（動詞）、同形容詞、同名詞
    aConTypeFV = "*"
    aConTypeFA = "*"
    aConTypeFN = "*"
    aConType = data["aConType"]
    buf = aConType.split(",")
    # F6 は、コンマ句切りで２つ数字が入っているので、
    # その部分は区切らないように簡易ハックする
    for ii in range( 0, len(buf) ):
        if ii >= len(buf): break
        if ref6.search( buf[ii] ) is not None:
            buf[ii] = buf[ii] + "," + buf[ii+1]
            buf.remove( buf[ii+1] )
    for ii in range(0,len(buf)):
        if redoushi.search(buf[ii]) is not None: aConTypeFV = buf[ii]
        if rekeiyoshi.search(buf[ii]) is not None: aConTypeFA = buf[ii]
        if remeishi.search(buf[ii]) is not None: aConTypeFN = buf[ii]

    data["aConTypeFV"] = aConTypeFV
    data["aConTypeFA"] = aConTypeFA
    data["aConTypeFN"] = aConTypeFN
    
    # アクセント修飾型を反映させた aType1 (MaType1)
    if data["aModType"] == "*":
        aModType_type = "*"
    else:
        aModType_type, aModType_value = data["aModType"].split("@")
        aModType_value = int( aModType_value )

    if aModType_type == "M1":
        MaType1 = str( nmora - aModType_value )
    elif aModType_type == "M2":
        if aType1 == "0":
            MaType1 = str( nmora - aModType_value )
        else:
            MaType1 = aType1
    elif aModType_type == "M4":
        if aType1 == "0" or aType1 == "1" or aType1 == "*":
            MaType1 = aType1
        else:
            MaType1 = str( int(aType1) - aModType_value )
    else:
        # aModType_type == "*"
        MaType1 = aType1
    data["MaType1"] = MaType1

    buf_data.append(data)

print
