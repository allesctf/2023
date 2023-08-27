from tpu import *
from PIL import Image
import numpy as np
import sys, random

minicat = """
___OO__________OO___: nop
____________________: nop
_________WW_________: nop
__WW____WWWW____WW__: nop
___WW__WW__WW__WW___: nop
____WWWW____WWWW____: nop
"""

meowcode = ["mov 109, UP", "mov 101, RIGHT", "mov 111, DOWN", "mov 119, LEFT"]

#catsounds = ["nyaa", "miao", "meow"]
#randomcap = lambda s : "".join([c.upper() if random.choice([0,1]) else c.lower() for c in s])

main = parse(open(sys.argv[1]).read())
offx = int(sys.argv[3])
offy = int(sys.argv[4])

im = Image.open(sys.argv[2]).convert("L")
im = np.array(im)

w,h = im.shape
for y in range(h):
    for x in range(w):
        if im[y][x] != 255:
            main["tpus"][(x+offx,y+offy)] = meowcode

write(main, sys.argv[5])
