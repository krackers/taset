TASET (Tokyo Accent Sandhi Estimation TookKit) は，
日本語アクセント結合を推定するプログラム群です．


========================================
・シンプルなアクセント推定（simple ディレクトリ）
予めモデルが同梱された，アクセント結合推定モジュールです．

train ディレクトリのもの学習して出来るモデルと異なる点は，
名詞連続 n-gram を利用していない点のみです．
名詞連続 n-gram を利用すると，モデルの読み込みに時間がかかる上，
精度向上はあまり大きくないため，ここでは採用していません．

cd simple
./01do.sh

を実行すると，input.txt にかかれた文章のアクセントを出力します．

なお，利用に先立ち，
mecab (unidic, utf-8)
cabocha　(unidic, utf-8)
crf++
をインストールしてパスを通しておく必要があります．

mecab や cabocha は，辞書に unidic，エンコードに utf-8 を
利用しているものでないと動作しないため注意してください．


========================================
・アクセント結合推定用モデルの学習・テスト（train ディレクトリ）

参考文献：
鈴木雅之，黒岩龍，印南圭祐，小林俊平，清水信哉，峯松信明，広瀬啓吉
条件付き確率場を用いた日本語東京方言のアクセント結合自動推定
電子情報通信学会論文誌 (submitted)

以下のコマンドを実行することで，モデルの学習・テストを実行できます．

cd train/01mkdata/
./00init.sh
./01do.sh
cd ../02bcrf/
./00init.sh
./02do.sh
cd ../03acrf/
./00init.sh
./02do.sh

詳細は，シェルスクリプトの中身を読んで下さい．
モデルの学習には，別途配布のデータベースが必要となります．
taset/train/01mkdata/in/jnas_test.txt
taset/train/01mkdata/in/jnas.txt
taset/train/01mkdata/in/label.txt 
これらのデータは，JNAS もしくは S-JNAS の購入者に限り無償配布しています．
利用したい方は，suzukimasayki (at) gmail.com に JNAS もしくは S-JNAS を
購入したことを証明できるものをお送り下さい．

また，
mecab (unidic, utf-8)
cabocha　(unidic, utf-8)
crf++
wp2txt
を内部で使用するので，予めパスを通しておいて下さい．

mecab や cabocha は，辞書に unidic，エンコードに utf-8 を
利用しているものでないと動作しないため注意してください．

wp2txt はコマンドラインから利用できる version 0.1.0 を使用することを想定しています．
wp2txt は内部で，ディレクトリの相対パスを指定しているので注意が必要です．


========================================
・openjtalk による音声合成

openjtalk のアクセントラベルを書き換えて音声合成ができます．

hts_engine
open_jtalk

は予めインストールし，シェルスクリプト内を自分の環境に書き換えて利用してください．
taset/openjtalk/00init.sh
taset/openjtalk/01do.sh
は，taset/train で作成したデータを音声合成するスクリプトです．

なお適切に書き換えることで，それ以外のデータを音声合成することも可能です．
詳しくは，openjtalk のドキュメントを参照ください．

--
Masayuki Suzuki 2012/08/29
