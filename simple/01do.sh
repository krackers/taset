#!/bin/sh

# cabocha -O2 で情報を出力させる
tmpfile1=log/1.txt
rm -rf $tmpfile1
for line in $(cat input.txt);do echo $line | cabocha -n1 -O2 >> $tmpfile1;done;

# cabocha の出力を整形し、データ化する。
tmpfile2=log/2.txt
./seikei.py $tmpfile1 > $tmpfile2

# バウンダリ用のデータ追加
tmpfile3=log/3.txt
./mkdata_bound.py $tmpfile2 > $tmpfile3

# CRF を使ってアクセントバウンダリを推定
tmpfile4=log/4.txt
crf_test -m model_bound $tmpfile3 | cut -f 1,15 > $tmpfile4

# バウンダリにスペースを挟む
tmpfile5=log/5.txt
./spacer.py $tmpfile4 | sed "s; ;;g" > $tmpfile5

# アクセント句を与えてもう一度 cabocha 
tmpfile6=log/6.txt
rm -rf $tmpfile6
for line in $(cat $tmpfile5);do echo $line | cabocha -n1 -O2 >> $tmpfile6;done;

# cabocha の出力を整形し、データ化する。
tmpfile7=log/7.txt
./seikei.py $tmpfile6 > $tmpfile7

# アクセント用にもろもろデータを追加する
tmpfile8=log/8.txt
./mkdata_accent.py $tmpfile7 > $tmpfile8

# ルールベースの結果を、相対ラベルにして、特徴量として加える
tmpfile9=log/9.txt; tmpfile10=log/10.txt
./rule.py $tmpfile8 > $tmpfile9
./abs2rel.py $tmpfile9 > $tmpfile10

# CRF を使って文中アクセント型を推定
tmpfile11=log/11.txt; tmpfile12=log/12.txt
crf_test -m model_accent $tmpfile10 > $tmpfile11
./rel2abs.py $tmpfile11 | cut -d " " -f 1,2,37 

