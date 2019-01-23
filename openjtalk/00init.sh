
# ディレクトリを作る
mkdir -p in
mkdir -p out

# リンクをはる
cd in
ln -s ../../train/01mkdata/in/jnas_test.txt .
ln -s ../../train/02bcrf/out/e_label_test.txt .
ln -s ../../train/03acrf/out/e_result.abs .
ln -s ../../train/03acrf/out/e_rule_result.abs .
cd -
