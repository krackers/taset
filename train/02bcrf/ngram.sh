wget http://dumps.wikimedia.org/jawiki/20120410/jawiki-20120410-pages-articles.xml.bz2
mkdir wikidata
wp2txt ./jawiki-20120410-pages-articles.xml.bz2 -o ./wikidata
cat wikidata/jawiki-20120410-pages-articles.xml-*.txt | mecab | ./noun_ngram.py -n 1 | sort | uniq -c > 1-gram.txt
cat wikidata/jawiki-20120410-pages-articles.xml-*.txt | mecab | ./noun_ngram.py -n 2 | sort | uniq -c > 2-gram.txt
