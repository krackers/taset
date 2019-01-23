
# アクセントのラベルは、相対変化ラベルにして利用する
./mkdata.py ./in/data_train.txt ./in/label_train.txt > train.abs
./mkdata.py ./in/data_test.txt ./in/label_test.txt > test.abs

# ルールベースでやる
./rule.py test.abs > out/rule_result.abs
./result.py out/rule_result.abs
#正答数:16153, 総形態素数:17801, 正解率:90.742093%,
#総アクセント句数:7642, 正解アクセント句数:6246, 正解率:81.732531%
#単純なアクセント句総数:2609, 正解した単純なアクセント句:2462, 正解率:94.365657%
#名詞連続総数:1044, 正解した名詞連続:891, 正解率:85.344828%
#主核正解(全て):6901, 正解率:90.303585%
#主核正解(単純):2469, 正解率:94.633959%
#主核正解(名詞連続):976, 正解率:93.486590%

tmptrainrel=$(mktemp)
tmptestrel=$(mktemp)
./abs2rel.py train.abs > $tmptrainrel
./abs2rel.py test.abs > $tmptestrel

# ルールベースの結果を、相対ラベルにして、特徴量として加える
tmpresult=$(mktemp)
tmpfile1=$(mktemp); tmpfile2=$(mktemp); tmpfile3=$(mktemp)
./rule.py train.abs > $tmpresult
./abs2rel.py $tmpresult | cut -d " " -f 37 > $tmpfile1
cut -d " " -f1-35 $tmptrainrel > $tmpfile2
cut -d " " -f36 $tmptrainrel > $tmpfile3
paste -d " " $tmpfile2 $tmpfile1 $tmpfile3 > train.rel

./abs2rel.py out/rule_result.abs | cut -d " " -f 37 > $tmpfile1
cut -d " " -f1-35 $tmptestrel > $tmpfile2
cut -d " " -f36 $tmptestrel > $tmpfile3
paste -d " " $tmpfile2 $tmpfile1 $tmpfile3 > test.rel

# アクセント句境界を与える場合
./mktemplate.sh > template
# -c 0.8 は cv.sh で求めたもの。-t は、テキスト形式でもモデルを出力するオプション
crf_learn -c 0.8 -p 8 -t template train.rel model
crf_test -m model test.rel > out/result.rel
./rel2abs.py out/result.rel > out/result.abs
./result.py out/result.abs
#正答数:17308, 総形態素数:17801, 正解率:97.230493%,
#総アクセント句数:7641, 正解アクセント句数:7213, 正解率:94.398639%
#単純なアクセント句総数:2608, 正解した単純なアクセント句:2525, 正解率:96.817485%
#名詞連続総数:1044, 正解した名詞連続:948, 正解率:90.804598%
#主核正解(全て):7420, 正解率:97.107708%
#主核正解(単純):2532, 正解率:97.085890%
#主核正解(名詞連続):1017, 正解率:97.413793%

