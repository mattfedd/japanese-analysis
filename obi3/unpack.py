# -*- coding: utf-8 -*-
# Python 2.7.15

import json
import codecs
import struct

filename = 'Obi3-T13-f10-20120914.bsm'

fp = open(filename,'r')
data = fp.read()
print(type(data))


str1 = data[0:6].decode('utf8')

ngraml = 2
classn=13
freqsize = len(struct.pack('f', '0.0')) * classn
bsize = ngraml + len(struct.pack('I', '1')) + freqsize

#str[offset+ngraml, bsize-ngraml].unpack('Ie*')
freq = data[7:]

print(str1)
