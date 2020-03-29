import os
from time import time
from random import random
from collections import Counter

from PIL import Image, ImageDraw

from vm import execute, generate_random, mutate

W = H = 64

SCALE = 4

img = Image.new("RGB", (W,H))

index = 0

colorcounter = None

IMAGEDIR = "results"

os.makedirs(IMAGEDIR, exist_ok=True)

def output(value):
    global img, index

    pixel = index // 3

    x = pixel % W
    y = pixel // W

    rgbindex = index % 3

    pixelvalue = list(img.getpixel((x,y)))
    pixelvalue[rgbindex] = value
    pixelvalue = tuple(pixelvalue)

    if rgbindex == 2:
        colorcounter[pixelvalue] += 1

    img.putpixel((x,y), pixelvalue)

    index += 1

    if index//3 >= W*H:
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
        execute(output, state)

        diffcolors = len(colorcounter)

        if best is None or diffcolors > pool[best]:
            print("New best: ", diffcolors)
            key = str(state)
            pool[key] = diffcolors
            best = key

            for i in range(10):
                queue.append(mutate(state))
