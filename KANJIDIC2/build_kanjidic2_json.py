# -*- coding: utf-8 -*-
# Python 2.7.15

# The purpose of this script is to convert the big XML file (kanjidic2.xml) into json
# We can remove extra info that we don't need, and it's just easier for me to manipulate json

import MeCab
import codecs
import sys
import os
import xml.etree.ElementTree as ET
from kanji import Kanji

reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

def get_attrib_single(item, attrib):
    temp_iter = item.iter(attrib)

    try:
        temp_obj = temp_iter.next()
    except StopIteration:
        temp_obj = None
        temp_text = ''
        pass

    if(temp_obj is not None):
        temp_text = temp_obj.text

    return temp_text

filename = "kanjidic2.xml"
tree = ET.parse(filename)
root = tree.getroot()
# print(root[1][0].text)

kanji_list = []

j = 0
for character in root.findall('character'):

    char = get_attrib_single(character, 'literal')
    freq = get_attrib_single(character, 'freq')
    grade = get_attrib_single(character, 'grade')
    stroke_count = get_attrib_single(character, 'stroke_count')
    jlpt = get_attrib_single(character, 'jlpt')

    if freq =='':
        continue

    # get on readings
    temp = character.findall("./reading_meaning/rmgroup/*[@r_type='ja_on']")
    on_readings = [i.text for i in temp]
    # print(on_readings)

    # get kun readings
    temp = character.findall("./reading_meaning/rmgroup/*[@r_type='ja_kun']")
    kun_readings = [i.text for i in temp]
    # print(kun_readings)

    # check for meanings that don't have any attributes (length of attribute array is zero)
    # since english meanings have no attributes
    temp = filter(lambda x: len(x.attrib)==0, character.findall("./reading_meaning/rmgroup/meaning"))
    meanings_en = [i.text for i in temp]
    # print(meanings_en)

    try:
        c = char.encode('shift-jis') # some of the super rare kanji throw issues with shift-jis and unicode
    except UnicodeEncodeError:
        continue
        pass

    k = Kanji(char, grade, stroke_count, freq, jlpt, on_readings, kun_readings, meanings_en)
    kanji_list.append(k.toDict())
    print(k)

    # j = j+1
    # if(j > 10):
    #     break;

kanji_list = sorted(kanji_list, key=lambda k: int(k['freq']))

import json

filename =  __file__.split('.')[0] + "_output.txt"
with codecs.open(filename, 'w', 'shift-jis') as fp:
    fp.write("[")
    for kanji_dict in kanji_list:
        if kanji_dict['freq'] == '':
            continue
        json_string = json.dumps(kanji_dict, indent=4)
        fp.write(json_string)
        fp.write(",")
    fp.seek(-1, os.SEEK_END)
    fp.truncate()
    fp.write("]")
