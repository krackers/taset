
# CRF++ をインストールし、
# crf_learn と crf_test にパスを通しておくこと。
#
# なお version は、CRF++ of 0.57 を利用した。

# ディレクトリを作る
mkdir -p in
mkdir -p out

# 01mkdata ディレクトリで作ったデータにリンクをはる
cd in
ln -s ../../01mkdata/out/data_train.txt .
ln -s ../../01mkdata/out/data_test.txt .
ln -s ../../01mkdata/out/label_train.txt .
ln -s ../../01mkdata/out/label_test.txt .
cd -

# wikipedia データから名詞 n-gram を作成
./ngram.sh

# n-gram データを読んで整形しておく
./rdnoungram.py 

