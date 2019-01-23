
# 3-fold cross varidation を行う。
# 02do.sh でやることを -c を変えて何回もやっているだけ。

candidate=(10 5 1.0 0.5 0.1 0.05 0.01)

resultfile=out/cvresult.txt
./mktemplate.sh > template

tmpfile1=$(mktemp); tmpfile2=$(mktemp); tmpfile3=$(mktemp)
tmpfile4=$(mktemp); tmpfile5=$(mktemp); tmpfile6=$(mktemp)

# データを 3 分割する。
head -n 25603 ./in/data_train.txt > $tmpfile1
tail -n 25558 ./in/data_train.txt > $tmpfile2
head -n 51217 ./in/data_train.txt | tail -n 25614 > $tmpfile3

head -n 25603 ./in/label_train.txt > $tmpfile4
tail -n 25558 ./in/label_train.txt > $tmpfile5
head -n 51217 ./in/label_train.txt | tail -n 25614 > $tmpfile6

# FIRST TRY
tmpfile7=$(mktemp); tmpfile8=$(mktemp);
tmptrain=$(mktemp); tmptest=$(mktemp)
cat $tmpfile2 $tmpfile3 > $tmpfile7
cat $tmpfile5 $tmpfile6 > $tmpfile8

./mkdata.py $tmpfile7 $tmpfile8 > $tmptrain
./mkdata.py $tmpfile1 $tmpfile4 > $tmptest

for c in $candidate;do     
    tmpfile9=$(mktemp)
    tmpmodel=$(mktemp)
    tmpresult=$(mktemp)
    crf_learn -c ${c} -p 8 template $tmptrain $tmpmodel
    crf_test -m $tmpmodel $tmptest > $tmpresult
    echo "FIRST TRY: c=${c}" >> $resultfile
    ./result.py $tmpresult >> $resultfile
done

# SECOND TRY
cat $tmpfile1 $tmpfile3 > $tmpfile7
cat $tmpfile4 $tmpfile6 > $tmpfile8

./mkdata.py $tmpfile7 $tmpfile8 > $tmptrain
./mkdata.py $tmpfile2 $tmpfile5 > $tmptest

for c in $candidate;do
    tmpfile9=$(mktemp)
    tmpmodel=$(mktemp)
    tmpresult=$(mktemp)
    crf_learn -c ${c} -p 8 template $tmptrain $tmpmodel
    crf_test -m $tmpmodel $tmptest > $tmpresult
    echo "SECOND TRY: c=${c}" >> $resultfile
    ./result.py $tmpresult >> $resultfile
done

# THIRD TRY
cat $tmpfile1 $tmpfile2 > $tmpfile7
cat $tmpfile4 $tmpfile5 > $tmpfile8

./mkdata.py $tmpfile7 $tmpfile8 > $tmptrain
./mkdata.py $tmpfile3 $tmpfile6 > $tmptest

for c in $candidate;do
    tmpfile9=$(mktemp)
    tmpmodel=$(mktemp)
    tmpresult=$(mktemp)
    crf_learn -c ${c} -p 8 template $tmptrain $tmpmodel
    crf_test -m $tmpmodel $tmptest > $tmpresult
    echo "THIRD TRY: c=${c}" >> $resultfile
    ./result.py $tmpresult >> $resultfile
done
