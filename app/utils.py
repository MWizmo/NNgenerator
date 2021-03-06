import math
import numpy as np
import csv
import os
from app import app, db
from flask import flash
from app.models import Task


def randomize(rMin, rMax, fiMin, fiMax, gMin, gMax):
    rObj = np.random.uniform(rMin, rMax)
    fiObj = np.random.uniform(fiMin, fiMax)
    gObj = np.random.uniform(gMin, gMax)
    xObj = rObj * math.cos(fiObj)
    yObj = rObj * math.sin(fiObj)
    return xObj, yObj, gObj, fiObj, rObj


def valid(xObj, yObj, gObj, h, l):
    t = math.sqrt(4 * pow(h, 2) - pow(l, 2)) * yObj
    cond1 = t + l * xObj > l * h
    cond2 = t - l * xObj > l * h
    cond3 = abs(-l * xObj - t + l * h) > 2 * h * gObj
    cond4 = abs(l * xObj - t + l * h) > 2 * h * gObj
    return cond1 and cond2 and cond3 and cond4


def F_a(x, y, r, h):
    if y >= 0 and x + h >= 0:
        return math.asin(y / r)
    elif y >= 0 and x + h < 0:
        return math.pi - math.asin(y / r)
    elif y < 0 and x + h < 0:
        return math.pi + math.asin(abs(y) / r)
    elif y < 0 and x + h >= 0:
        return 2 * math.pi - math.asin(abs(y) / r)


def F_b(x, y, r, h):
    if y >= 0 and x - h >= 0:
        return math.asin(y / r)
    elif y >= 0 and x - h < 0:
        return math.pi - math.asin(y / r)
    elif y < 0 and x - h < 0:
        return math.pi + math.asin(abs(y) / r)
    elif y < 0 and x - h >= 0:
        return 2 * math.pi - math.asin(abs(y) / r)


def count(xObj, yObj, h, gObj, m):
    rA = math.sqrt(pow((xObj + h), 2) + pow(yObj, 2))
    fiA = F_a(xObj, yObj, rA, h)
    rB = math.sqrt(pow((xObj - h), 2) + pow(yObj, 2))
    fiB = F_b(xObj, yObj, rB, h)
    L_a = math.floor((m / (2 * math.pi)) * (fiA - math.asin(gObj / rA)))
    R_a = math.floor((m / (2 * math.pi)) * (fiA + math.asin(gObj / rA)))
    L_b = math.floor((m / (2 * math.pi)) * (fiB - math.asin(gObj / rB)))
    R_b = math.floor((m / (2 * math.pi)) * (fiB + math.asin(gObj / rB)))
    return L_a, R_a, L_b, R_b


def generate(h, l, m, n, rMin, rMax, fiMin, fiMax, gMin, gMax, lambd, gamma, task_id):
    M = []
    for i in range(0, n):
        beta_A = [0] * m
        beta_B = [0] * m
        flag1 = False
        flag2 = False
        loops = 0
        is_ok = True
        while not flag1:
            while not flag2:
                xObj, yObj, gObj, fiObj, rObj = randomize(rMin, rMax, fiMin, fiMax, gMin, gMax)
                flag2 = valid(xObj, yObj, gObj, h, l)
            L_a, R_a, L_b, R_b = count(xObj, yObj, h, gObj, m)
            flag1 = L_a != R_a
            loops += 1
            if loops == 10:
                is_ok = False
                break
        Task.query.get(task_id).produced += 1
        db.session.commit()
        if not is_ok:
            continue
        for j in range(L_a, R_a + 1):
            beta_A[j] = 1
        for j in range(L_b, R_b + 1):
            beta_B[j] = 1
        d = math.tanh(lambd * (rObj / h))
        a = 1 / (1 + math.exp(-gamma * (math.pi / 2 - fiObj)))
        M.append({'beta_A': beta_A, 'beta_B': beta_B, 'd': d, 'a': a})
    save_to_file(M, m)


def save_to_file(dataset, m):
    filename = os.path.join(app.root_path, 'datasets', f'dataset-{m}.csv')
    with open(filename, 'a') as output:
        writer = csv.writer(output, delimiter=';')
        for row in dataset:
            writer.writerow(row['beta_A'] + row['beta_B'] + [row['d'], row['a']])
