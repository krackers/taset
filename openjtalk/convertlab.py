#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import itertools as it
import re
from optparse import OptionParser

def is_boin( p ):
    if p == "a" or p == "i" or p == "I" or p == "u" or p == "U" or p == "e" or p == "o":
        return True
    else:
        return False

def is_boinNcl( p ):
    if p == "a" or p == "i" or p == "I" or p == "u" or p == "U" or p == "e" or p == "o" or p == "N" or p == "cl":
        return True
    else:
        return False

def is_boinNclsilpau( p ):
    if p == "a" or p == "i" or p == "I" or p == "u" or p == "U" or p == "e" or p == "o" or p == "N" or p == "cl" or p == "sil" or p == "pau":
        return True
    else:
        return False

def katakana2roma( pron ):
    nonMoraList = set(u"ァ ィ ゥ ェ ォ ャ ュ ョ".split())
    index_mora = 0
    mora = []
    for p in pron.decode("utf-8"):
        if p not in nonMoraList:
            mora.append(p.encode("utf-8"))
            index_mora += 1
        else:
            mora[index_mora-1] += p.encode("utf-8")
    mora2roma = {
        "ア":["a"], "イ":["i"], "ウ":["u"], "エ":["e"], "オ":["o"],
        "カ":["k","a"], "キ":["k","i"], "ク":["k","u"], "ケ":["k","e"], "コ":["k","o"],
        "ガ":["g","a"], "ギ":["g","i"], "グ":["g","u"], "ゲ":["g","e"], "ゴ":["g","o"],
        "サ":["s","a"], "シ":["sh","i"], "ス":["s","u"], "セ":["s","e"], "ソ":["s","o"],
        "ザ":["z","a"], "ジ":["j","i"], "ズ":["z","u"], "ゼ":["z","e"], "ゾ":["z","o"],
        "スィ":["s","i"], "ズィ":["z","i"],
        "タ":["t","a"], "ティ":["t","i"], "トゥ":["t","u"] ,"テ":["t","e"], "ト":["t","o"],
        "ツ":["ts","u"],"ツィ":["ts","i"],
        "ダ":["d","a"], "ディ":["d","i"], "ドゥ":["d","u"], "デ":["d","e"], "ド":["d","o"],
        "ナ":["n","a"], "ニ":["n","i"], "ヌ":["n","u"], "ネ":["n","e"], "ノ":["n","o"],
        "ハ":["h","a"], "ヒ":["h","i"], "フ":["f","u"], "ヘ":["h","e"], "ホ":["h","o"],
        "ファ":["f","a"],"フィ":["f","i"], "フェ":["f","e"], "フォ":["f","o"], 
        "バ":["b","a"], "ビ":["b","i"], "ブ":["b","u"], "ベ":["b","e"], "ボ":["b","o"],
        "パ":["p","a"], "ピ":["p","i"], "プ":["p","u"], "ペ":["p","e"], "ポ":["p","o"],
        "マ":["m","a"], "ミ":["m","i"], "ム":["m","u"], "メ":["m","e"], "モ":["m","o"],
        "ヤ":["y","a"], "ユ":["y","u"], "ヨ":["y","o"],
        "ラ":["r","a"], "リ":["r","i"], "ル":["r","u"], "レ":["r","e"], "ロ":["r","o"],
        "ワ":["w","a"], "ウィ":["w","i"], "ウェ":["w","e"], "ウォ":["w","o"], "ン":["N"],
        "ッ":["cl"],
        "キャ":["ky","a"], "キュ":["ky","u"], "キェ":["ky","e"], "キョ":["ky","o"],
        "ギャ":["gy","a"], "ギュ":["gy","u"], "ギェ":["gy","e"], "ギョ":["gy","o"],
        "シャ":["sh","a"], "シュ":["sh","u"], "シェ":["sh","e"], "ショ":["sh","o"],
        "ジャ":["j","a"], "ジュ":["j","u"], "ジェ":["j","e"], "ジョ":["j","o"],
        "ダャ":["dy","a"], "デュ":["dy","u"], "デョ":["dy","o"], 
        "チャ":["ch","a"], "チ":["ch","i"], "チュ":["ch","u"], "チェ":["ch","e"], "チョ":["ch","o"],
        "ニャ":["ny","a"],"ニュ":["ny","u"], "ニェ":["ny","e"], "ニョ":["ny","o"],
        "ヒャ":["hy","a"], "ヒュ":["hy","u"], "ヒェ":["hy","e"], "ヒョ":["hy","o"],
        "ビャ":["by","a"], "ビュ":["by","u"], "ビェ":["by","e"], "ビョ":["by","o"],
        "ピャ":["py","a"], "ピュ":["py","u"], "ピェ":["py","e"], "ピョ":["py","o"],
        "ミャ":["my","a"], "ミュ":["my","u"], "ミェ":["my","e"], "ミョ":["my","o"],
        "リャ":["ry","a"], "リュ":["ry","u"], "リェ":["ry","e"], "リョ":["ry","o"]
        }
    roma = []
    for m in mora:
        if m == "ー":
            roma.append( roma[-1] )
        else:
            rr = mora2roma[ m ]
            for r in rr:
                roma.append( r )
    return roma


usage = u"""usage: %prog jtalklab datafile
jtalklab を読み込み、datafile の accent phrase, accent を反映させて出力する
"""
parser = OptionParser(usage=usage)
(options,args) = parser.parse_args()

if len(args) < 2:
    print >> sys.stderr, "Error: too few arguments\n"
    parser.print_help()
    exit()
jtalkfile, datafile = map(open, args[0:2])

reline = re.compile("(.+)\^(.+)\-(.+)\+(.+)=(.+)/A:(.+)\+(.+)\+(.+)/B:(.+)\-(.+)_(.+)/C:(.+)_(.+)\+(.+)/D:(.+)\+(.+)_(.+)/E:(.+)_(.+)!(.+)_(.+)\-(.+)/F:(.+)_(.+)#(.+)_(.+)@(.+)_(.+)\|(.+)_(.+)/G:(.+)_(.+)%(.+)_(.+)\-(.+)/H:(.+)_(.+)/I:(.+)\-(.+)@(.+)\+(.+)&(.+)\-(.+)\|(.+)\+(.+)/J:(.+)_(.+)/K:(.+)\+(.+)\-(.+)" )

# モーラ、アクセント句、ブレス、open_jtalk のラベルでそれぞれどこに区切りがあるのか表すリスト
mora_jb = []
phrase_jb = []
breath_jb = []

prev_a3 = ""

# mora_jb phrase_jb breath_jb を作成する
for ii, line in enumerate( jtalkfile ):

    begin_time, end_time, data = line.strip().split()

    # An example of context-dependent label format for HMM-based speech synthesis in Japanese
    # Keiichiro Oura 参照
    aa = reline.search( data )
    p1,p2,p3,p4,p5, a1,a2,a3, b1,b2,b3, c1,c2,c3, d1,d2,d3, e1,e2,e3,e4,e5, f1,f2,f3,f4,f5,f6,f7,f8, g1,g2,g3,g4,g5, h1,h2, i1,i2,i3,i4,i5,i6,i7,i8, j1,j2, k1,k2,k3 = aa.groups()

    # sil だったら、無視。
    if p3 == "sil":
        prev_a3 = a3        
        continue
    
    # pau だったら、すべての句切れ目。
    if p3 == "pau":
        mora_jb.append(ii)
        phrase_jb.append(ii)
        breath_jb.append(ii)
        prev_a3 = a3
        continue

    # [前が母音（及びその無声化 I or U） or N or cl だった場合] 
    if is_boinNcl(p2): 
        mora_jb.append(ii)

    # 1 モーラのアクセント句がないとして、
    # アクセント句内のモーラカウントの切り替えを検出
    if prev_a3 == "1" and a2 == "1":
        phrase_jb.append(ii)
        
    prev_a3 = a3

# アクセント句が、推定した結果（data）のラベルでそれぞれどこに区切りがあるのか表すリスト
phrase_db = []

# アクセント核が、それぞれのアクセント句で何モーラ目にあるか表すリスト
accent_mora = []
# それぞれのアクセント句で何モーラあるか表すリスト
count_mora = []

prons = []

ruisekimora = 0
for ii,line in enumerate(datafile):

    elems = line.split()
    count_mora.append( elems[2] )
    ruisekimora += int(elems[2])
    prons.append(elems[1])

    # 一番最後のアクセント句区切りは、いらない（アクセント句数は、区切り +1 個ある。）
    # それ以外は保存する。
    if ruisekimora < len(mora_jb)+1:
        phrase_db.append( mora_jb[ ruisekimora-1 ] )

    if elems[3] == "0":
        # 0 型の場合、最後のモーラにアクセントがあるとする
        accent = elems[2]
    else:
        accent = elems[3]
    accent_mora.append( accent )


# -------------------------------
# ここから新しいラベルを作成する
# -------------------------------

# jtalkfile を seek してもとに戻す
jtalkfile.seek(0)

mora_idx = 0
phrase_idx = 0
breath_idx = 0

mora_in_phrase_idx = 0
onso_in_phrase_idx = -1

for ii, line in enumerate( jtalkfile ):

    begin_time, end_time, data = line.strip().split()

    aa = reline.search( data )
    p1,p2,p3,p4,p5, a1,a2,a3, b1,b2,b3, c1,c2,c3, d1,d2,d3, e1,e2,e3,e4,e5, f1,f2,f3,f4,f5,f6,f7,f8, g1,g2,g3,g4,g5, h1,h2, i1,i2,i3,i4,i5,i6,i7,i8, j1,j2, k1,k2,k3 = aa.groups()

    orig_g1 = g1
    orig_g2 = g2
    # モーラ境界
    if mora_idx < len(mora_jb):
        if ii == mora_jb[ mora_idx ]:
            mora_idx += 1
            mora_in_phrase_idx += 1
            #print "m"
    # 【データファイルから読み込んだ】アクセント句境界
    if phrase_idx < len(phrase_db):
        if ii == phrase_db[ phrase_idx ]:
            phrase_idx += 1
            mora_in_phrase_idx = 0
            onso_in_phrase_idx = -1
            #print "p"
    # ブレス境界
    if breath_idx < len(breath_jb):
        if ii == breath_jb[ breath_idx ]:
            breath_idx += 1
            #print "b"
    # 音素境界
    if p3 != "sil" and p3 != "pau":
        onso_in_phrase_idx += 1

    
    if p3 == "sil" or p3 == "pau":
        a1 = "xx"
        a2 = "xx"
        a3 = "xx"
        e5 = "xx"
        f1 = "xx"
        f2 = "xx"
        f5 = "xx"
        f6 = "xx"
        f7 = "xx"
        f8 = "xx"
        g5 = "xx"
        i1 = "xx"
        i2 = "xx"
        prev_is_silpau = True
    else:

        # 読みが間違っていたら、途中でやめる。（途中で切れているものは後で rm する）
        dataroma = katakana2roma( prons[phrase_idx] )
        dataonso = dataroma[onso_in_phrase_idx]
        if dataonso.lower() != p3.lower():
            print >> sys.stderr, "Error: yomimatsugai"
            exit()
        
        # a1: the difference between accent type and position of the current mora identity
        a1 = str( 1 + mora_in_phrase_idx - int(accent_mora[ phrase_idx ]) )
        # a2: position of the current mora identity in the current accent phrase (forward)
        a2 = str( 1 + mora_in_phrase_idx )
        # a3: position of the current mora identity in the current accent phrase (backward)
        a3 = str( int(count_mora[ phrase_idx ]) - mora_in_phrase_idx )

        # e5: whether pause insertion or not in between the previous accent phrase and the current accent phrase (true==0, false==1)
        if 0 < phrase_idx:
            if 0 < breath_idx:
                if phrase_db[ phrase_idx-1 ] == breath_jb[ breath_idx-1 ]:
                    e5 = "0"
                else:
                    e5 = "1"
            else:
                e5 = "1"
        else:
            e5 = "xx"

        # g5: whether pause insertion or not in between the next accent phrase and the current accent phrase (true==0, false==1)
        if phrase_idx < len( phrase_db ):
            if breath_idx < len( breath_jb ):
                if phrase_db[ phrase_idx ] == breath_jb[ breath_idx ]:
                    g5 = "0"
                else:
                    g5 = "1"
            # 最後最後のブレス句
            else:
                g5 = "1"
        else:
            # 最後のアクセント句
            g5 = "xx"



        # f1: the number of moras in the current accent phrase
        f1 = count_mora[ phrase_idx ]
        # f2: accent type in the current accent phrase
        f2 = accent_mora[ phrase_idx ]

        # f5:position of the current accent phrase identity in the current breath group by the accent phrase (forward)
        # f6:position of the current accent phrase identity in the current breath group by the accent phrase (backward)
        # f7:position of the current accent phrase identity in the current breath group by the mora (forward)
        # f8:position of the current accent phrase identity in the current breath group by the mora (backward)
        if breath_idx != 0:
            tmp_begin = breath_jb[ breath_idx-1 ]
        else:
            tmp_begin = 0

        if breath_idx < len(breath_jb):
            tmp_end = breath_jb[ breath_idx ]

        else:
            tmp_end = 100000 # large number

        all_ap_incb = 0
        all_mo_incb = 0
        for index, jj in enumerate(phrase_db):
            if tmp_begin < jj and jj <= tmp_end:
                all_ap_incb += 1
                all_mo_incb += int(count_mora[index])
                if phrase_idx < len(phrase_db):
                    if jj == phrase_db[ phrase_idx ]:
                        now_ap_incb = all_ap_incb
                        now_mo_incb = all_mo_incb
                
        # 最後のbreath
        if breath_idx == len(breath_jb):
            all_ap_incb += 1
            all_mo_incb += int(count_mora[-1])
        # 最後のフレーズ
        if phrase_idx == len(phrase_db):
            now_ap_incb = all_ap_incb
            now_mo_incb = all_mo_incb
        # now_mo_incb は、アクセント句の先頭のモーラにおく
        now_mo_incb = now_mo_incb - int(count_mora[ phrase_idx ]) + 1
        
        f5 = str( now_ap_incb )
        f6 = str( all_ap_incb + 1 - now_ap_incb )
        
        f7 = str( now_mo_incb )
        f8 = str( all_mo_incb + 1 - now_mo_incb )

        # i1: the number of accent phrases in the current breath group by the accent phrase
        # i2: the number of accent phrases in the current breath group by the the mora

        i1 = all_ap_incb
        i2 = all_mo_incb

        # 最後の sil では、h1,h2 に i1,i2 をいれるので（openjtalk のバグ）保存しておく
        prev_i1 = i1
        prev_i2 = i2

        # i3: position of this utterance identity by breath group (forward)
        # i4: position of this utterance identity by breath group (backward)
        # i5: position of this utterance identity by accent phrase (forward)
        # i6: position of this utterance identity by accent phrase (backward)
        # i7: position of this utterance identity by mora (forward)
        # i8: position of this utterance identity by mora (backward)
        # という上記は、間違いで、本当は this utterance でなく this breath group。というバグがあるので、それに合わせる

        if prev_is_silpau:
            i3 = breath_idx + 1
            i4 = len( breath_jb ) - breath_idx + 1
            i5 = phrase_idx + 1
            i6 = len( phrase_db ) - phrase_idx + 1
            i7 = mora_idx + 1
            i8 = len( mora_jb ) - mora_idx + 1
            prev_i5 = i5
            prev_i6 = i6
            prev_i7 = i7
            prev_i8 = i8
        else:
            i5 = prev_i5
            i6 = prev_i6
            i7 = prev_i7
            i8 = prev_i8

        prev_is_silpau = False

    # ----------------------
    # sil pau も共通の処理
    if 0 < phrase_idx:
        # e1: the number of moras in the previous accent phrase
        e1 = count_mora[ phrase_idx-1 ]
        # e2: accent type in the previous accent phrase
        e2 = accent_mora[ phrase_idx-1 ]
    else:
        e1 = "xx"
        e2 = "xx"

    if phrase_idx < len( phrase_db ):
        # g1: the number of moras in the next accent phrase
        g1 = count_mora[ phrase_idx+1 ]
        # g2: accnt type in the next accent phrase
        g2 = accent_mora[ phrase_idx+1 ]
    else:
        g1 = "xx"
        g2 = "xx"
    # pau の場合は g1 は一つ前のを入れる
    if p3 == "pau":
        g1 = prev_g1
        g2 = prev_g2

    # h1: the number of accent phrases in the previous breath group by the accent phrase
    # h2: the number of accent phrases in the previous breath group by the the mora
    if breath_idx > 1:
        tmp_begin = breath_jb[ breath_idx-2 ]
    else:
        tmp_begin = 0
        
    if breath_idx != 0:
        tmp_end = breath_jb[ breath_idx-1 ]
    else:
        tmp_end = 0 

    all_ap_inpb = 0
    all_mo_inpb = 0
    for index, jj in enumerate(phrase_db):
        if tmp_begin < jj and jj <= tmp_end:
            all_ap_inpb += 1
            all_mo_inpb += int(count_mora[index])

    if breath_idx != 0:
        h1 = str( all_ap_inpb )
        h2 = str( all_mo_inpb )
    else:
        h1 = "xx"
        h2 = "xx"

    # 一番最後の sil だけ、なぜか h1,h2 に current のもの（i1,i2）が入っているので、それに合わせる
    # あと、e1,e2 も、一つ前の f1,f2 に変える。
    if p3 == "sil" and mora_idx == len( mora_jb ):
        h1 = prev_i1
        h2 = prev_i2
        e1 = prev_f1
        e2 = prev_f2

    # j1: the number of accent phrases in the next breath group by the accent phrase
    # j2: the number of accent phrases in the next breath group by the the mora
    if breath_idx < len(breath_jb):
        tmp_begin = breath_jb[ breath_idx ]
    else:
        tmp_begin = 0
        
    if breath_idx < len(breath_jb)-1:
        tmp_end = breath_jb[ breath_idx+1 ]
    else:
        tmp_end = 100000 # large number

    all_ap_innb = 0
    all_mo_innb = 0
    for index, jj in enumerate(phrase_db):
        if tmp_begin < jj and jj <= tmp_end:
            all_ap_innb += 1
            all_mo_innb += int(count_mora[index])

    # 最後かその一つ手前の breath だった場合
    if breath_idx == len(breath_jb) or breath_idx == len(breath_jb)-1:
        all_ap_innb += 1
        all_mo_innb += int(count_mora[-1])

    if breath_idx < len(breath_jb):
        j1 = str( all_ap_innb )
        j2 = str( all_mo_innb )
    else:
        j1 = "xx"
        j2 = "xx"

    # pau の場合は、一つ前の j1,j2 を使う
    if p3 == "pau":
        j1 = prev_j1
        j2 = prev_j2
    
    # 一番最初の sil だけ、なぜか j1,j2 に current のものが入っているので、それに合わせる
    # あと、g1,g2 はわけわからん値がはいっているので、とりあえずコピーしておく
    if p3 == "sil" and mora_idx == 0:
        tmp_begin = 0
        if breath_idx < len(breath_jb):
            tmp_end = breath_jb[ breath_idx ]
        else:
            tmp_end = 100000 # large number

        all_ap_incb = 0
        all_mo_incb = 0
        for index, jj in enumerate(phrase_db):
            if tmp_begin < jj and jj <= tmp_end:
                all_ap_incb += 1
                all_mo_incb += int(count_mora[index])
        #  breath フレーズが一つしかない場合
        if len(breath_jb) == 0:
            all_ap_incb += 1
            all_mo_incb += int(count_mora[-1])
        j1 = str(all_ap_incb)
        j2 = str(all_mo_incb)

        g1 = orig_g1
        g2 = orig_g2

    prev_j1 = j1
    prev_j2 = j2
    prev_f1 = f1
    prev_f2 = f2
    prev_g1 = g1
    prev_g2 = g2

    k1 = len(breath_jb) + 1
    k2 = len(phrase_db) + 1
    k3 = len(mora_jb) + 1
    
    print begin_time,
    print end_time,
    print "%s^%s-%s+%s=%s/A:%s+%s+%s/B:%s-%s_%s/C:%s_%s+%s/D:%s+%s_%s/E:%s_%s!%s_%s-%s/F:%s_%s#%s_%s@%s_%s|%s_%s/G:%s_%s%%%s_%s-%s/H:%s_%s/I:%s-%s@%s+%s&%s-%s|%s+%s/J:%s_%s/K:%s+%s-%s" \
          % (p1,p2,p3,p4,p5, a1,a2,a3, b1,b2,b3, c1,c2,c3, d1,d2,d3, e1,e2,e3,e4,e5, f1,f2,f3,f4,f5,f6,f7,f8, g1,g2,g3,g4,g5, h1,h2, i1,i2,i3,i4,i5,i6,i7,i8, j1,j2, k1,k2,k3)
    
