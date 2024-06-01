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

class rectangle:
    def __init__(self, y1, x1, y2, x2):
        self.y1 = y1
        self.x1 = x1
        self.y2 = y2
        self.x2 = x2

#initialising the world '4D' array
world = [[[['&&&' for x in range(w)] for y in range(h)] for bx in range(bw)] for by in range(bh)]

#definition of draw function
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

valid_generated = [[False for x in range(w)] for y in range(h)]

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
        if not valid_generated[bposy][bposx]:
            generate_tile(bposy, bposx)
        posy = 0
        step = 1
        while world[bposy][bposx][posy][posx] == "&&&":
            posx += step
            if posx == w:
                step = -1
                posx -= 1
            if posx == 0:
                generate_tile(bposy, bposx)
            elif posx < 0:
                posx = 0
                step = 0
        valid_generated[bposy][bposx] = True

    elif posy < 0:
        bposy -= 1
        if not valid_generated[bposy][bposx]:
            generate_tile(bposy, bposx)
        posy = h - 1
        step = 1
        while world[bposy][bposx][posy][posx] == "&&&":
            posx += step
            if posx == w:
                step = -1
                posx -= 1
            if posx == 0:
                generate_tile(bposy, bposx)
            elif posx < 0:
                posx = 0
                step = 0
        valid_generated[bposy][bposx] = True

    if posx == w:
        bposx += 1
        if not valid_generated[bposy][bposx]:
            generate_tile(bposy, bposx)
        posx = 0
        step = 1
        while world[bposy][bposx][posy][posx] == "&&&":
            posy += step
            if posy == h:
                step = -1
                posy -= 1
            if posy == 0:
                generate_tile(bposy, bposx)
            elif posy < 0:
                posy = 0
                step = 0
        valid_generated[bposy][bposx] = True

    elif posx < 0:
        bposx -= 1
        if not valid_generated[bposy][bposx]:
            generate_tile(bposy, bposx)
        posx = h - 1
        step = 1
        while world[bposy][bposx][posy][posx] == "&&&":
            posy += step
            if posy == h:
                step = -1
                posy -= 1
            if posy == 0:
                generate_tile(bposy, bposx)
            elif posy < 0:
                posy = 0
                step = 0
        valid_generated[bposy][bposx] = True

    if world[bposy][bposx][posy][posx] == "&&&":
        posy = old_posy
        posx = old_posx