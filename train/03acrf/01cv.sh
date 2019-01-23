
# 3-fold cross varidation を行う。
# 02do.sh でやっていることを何回もやっているだけ。

candidate=(1.2 1.0 0.8 0.6 0.4)

resultfile=out/cvresult.txt
./mktemplate.sh > template

tmpfile1=$(mktemp); tmpfile2=$(mktemp); tmpfile3=$(mktemp)
tmpfile4=$(mktemp); tmpfile5=$(mktemp); tmpfile6=$(mktemp)

head -n 25603 ./in/data_train.txt > $tmpfile1
tail -n 25558 ./in/data_train.txt > $tmpfile2
head -n 51217 ./in/data_train.txt | tail -n 25614 > $tmpfile3

head -n 25603 ./in/label_train.txt > $tmpfile4
tail -n 25558 ./in/label_train.txt > $tmpfile5
head -n 51217 ./in/label_train.txt | tail -n 25614 > $tmpfile6

# FIRST TRY
tmpfile7=$(mktemp); tmpfile8=$(mktemp); tmpfile9=$(mktemp); tmpfile10=$(mktemp);
tmptrain=$(mktemp); tmptest=$(mktemp)
cat $tmpfile2 $tmpfile3 > $tmpfile7
cat $tmpfile5 $tmpfile6 > $tmpfile8

./mkdata.py $tmpfile7 $tmpfile8 > $tmpfile9
./abs2rel.py $tmpfile9 > $tmptrain
./mkdata.py $tmpfile1 $tmpfile4 > $tmpfile10
./abs2rel.py $tmpfile10 > $tmptest

tmp1=$(mktemp); tmp2=$(mktemp); tmp3=$(mktemp); tmp4=$(mktemp);
tmp1rel=$(mktemp); tmp2rel=$(mktemp)
# ルールベースでやる
./rule.py $tmpfile9 > $tmp1
./rule.py $tmpfile10 > $tmp2
./abs2rel.py $tmp1 | cut -d " " -f 37 > $tmp1rel
./abs2rel.py $tmp2 | cut -d " " -f 37 > $tmp2rel

cut -d " " -f1-35 $tmptrain > $tmp3
cut -d " " -f36 $tmptrain > $tmp4
paste -d " " $tmp3 $tmp1rel $tmp4 > $tmptrain

cut -d " " -f1-35 $tmptest > $tmp3
cut -d " " -f36 $tmptest > $tmp4
paste -d " " $tmp3 $tmp2rel $tmp4 > $tmptest

for c in $candidate;do     
    tmpfile11=$(mktemp)
    tmpmodel=$(mktemp)
    tmpresult=$(mktemp)
    crf_learn -c ${c} -p 8 template $tmptrain $tmpmodel
    crf_test -m $tmpmodel $tmptest > $tmpfile11
    ./rel2abs.py $tmpfile11 > $tmpresult
    echo "FIRST TRY: c=${c}" >> $resultfile
    ./result.py $tmpresult >> $resultfile
done

# SECOND TRY
cat $tmpfile1 $tmpfile3 > $tmpfile7
cat $tmpfile4 $tmpfile6 > $tmpfile8

./mkdata.py $tmpfile7 $tmpfile8 > $tmpfile9
./abs2rel.py $tmpfile9 > $tmptrain
./mkdata.py $tmpfile2 $tmpfile5 > $tmpfile10
./abs2rel.py $tmpfile10 > $tmptest

tmp1=$(mktemp); tmp2=$(mktemp); tmp3=$(mktemp); tmp4=$(mktemp);
tmp1rel=$(mktemp); tmp2rel=$(mktemp)
# ルールベースでやる
./rule.py $tmpfile9 > $tmp1
./rule.py $tmpfile10 > $tmp2
./abs2rel.py $tmp1 | cut -d " " -f 37 > $tmp1rel
./abs2rel.py $tmp2 | cut -d " " -f 37 > $tmp2rel

cut -d " " -f1-35 $tmptrain > $tmp3
cut -d " " -f36 $tmptrain > $tmp4
paste -d " " $tmp3 $tmp1rel $tmp4 > $tmptrain

cut -d " " -f1-35 $tmptest > $tmp3
cut -d " " -f36 $tmptest > $tmp4
paste -d " " $tmp3 $tmp2rel $tmp4 > $tmptest

for c in $candidate;do     
    tmpfile11=$(mktemp)
    tmpmodel=$(mktemp)
    tmpresult=$(mktemp)
    crf_learn -c ${c} -p 8 template $tmptrain $tmpmodel
    crf_test -m $tmpmodel $tmptest > $tmpfile11
    ./rel2abs.py $tmpfile11 > $tmpresult
    echo "SECOND TRY: c=${c}" >> $resultfile
    ./result.py $tmpresult >> $resultfile
done

# THIRD TRY
cat $tmpfile1 $tmpfile2 > $tmpfile7
cat $tmpfile4 $tmpfile5 > $tmpfile8

./mkdata.py $tmpfile7 $tmpfile8 > $tmpfile9
./abs2rel.py $tmpfile9 > $tmptrain
./mkdata.py $tmpfile3 $tmpfile6 > $tmpfile10
./abs2rel.py $tmpfile10 > $tmptest

tmp1=$(mktemp); tmp2=$(mktemp); tmp3=$(mktemp); tmp4=$(mktemp);
tmp1rel=$(mktemp); tmp2rel=$(mktemp)
# ルールベースでやる
./rule.py $tmpfile9 > $tmp1
./rule.py $tmpfile10 > $tmp2
./abs2rel.py $tmp1 | cut -d " " -f 37 > $tmp1rel
./abs2rel.py $tmp2 | cut -d " " -f 37 > $tmp2rel

cut -d " " -f1-35 $tmptrain > $tmp3
cut -d " " -f36 $tmptrain > $tmp4
paste -d " " $tmp3 $tmp1rel $tmp4 > $tmptrain

cut -d " " -f1-35 $tmptest > $tmp3
cut -d " " -f36 $tmptest > $tmp4
paste -d " " $tmp3 $tmp2rel $tmp4 > $tmptest

for c in $candidate;do     
    tmpfile11=$(mktemp)
    tmpmodel=$(mktemp)
    tmpresult=$(mktemp)
    crf_learn -c ${c} -p 8 template $tmptrain $tmpmodel
    crf_test -m $tmpmodel $tmptest > $tmpfile11
    ./rel2abs.py $tmpfile11 > $tmpresult
    echo "THIRD TRY: c=${c}" >> $resultfile
    ./result.py $tmpresult >> $resultfile
done
