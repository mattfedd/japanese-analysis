# -*- coding: utf-8 -*-
# Python 2.7.15

# This script will analyze an input Japanese text string and produce the following
#   1. Dictionary of [kanji, frequency]
#   2. Dictionary of [vocab, frequency]

import MeCab
import codecs
import sys
import json
import os
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

vocab_list_item = {}
vocab_list = []
vocab_tracking_list = []

kanji_list_item = {}
kanji_list = []
kanji_tracking_list = []
total_kanji_count = 0

hayashi = {}

m = MeCab.Tagger('-Ochasen')

# input is unicode text
def analyze_text(data, filename=None):
    if(filename==None):
        filename = 'default.txt'

    # print(datetime.datetime.now().time() + ", ")

    global vocab_list_item
    global vocab_list
    global vocab_tracking_list
    global kanji_list_item
    global kanji_list
    global kanji_tracking_list
    global total_kanji_count
    global hayashi

    vocab_list_item = {}
    vocab_list = []
    vocab_tracking_list = []

    kanji_list_item = {}
    kanji_list = []
    kanji_tracking_list = []
    total_kanji_count = 0

    hayashi = {}

    extract_kanji(data)
    extract_vocab(data)
    calc_readability_Hayashi()
    write_text_analysis_to_file('output_' + filename)

# use unicode patterns to convert hiragana and katakana
def hira_to_kata_unicode(text):
    for i in range(0, len(text)):
        t = text[i]
        if(ord(t) >= 0x3041 and ord(t) <= 0x3097):
            t = unichr(ord(t) + 96)
        if(i == 0):
            text = t + text[1:]
        elif(i == len(text)-1):
            text = text[:len(text)-1] + t
        else:
            text = text[:i] + t + text[i+1:]
    return text

def kata_to_hira_unicode(text):
    for i in range(0, len(text)):
        t = text[i]
        if(ord(t) >= 0x30a1 and ord(t) <= 0x30f7):
            t = unichr(ord(t) - 96)
        if(i == 0):
            text = t + text[1:]
        elif(i == len(text)-1):
            text = text[:len(text)-1] + t
        else:
            text = text[:i] + t + text[i+1:]
    return text

def is_kanji_unicode(text):
    if(ord(text) >= 0x4e00 and ord(text) <= 0x9faf):
        return True
    return False

# index == 0 is the first character
def replace_char_in_string(index, text, new_char):
    output = ""
    if(index == 0):
        output = new_char + text[1:]
    elif(index == len(text)-1):
        output = text[:len(text)-1] + new_char
    else:
        output = text[:index] + t + text[index+1:]
    return output

# extract vocab, add to existing vocab list
# msg should be unicode
def extract_vocab(msg):
    msg_encode = msg.encode('cp932')
    # print(msg)
    node = m.parseToNode(msg_encode)

    fp = open("JLPT_vocab_json.txt", "r")
    JLPT_vocab_data = json.load(fp)
    fp.close()
    # print(type(JLPT_vocab_data))

    while node:
        # specific to ipadic, may need to change for unidic
        features = node.feature.split(',')
        # print(features[6])
        base_form = features[6].decode('shift-jis')
        pos1 = features[0].decode('shift-jis')
        pos2 = features[1].decode('shift-jis')

        # TODO : investigate this weirdness here. Why does it sometimes not provide the full output features?
        pronunciation_hira =""
        if(len(features) > 7):
            pronunciation_hira = kata_to_hira_unicode(features[7].decode('shift-jis'))

        vocab_list_item = {}
        vocab_list_item['freq'] = 1
        vocab_list_item['val'] = base_form
        vocab_list_item['pronunciation_hira'] = pronunciation_hira
        # vocab_list_item['JLPT'] = 0

        try:
            b = vocab_tracking_list.index(vocab_list_item['val'])
        except ValueError:
            # did not find existing vocab word
            # try:
            #     JLPT_match_data = next(item for item in JLPT_vocab_data if item["kanji"] == base_form)
            #     vocab_list_item['JLPT'] = JLPT_match_data["JLPT"]
            # except StopIteration:
            #     pass
            # else:
            #     pass
            vocab_list.append(vocab_list_item)
            vocab_tracking_list.append(vocab_list_item['val'])
            pass
        else:
            # we did find one whoo
            vocab_list[b]['freq'] = vocab_list[b]['freq'] + 1

        node=node.next

# extract kanji, add to existing kanji list
def extract_kanji(msg):
    global total_kanji_count
    msg_len = len(msg)
    for i in range(0, msg_len):
        moji = msg[i]
        if(is_kanji_unicode(moji)):
            total_kanji_count = total_kanji_count + 1
            kanji_list_item = {}
            kanji_list_item['freq'] = 1
            kanji_list_item['val'] = moji

            try:
                b = kanji_tracking_list.index(kanji_list_item['val'])
            except ValueError:
                # did not find existing kanji
                kanji_list.append(kanji_list_item)
                kanji_tracking_list.append(kanji_list_item['val'])
                pass
            else:
                # we did find one whoo
                kanji_list[b]['freq'] = kanji_list[b]['freq'] + 1

    # print("total kanji count is " + str(total_kanji_count))

def write_text_analysis_to_file(filename=None):
    if(filename == None):
        filename = __file__.split('.')[0] + "_output.txt"

    sorted_kanji = sorted(kanji_list, key=lambda k: k['freq'], reverse=True)
    sorted_vocab = sorted(vocab_list, key=lambda k: k['freq'], reverse=True)
    print(len(vocab_list))
    json_data = {}
    json_data["total_unique_kanji"] = len(sorted_kanji)
    json_data["total_unique_vocab"] = len(sorted_vocab)

    #remove after hayashi is implemented
    hayashi = {}
    hayashi["text_length"] = 0
    hayashi["num_roman_chars"] = 0
    hayashi["num_hiragana_chars"] = 0
    hayashi["num_katakana_chars"] = 0
    hayashi["num_kanji_chars"] = 0
    hayashi["num_touten_chars"] = 0
    hayashi["num_kuten_chars"] = 0
    hayashi["avg_sentence_length"] = 0
    hayashi["avg_roman_length"] = 0
    hayashi["avg_hiragana_length"] = 0
    hayashi["avg_katakana_length"] = 0
    hayashi["avg_kanji_length"] = 0
    hayashi["ratio_touten_kuten"] = 0
    hayashi["score"] = 0

    json_data["hayashi"] = hayashi

    json_data["kanji"] = sorted_kanji
    json_data["vocab"] = sorted_vocab

    fp = open(filename, "w")
    json.dump(json_data, fp)
    fp.close()

def calc_readability_Hayashi():
    return 0

def calc_readability_obi2():
    return 0

def read_text_analysis_from_file(filename):
    fp = open(filename, "r")
    json_data = json.load(fp)
    fp.close()
    return json_data
