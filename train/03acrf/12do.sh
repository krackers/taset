
# 02do.sh と違い、02bcrf で推定したアクセント句境界推定結果を使ってアクセントを推定する。

# アクセントのラベルは、相対変化ラベルにして利用する
./mkdata.py ./in/data_train.txt ./in/e_label_train.txt > e_train.abs
./mkdata.py ./in/data_test.txt ./in/e_label_test.txt > e_test.abs

# ルールベースでやる
./rule.py e_test.abs > out/e_rule_result.abs
./result.py out/e_rule_result.abs

tmptrainrel=$(mktemp)
tmptestrel=$(mktemp)
./abs2rel.py e_train.abs > $tmptrainrel
./abs2rel.py e_test.abs > $tmptestrel

# ルールベースの結果を、相対ラベルにして、特徴量として加える
tmpresult=$(mktemp)
tmpfile1=$(mktemp); tmpfile2=$(mktemp); tmpfile3=$(mktemp)
./rule.py e_train.abs > $tmpresult
./abs2rel.py $tmpresult | cut -d " " -f 37 > $tmpfile1
cut -d " " -f1-35 $tmptrainrel > $tmpfile2
cut -d " " -f36 $tmptrainrel > $tmpfile3
paste -d " " $tmpfile2 $tmpfile1 $tmpfile3 > e_train.rel

./abs2rel.py out/e_rule_result.abs | cut -d " " -f 37 > $tmpfile1
cut -d " " -f1-35 $tmptestrel > $tmpfile2
cut -d " " -f36 $tmptestrel > $tmpfile3
paste -d " " $tmpfile2 $tmpfile1 $tmpfile3 > e_test.rel

./mktemplate.sh > template
# -c 0.8 は cv.sh で求めたもの。-t は、テキスト形式でもモデルを出力するオプション
crf_learn -c 0.8 -p 8 -t template e_train.rel e_model
crf_test -m e_model e_test.rel > out/e_result.rel
./rel2abs.py out/e_result.rel > out/e_result.abs
./result.py out/e_result.abs
#正答数:16999, 総形態素数:17801, 正解率:95.494635%,
#総アクセント句数:7091, 正解アクセント句数:6417, 正解率:90.494994%
#単純なアクセント句総数:2197, 正解した単純なアクセント句:2120, 正解率:96.495221%
#名詞連続総数:1134, 正解した名詞連続:907, 正解率:79.982363%
#主核正解(全て):6711, 正解率:94.641094%
#主核正解(単純):2124, 正解率:96.677287%
#主核正解(名詞連続):1029, 正解率:90.740741%
