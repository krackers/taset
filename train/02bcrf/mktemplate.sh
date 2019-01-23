#!/bin/zsh

# データが以下の順番で保存されているとする。
# 
# 0.書字形, 1.発音形, 2.品詞, 3.活用型, 4.活用形, 5.語彙素-語彙素読み, 
# 6.語種, 7.語頭変化結合型 8.アクセントタイプ, 9.アクセント結合型, 
# 10.アクセント修飾型, 11. モーラ数
#
# 0.orth, 1.pron, 2.pos1-pos2-pos3-pos4, 3.cType, 4.cForm, 5.lemma-lForm, 
# 6.goshu, 7.iType-iForm-iConType, 8.aType, 9.aConType, 10.aModType, 11.nmora
# 

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
bunsetsu=12
nmora=13
s2noungram1=14
s2noungram2=15
s2noungram3=16
s2noungram4=17

echo "#unigram"

# 前後含めて -2,-1,0,1,2
for ii in -2 -1 0 1 2;do
    jj=$(($ii+2))
    # 書字形、発音形、活用型の組
    echo "U${jj}00:%x[${ii},${orth}]/%x[${ii},${pron}]/%x[${ii},${cType}]"
    # 品詞
    echo "U${jj}01:%x[${ii},${pos}]"
    # 活用型
    echo "U${jj}02:%x[${ii},${cType}]"
    # 活用形
    echo "U${jj}03:%x[${ii},${cForm}]"
    # 語種
    echo "U${jj}04:%x[${ii},${goshu}]"
    # 語頭変化結合型
    echo "U${jj}05:%x[${ii},${iType}]"
    # 単独発声アクセント型
    echo "U${jj}06:%x[${ii},${aType}]"
    # アクセント結合型
    echo "U${jj}07:%x[${ii},${aConType}]"
    # アクセント修飾型
    echo "U${jj}08:%x[${ii},${aModType}]"
    # 文節区切りかどうか
    echo "U${jj}10:%x[${ii},${bunsetsu}]"
    
    # モーラ数と前後のモーラ数
    echo "U${jj}20:%x[0,${nmora}]/%x[${ii},${nmora}]"
    # 単独発声アクセント型と前後のアクセント結合型の組
    echo "U${jj}21:%x[0,${aType}]/%x[${ii},${aConType}]"

done

# 名詞連続 n-gram のくっつき score1 と 一つ前と今の品詞
echo "U931:%x[0,${s2noungram1}]/%x[0,${pos}]/%x[-1,${pos}]"
# 名詞連続 n-gram のくっつき score2 と 一つ前と今の品詞
echo "U932:%x[0,${s2noungram2}]/%x[0,${pos}]/%x[-1,${pos}]"
# 名詞連続 n-gram のくっつき score3 と 一つ前と今の品詞
echo "U933:%x[0,${s2noungram3}]/%x[0,${pos}]/%x[-1,${pos}]"
# 名詞連続 n-gram のくっつき score4 と 一つ前と今の品詞
echo "U934:%x[0,${s2noungram4}]/%x[0,${pos}]/%x[-1,${pos}]"

echo "#bigram"
echo "B"

