# -*- coding: utf-8 -*-
# Python 2.7.15

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
