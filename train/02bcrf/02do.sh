
# データをつくる
./mkdata.py in/data_test.txt in/label_test.txt > test.txt
./mkdata.py in/data_train.txt in/label_train.txt > train.txt

# ルールベースの結果．
./rule.py test.txt > out/rule_result.txt
./result.py out/rule_result.txt 
#すべて:7641/17801->7675：正答数:6804, 脱落誤り:837, 挿入誤り:871, Recall:89.045936, Precision:88.651466, F値:88.848263
#名詞連続:606/1760->0：正答数:0, 脱落誤り:606, 挿入誤り:0, Recall:0.000000, Precision:0.000000, F値:0.000000

# crf++ のためのテンプレートを作成する
./mktemplate.sh > template

# -c 0.1 は、01cv.sh で決めた。
crf_learn -c 0.1 -p 8 -t template train.txt model
crf_test -m model test.txt > out/result.txt
./result.py out/result.txt
#すべて:7641/17801->7097：正答数:6915, 脱落誤り:726, 挿入誤り:182, Recall:90.498626, Precision:97.435536, F値:93.839056
#名詞連続:606/1760->455：正答数:395, 脱落誤り:211, 挿入誤り:60, Recall:65.181518, Precision:86.813187, F値:74.458058


# -------------------------------------------------------------
# 02bcrf の結果を使ってアクセント核を推定するためのラベルの作成

tmpfile1=$(mktemp); tmpfile2=$(mktemp); tmpfile3=$(mktemp); tmpfile4=$(mktemp)
crf_test -m model train.txt | cut -f20 | sed "s;\t; ;g" > $tmpfile1
crf_test -m model test.txt | cut -f20 | sed "s;\t; ;g" > $tmpfile2
cut -d " " -f1,2,3 in/label_train.txt > $tmpfile3
cut -d " " -f1,2,3 in/label_test.txt > $tmpfile4

paste -d " " $tmpfile3 $tmpfile1 > out/e_label_train.txt
paste -d " " $tmpfile4 $tmpfile2 > out/e_label_test.txt
