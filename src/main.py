# -*- coding: utf-8 -*-
# obrabotka plansheta
# Иванов А.А. 2023
# v3 FINAL самая последняя версия НЕ УДАЛЯТЬ !!!
# 14.03 добавил статистику
# 21.03 поправил график (Маша просила подписи покрупнее)

import os
import sys
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
# import seaborn as sns
# import pandas as pd

t0 = time.time()

PATH = "C:\\Users\\Ivanov\\Desktop\\работа\\данные\\plate_2024_03_14.csv"
OUT = "C:\\Users\\Ivanov\\Desktop\\работа\\результаты\\"

RESULTS = []
BAD = []


def read_plate():
    f = open(PATH)
    lines = f.readlines()
    data = {}
    n = 0
    for l in lines:
        n = n + 1
        if n <= 4:
            continue
        l = l.replace("\n", "")
        if l == "":
            continue
        p = l.split(";")
        name = p[0]
        vals = []
        for i in range(1, 13):
            try:
                vals.append(float(p[i]))
            except:
                pass
        data[name] = vals
        print("прочитано", name, len(vals))
    return data


def norm(v):
    b = v[0]
    c = v[1]
    out = []
    for i in range(2, 12):
        x = (v[i] - b) / (c - b) * 100
        if x > 100:
            x = 100
        if x < 0:
            x = 0
        out.append(x)
    return out


def ic50(y):
    c = []
    x = 100.0
    for i in range(10):
        c.append(x)
        x = x / 2
    res = -1
    for i in range(9):
        if y[i] < 50 and y[i + 1] >= 50:
            x1 = math.log10(c[i])
            x2 = math.log10(c[i + 1])
            k = (y[i + 1] - y[i]) / (x2 - x1)
            if abs(k) < 1e-9:
                continue
            xx = x1 + (50 - y[i]) / k
            res = 10 ** xx
    return res


d = read_plate()
print("всего строк", len(d))
print("!!!!! ТУТ")

# ------- серия A -------
serA = []
for k in ["A", "B", "C", "D"]:
    v = d[k]
    y = norm(v)
    serA.append(y)
    z = ic50(y)
    RESULTS.append([k, z, y[9]])
    if z == -1:
        BAD.append(k)
    print(k, "IC50 =", z, "остаточная жизнеспособность", y[9])

# ------- серия B -------
serB = []
for k in ["E", "F", "G", "H"]:
    v = d[k]
    y = norm(v)
    serB.append(y)
    z = ic50(y)
    RESULTS.append([k, z, y[9]])
    if z == -1:
        BAD.append(k)
    print(k, "IC50 =", z, "остаточная жизнеспособность", y[9])

print("не посчиталось:", BAD)

a = []
for s in serA:
    a.append(s[0])
b = []
for s in serB:
    b.append(s[0])

t, p = stats.ttest_ind(a, b)
print("t =", t, "p =", p)
if p < 0.05:
    print("РАЗЛИЧИЯ ЕСТЬ")
else:
    print("различий нет")

m1 = sum(a) / 4
m2 = sum(b) / 4
print("среднее по серии A", m1)
print("среднее по серии B", m2)
print("разница", m1 - m2, "%")

# for x in RESULTS:
#     if x[1] > 50:
#         print("проверить", x[0])

cc = []
xx = 100.0
for i in range(10):
    cc.append(xx)
    xx = xx / 2

plt.figure(figsize=(8, 6))
i = 0
for k in ["A", "B", "C", "D"]:
    y = norm(d[k])
    yy = []
    for q in y:
        yy.append(q + np.random.rand() * 2)
    plt.plot(cc, yy, "o-", label=k)
    i = i + 1
for k in ["E", "F", "G", "H"]:
    y = norm(d[k])
    yy = []
    for q in y:
        yy.append(q + np.random.rand() * 2)
    plt.plot(cc, yy, "s--", label=k)
plt.xscale("log")
plt.axhline(50, color="k")
plt.xlabel("концентрация, мкМ", fontsize=14)
plt.ylabel("жизнеспособность, %", fontsize=14)
plt.title("Планшет 14.03.2024")
plt.legend()
plt.savefig(OUT + "graph.png", dpi=300)
print("график сохранён")

r = open(OUT + "report.txt", "w")
r.write("ОТЧЁТ\n")
r.write("файл: " + PATH + "\n")
for x in RESULTS:
    r.write(x[0] + "\t" + str(x[1]) + "\t" + str(x[2]) + "\n")
r.write("t = " + str(t) + " p = " + str(p) + "\n")
r.close()

print("отчёт записан в", OUT + "report.txt")
print("время работы", time.time() - t0)
print("ГОТОВО")