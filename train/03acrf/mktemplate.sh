#!/bin/bash
# 

# ラベルファイルのフォーマット
# 0.書字形, 1.発音形, 2.文中アクセント, 3.アクセント句境界
# 0.orth, 1.pron, 2.accent 3.boundary

# 素性
# 0.書字形, 1.発音形, 2.品詞, 3.活用型, 4.活用形, 5.語彙素-語彙素読み, 
# 6.語種, 7.語頭変化結合型 8.アクセントタイプ, 9.アクセント結合型, 10.アクセント修飾型, 
# 11.IREX, 12. 文節
# 13.当該形態素のモーラ数、14.アクセント句内の一つ目か否か、15.アクセント句内の最後か否か、
# 16.アクセント句の形態素数、17.数詞か否か、18.助数詞か否か
# 19.単独型種類ラベル、20.助数詞ラベル、21.2モーラ以下かどうか、22.重音節を含むか、
# 23.先頭モーラ、24.第二モーラ、25.単独発声アクセント核位置の一つ前、26.核位置、
# 27.核位置の一つ後のモーラ、28.末尾の１つ前のモーラ、29.末尾モーラ
# 30.aType(8)の第一候補、
# 31.aConTypeの助詞・助動詞タイプ（動詞）、32.同形容詞、33.同名詞
# 34.aType1をアクセント修飾型(10)で修正したもの
# 35.規則で推定したアクセント（rel）

orth=0
pron=1
pos=2
cType=3
cForm=4
lemma=5
goshu=6
iType=7
aType=8
aConType=9
aModType=10
irex=11
bunsetxu=12
nmora=13
morph1=14
morphl=15
nmorph=16
issushi=17
isjosushi=18
relAType=19
josushiType=20
two=21
juuon=22
mora1=23
mora2=24
mora3=25
mora4=26
mora5=27
mora6=28
mora7=29
aType1=30
aConTypeFV=31
aConTypeFA=32
aConTypeFN=33
MaType1=34
rule=35

echo "#unigram"

# bias 項
echo "U999:"

#for i in `seq -2 2`;do
for((i=-2; i <= 2; i++));do	
    j=$((i+2))
    # 書字形
    echo "U${j}00:%x[${i},${orth}]"
    # 発音形
    echo "U${j}01:%x[${i},${pron}]"
    # 品詞
    echo "U${j}02:%x[${i},${pos}]"
    # 活用型
    echo "U${j}03:%x[${i},${cType}]"
    # 活用形
    echo "U${j}04:%x[${i},${cForm}]"
    # 語彙素-語形
    echo "U${j}05:%x[${i},${lemma}]"
    # 語種
    echo "U${j}06:%x[${i},${goshu}]"
    # 語頭変化結合型
    echo "U${j}07:%x[${i},${iType}]"
    # 単独発声アクセント型
    echo "U${j}08:%x[${i},${aType}]"
    # アクセント結合型
    #echo "U${j}09:%x[${i},${aConType}]"
    # アクセント修飾型
    echo "U${j}10:%x[${i},${aModType}]"
    # モーラ数
    echo "U${j}11:%x[${i},${nmora}]"
    # アクセント句一つ目の形態素？
    echo "U${j}12:%x[${i},${morph1}]"
    # アクセント句の形態素数
    echo "U${j}14:%x[${i},${nmorph}]"
    # IREX
    echo "U${j}15:%x[${i},${irex}]"
    # 単独型種類ラベル
    echo "U${j}17:%x[${i},${relAType}]"
    # 二モーラ以下かどうか
    echo "U${j}19:%x[${i},${two}]"
    # 二モーラ以下かどうか、と語種の組み合わせ
    echo "U${j}20:%x[${i},${two}]/%x[${i},${goshu}]"
    # 重音節を含むかどうか
    echo "U${j}21:%x[${i},${juuon}]"
    # 各箇所のモーラ（先頭二つ、核周辺三つ、末尾二つ）
    echo "U${j}22:%x[${i},${mora1}]"
    echo "U${j}23:%x[${i},${mora2}]"
    echo "U${j}24:%x[${i},${mora3}]"
    echo "U${j}25:%x[${i},${mora4}]"
    echo "U${j}26:%x[${i},${mora5}]"
    echo "U${j}27:%x[${i},${mora6}]"
    echo "U${j}28:%x[${i},${mora7}]"
    # aConType の助詞・助動詞（動詞）
    echo "U${j}30:%x[${i},${aConTypeFV}]"
    # aConType の助詞・助動詞（形容詞）
    echo "U${j}31:%x[${i},${aConTypeFA}]"
    # aConType の助詞・助動詞（名詞）
    echo "U${j}32:%x[${i},${aConTypeFN}]"
    # アクセント修正型による修正済 aType1
    echo "U${j}33:%x[${i},${MaType1}]"
    # ルールによるアクセント(rel)
    echo "U${j}34:%x[${i},${rule}]"

    if [ ${i} -ne 0 ]; then
        # 中心の単独発声アクセント型と、前後のアクセント結合型の組
	echo "U${j}41:%x[0,${MaType1}]/%x[${i},${aConType}]"
	echo "U${j}42:%x[${i},${MaType1}]/%x[0,${aConType}]"
        # 品詞と、中心の単独発声アクセント型と、前後のアクセント結合型（品詞依存）の組
	echo "U${j}43:%x[0,${pos}]/%x[0,${MaType1}]/%x[${i},${aConTypeFV}]"
	echo "U${j}44:%x[0,${pos}]/%x[0,${MaType1}]/%x[${i},${aConTypeFA}]"
	echo "U${j}45:%x[0,${pos}]/%x[0,${MaType1}]/%x[${i},${aConTypeFN}]"
	echo "U${j}46:%x[${i},${pos}]/%x[${i},${MaType1}]/%x[0,${aConTypeFV}]"
	echo "U${j}47:%x[${i},${pos}]/%x[${i},${MaType1}]/%x[0,${aConTypeFA}]"
	echo "U${j}48:%x[${i},${pos}]/%x[${i},${MaType1}]/%x[0,${aConTypeFN}]"
    fi
    
    # iType（か issushi）と josushiType（か isjosushi）の組
    if [ 0 -lt ${i} ]; then
        echo "U${j}61:%x[0,${iType}]/%x[${i},${josushiType}]"
        echo "U${j}62:%x[0,${issushi}]/%x[${i},${josushiType}]"
        echo "U${j}63:%x[0,${iType}]/%x[${i},${isjosushi}]"
        echo "U${j}64:%x[0,${issushi}]/%x[${i},${isjosushi}]"
    fi
    if [ ${i} -lt 0 ]; then
        echo "U${j}71:%x[${i},${iType}]/%x[0,${josushiType}]"
        echo "U${j}72:%x[${i},${issushi}]/%x[0,${josushiType}]"
        echo "U${j}73:%x[${i},${iType}]/%x[0,${isjosushi}]"
        echo "U${j}74:%x[${i},${issushi}]/%x[0,${isjosushi}]"
    fi

done

# ルールによるアクセント(rel)と、今,一つ前の品詞の組
echo "U${j}90:%x[0,${rule}]/%x[0,${pos}]/%x[1,${pos}]"


echo "#bigram"
echo "B"
