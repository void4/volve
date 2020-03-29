import os
from time import time
from random import random
from collections import Counter
from tempfile import TemporaryFile

from PIL import Image, ImageDraw

from vm import execute, generate_random, mutate, F_GAS, W, H

SCALE = 2

img = Image.new("RGB", (W,H))

index = 0

colorcounter = None

IMAGEDIR = "results"

os.makedirs(IMAGEDIR, exist_ok=True)

def output(x, y, value):
    global img, index

    pixel = index // 3

    x = x#pixel % W
    y = y#pixel // W

    rgbindex = index % 3

    pixelvalue = list(img.getpixel((x,y)))
    pixelvalue[rgbindex] = value
    pixelvalue = tuple(pixelvalue)

    if rgbindex == 2:
        colorcounter[pixelvalue] += 1

    img.putpixel((x,y), pixelvalue)

    index += 1

    if index//3 >= W*H:

        tmpfile = TemporaryFile()
        img.save(tmpfile, "png")
        compressed_imgbytes = tmpfile.tell()
        imgbytes = W*H*3
        ratio = compressed_imgbytes/imgbytes
        print("Result .png compression ratio:", ratio)

        img = img.resize((W*SCALE, H*SCALE))
        img.save(IMAGEDIR + "/" + str(int(time()*1000))+".png")
        exit(0)

pool = {}
best = None
queue = []

def evolve():
    global colorcounter, pool, best, queue
    while True:
        colorcounter = Counter()

        if random() < 0.9 and len(queue) > 0:
            state = queue.pop(0)
        else:
            state = generate_random()

        startgas = state[F_GAS]

        execute(output, state)

        diffcolors = len(colorcounter)

        gasdelta = state[F_GAS] - startgas

        score = diffcolors - gasdelta

        if best is None or score > pool[best]:
            print("New best: ", score)
            key = str(state)
            pool[key] = score
            best = key

            for i in range(10):
                queue.append(mutate(state))
