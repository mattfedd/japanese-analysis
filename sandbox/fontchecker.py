# -*- coding: utf-8 -*-
# Python 2.7.15

"""
Matplotlib font checker
Prints a figure displaying a variety of system fonts and their ability to produce Japanese text

@author: Mads Olsgaard, 2014

Released under BSD License.
"""

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
print(font_manager.findSystemFonts(fontpaths=None, fontext='ttf'))

fonts = ['Droid Sans', 'Vera', 'TakaoGothic', 'TakaoPGothic', 'Liberation Sans', 'ubuntu', 'FreeSans', 'Droid Sans Japanese', 'DejaVu Sans']
fonts = ['Arial', 'Times New Roman', 'osaka.unicode.ttf'] #uncomment this line on Windows and see if it helps!
fp = font_manager.FontProperties(fname=os.path.expanduser('C:\\WINDOWS\\Fonts\\osaka.unicode.ttf'))
english = u'The quick ...'
japanese = u'日本語'
x = 0.1
y = 1

# Buils headline
plt.text(x+0.5,y, 'english')
plt.text(x+0.7, y, 'japanese')
plt.text(x,y, 'Font name')
plt.text(0,y-0.05, '-'*100)
y -=0.1

for f in fonts:
    matplotlib.rc('font', family='DejaVu Sans')
    plt.text(x,y, f+':')
    matplotlib.rc('font', family=f)
    plt.text(x+0.5,y, english)
    plt.text(x+0.7, y, japanese)
    y -= 0.1
    print(f, font_manager.findfont(f))  # Sanity check. Prints the location of the font. If the font it not found, an error message is printed and the location of the fallback font is shown

plt.show()
