import os.path
import requests as r
import re
import scipy.special as sci
import numpy as np
import matplotlib.pyplot as plt
import math


def JOrd(order, countt):
    jblist = (sci.spherical_jn(order, k[countt] * D / 2))
    return jblist


def HOrd(order, countt):
    yblist = (sci.spherical_yn(order, k[countt] * D / 2))
    hblist = (complex(JOrd(order, countt), yblist))
    return hblist


def AOrd(order, countt):
    anlist = (JOrd(order, countt) / HOrd(order, countt))
    return anlist


def BOrd(order, countt):
    bnlist = (((k[countt] * (D / 2) * JOrd(order - 1, countt) - order * JOrd(order, countt)) / (k[countt] * (D / 2) * HOrd(order - 1, countt) - order * HOrd(order, countt))))
    return bnlist


if(os.path.exists('download') == False):
    os.mkdir('download')
if(os.path.exists('results') == False):
    os.mkdir('results')

url = 'https://jenyay.net/uploads/Student/Modelling/task_02_01.txt'

file = r.get(url)
if file.ok is False:
    print('Smth went wrong')
    quit()

with open('download/Task2Parametrs.txt', 'wb') as f:
    f.write(file.content)
with open('download/Task2Parametrs.txt', 'r') as f:
    data = f.readlines()

needvar = data[11]
print(needvar)

pattern = r'(?<!\d)\d+[.]\d+|\d+|-\d+(?!\d)'
zn = re.findall(pattern, str(needvar))
print(zn)

D = float(zn[1])*10**float(zn[2])
fmin = float(zn[3])*10**float(zn[4])
fmax = float(zn[5])*10**float(zn[6])
c = 3*10**8
print(D)
print(fmin)
print(fmax)

count = 200
step = 25

flist = np.linspace(fmin, fmax, count)
k = []
for i in range(count):
    k.append(2 * math.pi * flist[i] / c)

j = 1
ssuumm = [0]*count
while j <= step:
    for i in range(count):
        ssuumm[i] += ((-1)**j * (j+0.5) * (BOrd(j, i) - AOrd(j, i)))
    j += 1

epr = []
lam = []
for i in range(count):
    epr.append((c ** 2 / (math.pi * flist[i] ** 2)) * (abs(ssuumm[i]) ** 2))
    lam.append(c/flist[i])

flist1 = flist.tolist()

with open('results/results_2.json', 'w') as f:
    f.write(f"{{\n    \"freq\": {flist1},\n    \"lambda\": {lam},\n    \"rcs\": {epr}\n}}")

plt.plot(flist, epr)
plt.show()
