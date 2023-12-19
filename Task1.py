import matplotlib.pyplot as plt
import numpy as np
import math as m
import xml.etree.ElementTree as et
import os.path


def func(x):
    a = 0
    function = -(1 + m.cos(12 * m.sqrt(x**2 + a**2)))/(0.5 * (x**2 + a**2) + 2)
    return function


xmin = -5.12
xmax = 5.12
step = 0.01
count = 1000

xlist = np.arange(xmin, xmax, step)
# xlist = np.linspace(xmin, xmax, count)
ylist = []

for i in range(len(xlist)):
    y = func(xlist[i])
    ylist.append(y)

if(os.path.exists('results') == False):
    os.mkdir('results')

data = et.Element('data')
for i in range(len(xlist)):
    item_row = et.SubElement(data, 'row')
    item_x = et.SubElement(item_row, 'x')
    item_y = et.SubElement(item_row, 'y')
    item_x.text = str(xlist[i])
    item_y.text = str(ylist[i])

ffile = et.ElementTree(data)
et.indent(ffile, space="\t", level=0)
ffile.write("results/results_1.xml", encoding="utf-8", xml_declaration=True)

plt.plot(xlist, ylist)
plt.savefig('results/plot_1.png', dpi=50, bbox_inches='tight')
plt.show()
