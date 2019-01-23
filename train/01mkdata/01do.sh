
# cabocha -O2 で情報を出力させる
tmpfile1=cabocha.txt
for line in $(cat in/jnas.txt);do 
    echo $line | cabocha -n1 -O2 >> $tmpfile1
done

# cabocha の出力を整形。読みが誤っているものは、データから省く。
tmpfile2=seikei.txt
./seikei.py $tmpfile1 > $tmpfile2
./mkdata.py $tmpfile2 in/label.txt > out/data.txt
./mklabel.py $tmpfile2 in/label.txt > out/label.txt

# 学習データと評価データに分割する。999 文章を評価データにする。
tail -n 20602 out/data.txt > out/data_test.txt
head -n 76775 out/data.txt > out/data_train.txt
tail -n 20602 out/label.txt > out/label_test.txt
head -n 76775 out/label.txt > out/label_train.txt
