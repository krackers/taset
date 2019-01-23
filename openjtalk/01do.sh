
./openjtalk.sh
./mkdata.py in/e_label_test.txt in/e_result.abs > data.txt
for s in $(seq 1 999);do 
    echo $s;
    ./convertlab.py jtalk_out/s${s}.lab data/s${s}.txt > convertedlab/s${s}.lab;
done;

# 読みが間違っているものは取り除く
for s in $(seq 1 999);do 
    if [ $(wc -l convertedlab/s${s}.lab | sed "s; .*;;g") -ne $(wc -l jtalk_out/s${s}.lab | sed "s; .*;;g") ];then 
	rm convertedlab/s${s}.lab;
    fi;
done;
./htsengine.sh
