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
    def __init__(self, by: int, bx: int, y: int, x: int, c: str, 
                 type: str, items: Dict[str, item], equipped: str,
                 max_health: int, health: int, armor: int, demagable: bool):
        self.by = by
        self.bx = bx
        self.y = y
        self.x = x
        self.c = c
        self.type = type
        self.items = items
        self.equipped = equipped
        self.max_health = max_health
        self.health = health
        self.armor = armor
        self.demagable = demagable


#test sprites of type 'monster' initialization
#monster0 = sprite(0, 0, 1, 1, ":-)", "monster")
monster1 = sprite(0, 0, 0, 0, ":-(", "monster", {'': None}, None, 60, 60, 0, True)

wall1 = sprite(0, 0, 3, 3, "-&-", "wall_tool", {'': None}, None, 0, 0, 0, False)
sword1 = sprite(0, 0, 2, 2, "--L", "wooden_sword", {'': None}, None, 0, 0, 0, False)
player = sprite(0, 0, 0, 0, " @ ", "player", {'': None}, None, 100, 100, 0, True)

item_table = {"wall_tool": "-&-",
              "wooden_sword": "--L"}

#dictionary to hold the information of all sprites, can add new sprites dynamically
sprites = {}
sprites["wall_tool"] = wall1
sprites["wooden_sword"] = sword1
sprites["player"] = player
#sprites["smiley"] = monster0
sprites["grumpy"] = monster1


keys_to_remove = []
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
        
        elif name.type == "wall_tool":
            if bposy == name.by and bposx == name.bx and posy == name.y and posx == name.x:
                if input("Pick up wall placing tool? (1/0) ") == "1":
                    sword = item(False, "wall_tool", "wall_tool")
                    sprites["player"].items.update({"wall_tool": sword})
                    keys_to_remove.append(key)

        elif name.type == "wooden_sword":
            if bposy == name.by and bposx == name.bx and posy == name.y and posx == name.x:
                if input("Pick up sword? (1/0) ") == "1":
                    sword = item(False, "wooden_sword", "wooden_sword")
                    sprites["player"].items.update({"wooden_sword": sword})
                    keys_to_remove.append(key)
                    
    for key in keys_to_remove:
        del sprites[key]


def demage_target(name: str, dmg: int, arm: int):
    target = sprites[name]
    target.armor -= arm
    target.health -= dmg
    if target.armor < 0:
        target.armor = 0
    if target.health <= 0:
        keys_to_remove.append(name)
    print("You hit " + name + "!")

def use_item(actor: str):
    keys_to_remove = []
    if sprites[actor].equipped == "wall_tool":
        world[bposy][bposx][posy][posx] = "&&&"
    
    if sprites[actor].equipped == "wooden_sword":
        ch = str(msvcrt.getch())
        ch = (ch.replace("b'", "")).strip("'")

        if ch == "w":
            for key in sprites:
                target = sprites[key]
                if target.by == bposy and target.bx == bposx and target.y == posy - 1 and target.x == posx:
                    demage_target(key, 12, 1)

        if ch == "s":
            for key in sprites:
                target = sprites[key]
                if target.by == bposy and target.bx == bposx and target.y == posy + 1 and target.x == posx:
                    demage_target(key, 12, 1)

        if ch == "a":
            for key in sprites:
                target = sprites[key]
                if target.by == bposy and target.bx == bposx and target.y == posy and target.x == posx - 1:
                    demage_target(key, 12, 1)
        
        if ch == "d":
            for key in sprites:
                target = sprites[key]
                if target.by == bposy and target.bx == bposx and target.y == posy and target.x == posx + 1:
                    demage_target(key, 12, 1)

        for key in keys_to_remove:
            del sprites[key]


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
    sprites[i] = sprite(sp.by, sp.bx, sp.y, sp.x, item_table[i], 
                        sp.items[i].type, {'' :None}, None, 0, 0, 0, False)
    if sp.equipped == i:
        del sp.items[sp.equipped]
        sp.equipped = ""

#initialising the world '4D' array
world = [[[['&&&' for x in range(w)] for y in range(h)] for bx in range(bw)] for by in range(bh)]


#definition of draw function
def draw():
    clear()
    print(f"bposy: {bposy}, bposx: {bposx}, posy: {posy}, posx: {posx}")
    for key in sprites["player"].items:
        if sprites["player"].equipped == key:
            print("*", end='')
        print(key, end=' ')
    print(sprites["grumpy"].health)

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

#definition of list index out of range checker of position correction
def update_illegal():
    if bposy < 0 or bposy == bh:
        bposy = old_bposy
    if bposx < 0 or bposx == bw:
        bposx = old_bposx

loop = True

#pre-generate world
for by in range(bh):
    for bx in range(bw):
        generate_tile(by, bx)

#main uptade loop
while loop:
        
    draw()

    #get key input, will need a cross-platform solution
    ch = str(msvcrt.getch())
    ch = (ch.replace("b'", "")).strip("'")

    #needed for position correction in wall collision
    old_posy = posy
    old_posx = posx
    old_bposy = bposy
    old_bposx = bposx

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
        if bposy == bh:
            bposy = old_bposy
            posy = h - 1
        else:
            posy = 0
        if world[bposy][bposx][posy][posx] == "&&&":
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
        if bposy < 0:
            bposy = old_bposy
            posy = 0
        else:
            posy = h - 1
        step = 1
        if world[bposy][bposx][posy][posx] == "&&&":
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
        if bposx == bw:
            bposx = old_bposx
            posx = w - 1
        else:
            posx = 0
        step = 1
        if world[bposy][bposx][posy][posx] == "&&&":
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
        if bposx < 0:
            bposx = old_bposx
            posx = 0
        else:
            posx = w - 1
        step = 1
        if world[bposy][bposx][posy][posx] == "&&&":
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