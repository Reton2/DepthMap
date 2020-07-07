# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 20:35:07 2019

@author: Reton2
"""
from PIL import Image
# import math
import sys
import time

Pds = 0.9
S = 16
Occlusion = 3.87
# math.log(Pds * math.sqrt(S) / ((1 - Pds) * math.sqrt(2 * math.pi)))

def costMap(pix1, y1, pix2, y2, width):

    def pixel_cost(i, j):
        if type(pix1[i, y1]) is not tuple:
            return ((pix1[i, y1] - pix2[j, y2])**2) / (2 * S)
        r, g, b = pix1[i, y1]
        z1 = 0.2989 * r + 0.5870 * g + 0.1140 * b
        r, g, b = pix2[j, y2]
        z2 = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return ((z1 - z2)**2) / (2 * S)

    def cost(i, j):
        if Map[i][j] != 0:
            return Map[i][j]
        a = 0
        if j == 0:
            a = i * Occlusion
        elif i == 0:
            a = j * Occlusion
        else:
            a = min([cost(i - 1, j - 1) + pixel_cost(i, j),
                     cost(i, j - 1) + Occlusion,
                     cost(i - 1, j) + Occlusion])
        return round(a, 3)

    Map = [[0 for i in range(0, width)] for j in range(0, width)]

    for i in range(1, width):
        Map[i][0] = cost(i, 0)
    for i in range(1, width):
        Map[0][i] = cost(0, i)
    for i in range(1, width):
        for j in range(1, width):
            a = cost(i, j)
            Map[i][j] = a

    return Map


def getLine(pix, x, y):
    arr = {}
    for i in range(0, x):
        arr[i] = pix[i, y]
    return arr


def make(Floats, width,):
    i = width - 1
    j = width - 1
    disi = [0] * width
    disj = [0] * width
    while i > 0 and j > 0:
        match = Floats[i - 1][j - 1]
        I_ = Floats[i - 1][j]
        J = Floats[i][j - 1]
        lis = [match, I_, J]
        if J == min(lis):
            disj[j] = abs(i - j) * 6
            j -= 1
        elif I_ == min(lis):
            disi[i] = abs(i - j) * 6
            i -= 1
        elif match == min(lis):
            disi[i] = abs(i - j) * 6
            disj[j] = abs(i - j) * 6
            i -= 1
            j -= 1
    return ((disi, disj))


def depth_map(left, right, result1, result2):
    img1 = Image.open(left)
    img2 = Image.open(right)
    width, height = img1.size
    thumb_size = 256
    try:
        size = thumb_size, thumb_size * height / width
        img1.thumbnail(size, Image.ANTIALIAS)
        img2.thumbnail(size, Image.ANTIALIAS)
    except IOError:
        print("cannot create thumbnail")
    pix1 = img1.load()
    pix2 = img2.load()

    (width, height) = img1.size
    my_listR = [255] * width * height
    my_listL = [255] * width * height
    imgR = Image.new('L', (width, height))
    imgL = Image.new('L', (width, height))

    for i in range(0, height):
        cost = costMap(pix1, i, pix2, i, width)
        (disi, disj) = make(cost, width)
        my_listL[i * width: (i + 1) * width] = disi
        my_listR[i * width: (i + 1) * width] = disj

    imgR.putdata(my_listR)
    imgL.putdata(my_listL)
    imgR.save(str(result2) + ".png")
    imgL.save(str(result1) + ".png")


if __name__ == '__main__':
    a = time.time()
    depth_map(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print(time.time() - a)
