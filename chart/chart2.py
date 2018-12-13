# -*- coding: utf-8 -*-
# Python 2.7.15

import json
from kanji import Kanji
import math
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

class Box:
    def __init__(self, kanji):
        self.kanji = kanji
        self.x = 0
        self.y = 0
        self.size = 20 # pixels

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setSize(self, size):
        self.size = size

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getSize(self):
        return self.size

    def __repr__(self):
        return "Box()"

    def __str__(self):
        str_out = self.kanji.char
        return str_out

def getColor(mode, input):
    # print(mode, input)
    if(mode == 1): #JLPT grades
        if(input == 1):
            return 'r'
        elif(input == 2):
            return '#ffa500'
        elif(input == 3):
            return 'y'
        elif(input == 4):
            return 'g'
        elif(input == 5):
            return 'b'
        else:
            return 'k'
    elif(mode == 2):
        if(input == 1):
            return 'pink'
        elif(input == 2):
            return 'm'
        elif(input == 3):
            return 'blueviolet'
        elif(input == 4):
            return 'c'
        elif(input == 5):
            return 'b'
        elif(input == 6):
            return 'g'
        elif(input == 7):
            return 'y'
        elif(input == 8):
            return 'orange'
        elif(input == 9):
            return 'r'
        elif(input == 10):
            return 'brown'
        elif(input == 11):
            return 'maroon'
        elif(input == 12):
            return 'deeppink'
        else:
            return 'k'
    elif(mode == 3):
        if(input == 0):
            return 'k'
        if(input > 0 and input < 0.2):
            return 'b'
        elif(input >= 0.2 and input < 0.4):
            return 'g'
        elif(input >= 0.4 and input < 0.6):
            return 'yellow'
        elif(input >= 0.6 and input < 0.8):
            return 'orange'
        elif(input >= 0.8 and input <= 1):
            return 'r'
        else:
            return 'w'
    else:
        pass

def getColorByFreq(freq):
    print("test")

# grab list of kanji, generate chart of boxes
filename = 'build_kanjidic2_json_output.txt'
fp = open(filename, "r")
json_data = json.load(fp)
fp.close()
json_data = sorted(json_data, key=lambda k: str(len(k['grade']))+k['grade'] if k['grade'] else 'z'*100)
boxlist = []

filename = u'output_ヤマグチノボル-ゼロの使い魔 外伝 タバサの冒険 1(青空文庫txt形式)[挿絵有](校正07-05-23)(軽量化).txt'
title = filename[7:len(filename)-4]
fp = open(filename, "r");
input_data = json.load(fp)
fp.close()

total_unique_kanji = input_data['total_unique_kanji']
total_unique_vocab = input_data['total_unique_vocab']
hayashi = input_data['hayashi']
kanji = input_data['kanji']
vocab = input_data['vocab']

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager
from matplotlib.textpath import TextPath
from matplotlib.path import Path

fop = font_manager.FontProperties(fname=os.path.expanduser('C:\\WINDOWS\\Fonts\\osaka.unicode.ttf'))
plt.rcParams['font.family'] = fop.get_name()
fig,ax = plt.subplots(1)
ax.set_xlim(0, 8)
ax.set_ylim(0, 4.6)
plt.style.use('ggplot')
plt.subplots_adjust(top=0.99,
bottom=0.01,
left=0.01,
right=0.99,
hspace=0.2,
wspace=0.2)

i = 0
boxsize = 0.1

boxpadding = 0.02
width = 66 #height is implicitly around 100-150 due to the total being ~2500

element = json_data[0]

for element in json_data:
    char = element['char']
    grade = element['grade']
    stroke_count = element['stroke_count']
    freq = element['freq']
    jlpt = element['jlpt']
    on_readings = element['on_readings']
    kun_readings = element['kun_readings']
    meanings_en = element['meanings_en']

    matching_data = next((item for item in kanji if item["val"] == char), None)

    frequency_data = 0

    if(matching_data != None):
        frequency_data = float(matching_data['freq']) / 515 # hard coded for now

    k = Kanji(char, grade, stroke_count, freq, jlpt, on_readings, kun_readings, meanings_en)
    b = Box(k)
    b.setSize(boxsize)
    x = (i % width) * (boxsize + boxpadding)
    y = (math.floor(i/width)) * (boxsize + boxpadding)
    b.setX(x)
    b.setY(y)

    boxlist.append(b)
    i = i + 1

    # print(x, y, i, char, b.getSize())
    # print(char)
    if(jlpt == u''):
        jlpt = u'0'
    if(grade == u''):
        grade = u'0'
    # boxcolor = getColor(1, int(jlpt))
    # boxcolor = getColor(2, int(grade))
    boxcolor = getColor(3, frequency_data)
    # boxcolor = 'r'
    boxalpha = 0.5* frequency_data+0.5
    # boxalpha = 1

    rect = patches.Rectangle((b.getX(),b.getY()),b.getSize(),b.getSize(),linewidth=2,edgecolor=boxcolor,facecolor='none', alpha=boxalpha)
    # plt.text(b.getX(),b.getY(), char, fontsize=28)
    tp1=TextPath((b.getX(),b.getY()+b.getSize()*0.15), char, size=0.1)
    polygon=tp1.to_polygons()
    for a in polygon:
        p1=patches.Polygon(a, fill=False, color='k')
        ax.add_patch(p1)
    ax.add_patch(rect)

plt.show()
