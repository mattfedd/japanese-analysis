# -*- coding: utf-8 -*-
# Python 2.7.15

import MeCab
import codecs
import sys
import os
import xml.etree.ElementTree as ET

reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

class Kanji:

    def __init__(self, char, grade='', stroke_count='', freq='', jlpt='', on_readings=[], kun_readings=[], meanings_en=[]):
        self.char = char.encode('shift-jis')
        self.grade = grade
        self.jlpt = jlpt
        self.freq = freq
        self.stroke_count = stroke_count
        self.on_readings = on_readings
        self.kun_readings = kun_readings
        self.meanings_en = meanings_en

    def toDict(self):
        return_dict = {}
        return_dict["char"] = self.char.decode('shift-jis').encode('utf-8')
        return_dict["grade"] = self.grade
        return_dict["jlpt"] = self.jlpt
        return_dict["freq"] = self.freq
        return_dict["stroke_count"] = self.stroke_count
        return_dict["on_readings"] = self.on_readings
        return_dict["kun_readings"] = self.kun_readings
        return_dict["meanings_en"] = self.meanings_en

        return return_dict

    def __repr__(self):
        return "Kanji()"

    def __str__(self):
        str_out = self.char + ", " + self.grade + ", " + self.jlpt + ", " + self.freq + ", " + self.stroke_count
        return str_out


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

import json

filename =  __file__.split('.')[0] + "_output.txt"
with codecs.open(filename, 'w', 'shift-jis') as fp:
    fp.write("[")
    for kanji_dict in kanji_list:
        if kanji_dict['freq'] == '':
            continue
        json_string = json.dumps(kanji_dict, indent=4)
        fp.write(json_string)
        fp.write(",\r\n")
    fp.seek(-1, os.SEEK_END)
    fp.truncate()
    fp.write("]")


# m = MeCab.Tagger('')
# msg = u'私は今日もしないとね'
# msg_encode = msg.encode('shift-jis')
# print(msg)
# result = m.parse(msg_encode).split('\n')
# for r in result:print(r)

# filename = __file__.split('.')[0] + "_output.txt"
# fp = open(filename, "w")
# fp.write(msg_encode)
# fp.write('\r\n')
# for r in result:
#     fp.write(r)
#     fp.write('\r\n')
# fp.close()
#
# print("success")
