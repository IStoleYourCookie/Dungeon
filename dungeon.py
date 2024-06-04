import msvcrt
import random
from os import system, name
from typing import Dict

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
    def __init__(self, y1: int, x1: int, y2: int, x2: int):
        self.y1 = y1
        self.x1 = x1
        self.y2 = y2
        self.x2 = x2

class item:
    def __init__(self, equipped: bool, type: str, name: str):
        self.equipped = equipped
        self.type = type
        self.name = name

#sprite class definition
class sprite:
    def __init__(self, by: int, bx: int, y: int, x: int, c: str, type: str, items: Dict[str, item], equipped: str):
        self.by = by
        self.bx = bx
        self.y = y
        self.x = x
        self.c = c
        self.type = type
        self.items = items
        self.equipped = equipped


#test sprites of type 'monster' initialization
#monster0 = sprite(0, 0, 1, 1, ":-)", "monster")
#monster1 = sprite(0, 0, 2, 2, ":-(", "monster")

sword1 = sprite(0, 0, 3, 3, "--L", "wooden_sword", {'': None}, None)
player = sprite(0, 0, 0, 0, " @ ", "player", {'': None}, None)

item_table = {"wooden_sword": "--L"}

#dictionary to hold the information of all sprites, can add new sprites dynamically
sprites = {}
sprites["wooden_sword1"] = sword1
sprites["player"] = player
#sprites["smiley"] = monster0
#sprites["grumpy"] = monster1

#defining the behaviour of type 'monster' sprites
def update_sprites():
    keys_to_remove = []
    for key in sprites:
        name = sprites[key]
        if name.type == "monster":
            oy = name.y
            ox = name.x
            if oy > posy:
                name.y += random.randint(-1, 0)
            else:
                name.y += random.randint(0, 1)
            if ox > posx:
                name.x += random.randint(-1, 0)
            else:
                name.x += random.randint(0, 1)

            if name.x == w or name.x == -1 or name.y == h or name.y == -1 or world[name.by][name.bx][name.y][name.x] == "&&&":
                name.y = oy
                name.x = ox
        
        elif name.type == "wooden_sword":
            if bposy == name.by and bposx == name.bx and posy == name.y and posx == name.x:
                if input("Pick up sword? (1/0) ") == "1":
                    sword = item(False, "wooden_sword", "wooden_sword")
                    sprites["player"].items.update({"wooden_sword": sword})
                    keys_to_remove.append("wooden_sword1")
    for key in keys_to_remove:
        del sprites[key]


def use_item(actor: str):
    if sprites[actor].equipped == "wooden_sword":
        world[bposy][bposx][posy][posx] = "&&&"

def equip_item(actor: str):
    i = input("Name of item to equip: ")
    sprites[actor].equipped = i

def discard_item(actor: str):
    if actor == "player":
        if input("Are you sure you want to discard item? (1/0) ") == "1":
            #(you can only discard items that are equipped)
            del sprites["player"].items[sprites["player"].equipped]
            sprites[actor].equipped = ""
    del sprites[actor].items[sprites[actor].equipped]
    sprites[actor].equipped = ""

def drop_item(actor: str):
    sp = sprites[actor]
    i = input("Item to drop from inventory: ")
    if sp.equipped == i:
        del sp.items[sp.equipped]
        sp.equipped = ""
    sprites[i] = sprite(sp.by, sp.bx, sp.y, sp.x, item_table[i], sprites[sp.items[i]], {'' :None}, None)


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
            for i in sprites:
                name = sprites[i]
                if name.y == y and name.x == x and name.by == bposy and name.bx == bposx and name.type != "player":
                    char = name.c
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

    #making inventory an ordinary array, so index can be easily changed to cycle between items to equip
    """
    inventory = [item(False, "")]*len(sprites["player"].items)
    i = 0
    for key in sprites["player"].items:
        if i < len(inventory):
            inventory[i] = sprites["player"].items[key]
        i += 1
    """
        
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
    elif ch == "o":
        loop = False
    elif ch == "r":
        generate_tile(bposy, bposx)
    elif ch == "f":
        use_item("player")
    elif ch == "e":
        equip_item("player")
    elif ch == "q":
        discard_item("player")
    elif ch == "v":
        drop_item("player")


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
                posy = h - 1
                bposy -= 1
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
                posy = 0
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
                bposx -= 1
                posx = w - 1
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
                posx = 0
                break
            elif posy < 0:
                posy = 0
                step = 0

    if world[bposy][bposx][posy][posx] == "&&&":
        posy = old_posy
        posx = old_posx

    sprites["player"].by = bposy
    sprites["player"].bx = bposx
    sprites["player"].y = posy
    sprites["player"].x = posx
    #updating the monsters
    update_sprites()