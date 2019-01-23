
# ディレクトリを作る
mkdir -p in
mkdir -p out

# データにリンクをはる
cd in
ln -s ../../01mkdata/out/data_train.txt .
ln -s ../../01mkdata/out/data_test.txt .
ln -s ../../01mkdata/out/label_train.txt .
ln -s ../../01mkdata/out/label_test.txt .

ln -s ../../02bcrf/out/e_label_train.txt .
ln -s ../../02bcrf/out/e_label_test.txt .

cd -
