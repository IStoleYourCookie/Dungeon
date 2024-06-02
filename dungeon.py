import msvcrt
import random
from os import system, name

#cross-platform clear function definition
def clear():
    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')


#world size and generation deepness
w = int(input("Tile width:  "))
h = int(input("Tile height: "))
bw = int(input("World width in tiles:  "))
bh = int(input("World height in tiles: "))
n = int(input("Deepness:    "))

#rectangle class definition
class rectangle:
    def __init__(self, y1, x1, y2, x2):
        self.y1 = y1
        self.x1 = x1
        self.y2 = y2
        self.x2 = x2

#sprite class definition
class sprite:
    def __init__(self, by, bx, y, x, c):
        self.by = by
        self.bx = bx
        self.y = y
        self.x = x
        self.c = c

#test sprites of 'type' 'monster' initialization
monster0 = sprite(0, 0, 1, 1, ":-)")
monster1 = sprite(0, 0, 2, 2, ":-(")

#defining the behaviour of monster 'type' sprites
def update_monster(name: sprite):
    oy = name.y
    ox = name.x
    name.y += random.randint(-1, 1)
    name.x += random.randint(-1, 1)
    if name.x == w or name.x == -1 or name.y == h or name.y == -1 or world[name.by][name.bx][name.y][name.x] == "&&&":
        name.y = oy
        name.x = ox

#array to hold the information of all sprites, to add new sprites dynamically, use 'append'
sprites = [None]
sprites[0] = monster0
sprites.append(monster1)

#initialising the world '4D' array
world = [[[['&&&' for x in range(w)] for y in range(h)] for bx in range(bw)] for by in range(bh)]

#definition of draw function
def draw():
    clear()
    print(f"bposy: {bposy}, bposx: {bposx}, posy: {posy}, posx: {posx}")
    for y in range(h):
        for x in range(w):
            if y == posy and x == posx:
                char = " @ "
            else:
                char = world[bposy][bposx][y][x]
            for i in range(len(sprites)):
                if sprites[i].y == y and sprites[i].x == x:
                    char = sprites[i].c
            print(char, end=" ")
        print()
    print()

#definition of tile generating function
def generate_tile(by, bx):
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

#starting position

posy = int(input("Starting y:  "))
posx = int(input("Starting x:  "))
bposy = int(input("Starting by: "))
bposx = int(input("Starting bx: "))

loop = True

#pre-generate world
for by in range(bh):
    for bx in range(bw):
        generate_tile(by, bx)

#main uptade loop
while loop:
    draw()

    #for debugging
    """
    for by in range(bh):
        for bx in range(bw):
            print(world[by][bx])
    """

    #get key input, will need a cross-platform solution
    ch = str(msvcrt.getch())
    ch = (ch.replace("b'", "")).strip("'")

    #needed for position correction in wall collision
    old_posy = posy
    old_posx = posx

    #handling input, updating position
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
        generate_tile(bposy, bposx)
    
    #paging logic for legal repositioning and regeneration of the tile, if no legal positions
    if posy == h:
        bposy += 1
        posy = 0
        step = 1
        while world[bposy][bposx][posy][posx] == "&&&":
            posx += step
            if posx == w:
                step = -1
                posx -= 1
            if posx == 0:
                posx = old_posx
                bposy += 1
                break
            elif posx < 0:
                posx = 0
                step = 0

    elif posy < 0:
        bposy -= 1
        posy = h - 1
        step = 1
        while world[bposy][bposx][posy][posx] == "&&&":
            posx += step
            if posx == w:
                step = -1
                posx -= 1
            if posx == 0:
                posx = old_posx
                bposy += 1
                break
            elif posx < 0:
                posx = 0
                step = 0

    if posx == w:
        bposx += 1
        posx = 0
        step = 1
        while world[bposy][bposx][posy][posx] == "&&&":
            posy += step
            if posy == h:
                step = -1
                posy -= 1
            if posy == 0:
                posy = old_posy
                bposx += 1
                break
            elif posy < 0:
                posy = 0
                step = 0

    elif posx < 0:
        bposx -= 1
        posx = h - 1
        step = 1
        while world[bposy][bposx][posy][posx] == "&&&":
            posy += step
            if posy == h:
                step = -1
                posy -= 1
            if posy == 0:
                posy = old_posy
                bposx += 1
                break
            elif posy < 0:
                posy = 0
                step = 0

    if world[bposy][bposx][posy][posx] == "&&&":
        posy = old_posy
        posx = old_posx

    update_monster(monster0)
    update_monster(monster1)