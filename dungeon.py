import msvcrt
import random
from os import system, name
 
def clear():
    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')

w = int(input("Tile width:  "))
h = int(input("Tile height: "))
n = int(input("Deepness:    "))
grid = [['&&&' for x in range(w)] for y in range(h)]

class rectangle:
    def __init__(self, y1, x1, y2, x2):
        self.y1 = y1
        self.x1 = x1
        self.y2 = y2
        self.x2 = x2

bw = int(input("World width in tiles:  "))
bh = int(input("World height in tiles: "))
world = [[grid for x in range(bw)] for y in range(bh)]

bposy = 0
bposx = 0

posy = 0
posx = 0

def draw():
    clear()
    print(f"bposy: {bposy}, bposx: {bposx}, posy: {posy}, posx: {posx}")
    for y in range(h):
        for x in range(w):
            if y == posy and x == posx:
                print(" @ ", end=" ")
            else:
                print(world[bposy][bposx][y][x], end=" ")
        print()
    print()

def generate_world(by, bx):
    i = 0
    invert = False

    while i < n:
        
        main = rectangle(random.randint(0, h), 
                         random.randint(0, w), 
                         random.randint(0, h), 
                         random.randint(0, w))
        
        for y in range(main.y2):
            for x in range(main.x2):
                if not invert:
                    world[by][bx][y - main.y1][x - main.x1] = " . "
                else:
                    world[by][bx][y - main.y1][x - main.x1] = "&&&"
                            
        draw()

        invert = not invert
        i+=1
        print()


posy = int(input("Starting y:  "))
posx = int(input("Starting x:  "))
bposy = int(input("Starting by: "))
bposx = int(input("Starting bx: "))

loop = True

generate_world(0, 0)

while loop:
    draw()

    ch = str(msvcrt.getch())
    ch = (ch.replace("b'", "")).strip("'")

    old_posy = posy
    old_posx = posx

    if ch == "w":
        posy = posy - 1
    elif ch == "s":
        posy = posy + 1
    elif ch == "a":
        posx = posx - 1
    elif ch == "d":
        posx = posx + 1
    elif ch == "e":
        loop = False
    elif ch == "r":
        generate_world(bposy, bposx)
    
    if posy == h:
        bposy += 1
        generate_world(bposy, bposx)
        posy = 0
        step = 1
        while world[bposy][bposx][posy][posx] == "&&&":
            posx += step
            if posx == w:
                step = -1
                posx -= 1
            if posx == 0:
                generate_world(bposy, bposx)

    elif posy < 0:
        bposy -= 1
        generate_world(bposy, bposx)
        posy = h - 1
        step = 1
        while world[bposy][bposx][posy][posx] == "&&&":
            posx += step
            if posx == w:
                step = -1
                posx -= 1
            if posx == 0:
                generate_world(bposy, bposx)

    if posx == w:
        bposx += 1
        generate_world(bposy, bposx)
        posx = 0
        step = 1
        while world[bposy][bposx][posy][posx] == "&&&":
            posy += step
            if posy == h:
                step = -1
                posy -= 1
            if posy == 0:
                generate_world(bposy, bposx)

    elif posx < 0:
        bposx -= 1
        generate_world(bposy, bposx)
        posx = h - 1
        step = 1
        while world[bposy][bposx][posy][posx] == "&&&":
            posy += step
            if posy == w:
                step = -1
                posy -= 1
            if posy == 0:
                generate_world(bposy, bposx)

    if world[bposy][bposx][posy][posx] == "&&&":
        posy = old_posy
        posx = old_posx