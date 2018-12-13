# -*- coding: utf-8 -*-
# Python 2.7.15

import MeCab
import codecs
import os
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

import mecab_test2 as mcb

msg= u'病院で体のチェックをしようと思っています」と話していました。'

src_location = "F:/Downloads/400+MB assorted LN txt file format/400+MB assorted LN txt file format/"

import combine
counter = 0
for root, dirs, files in os.walk(src_location):
    for i in files:
        counter = counter + 1
        print(str(counter) + ', ' + str(datetime.datetime.now().time()) + ', ' + i)
        fname = src_location + i
        fp = codecs.open(fname,'r', encoding='mbcs') # this dumb encoding
        data = fp.read()
        mcb.analyze_text(data, i)
        fp.close()

# src_file = u"カフカ／高橋義孝訳-変身.txt"
# fname = src_location + src_file
# fp =codecs.open(fname,'r', encoding='mbcs') # this dumb encoding
#
# data = fp.read()
# mcb.analyze_text(data, src_file)

# mcb.extract_kanji(data)
# mcb.extract_vocab(data)
#
# mcb.write_text_analysis_to_file('output_'+src_file)



print("success")
