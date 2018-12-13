# -*- coding: utf-8 -*-
# Python 2.7.15

import json

# take one output file, add it to the big bad master file

def add_file(filename):
    master_file = 'output_master.txt'

    fp = open(filename, "r")
    json_data = json.load(fp)
    json_data['filename'] = filename[7:len(filename)-4]
    fp.close()

    try:
        fp = open(master_file, "r")
    except IOError:
        # does not exist, make empty file with empty json object
        fp = open(master_file, "w")
        data = []
        json.dump(data, fp)
        fp.close()
        fp = open(master_file, "r")
        pass
    else:
        pass

    master_data = json.load(fp)

    fp.close()

    master_data.append(json_data)

    fp = open(master_file, "w")
    json.dump(master_data, fp)
    fp.close()

# test
# add_file(u'output_カフカ／高橋義孝訳-変身.txt')
