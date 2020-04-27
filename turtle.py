import string
import pygame
import sys
import os
import time
import random
import math
from pygame.locals import *
#pygame.init()

WHITE = 255, 255, 255
GREY = 64, 64, 64
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
BG_COLOUR = GREY

SCREEN_WIDTH = 1366 
SCREEN_HEIGHT = 768
TURTLE_ACTION_INTERVAL = 0 # time in ms between actions
TURTLE_PEN_COLOURS = RED, GREEN, BLUE
TURTLE_SIZE_DEFAULT = 10
TURTLE_MOVE_SPEED_DEFAULT = 1
#TURTLE_PERFORM_CURRENT_DIRECTORY = True # perform all TurtleScript files in the current (relative) directory
TURTLE_RANDOM_DIST_MAX = 10
TURTLE_CAN_OVERLAP_TRAIL = True
TURTLE_USES_FULL_COLOUR_RANGE = True
TURTLE_USES_FULL_DIRECTION_RANGE = False
TURTLE_GO_DIAGONAL = True
TURTLE_NO_TRAIL = False
TURTLE_CHECK_NEIGHBOURS = False # began to implement Conway's Game of Life but decided it was out of the scope of this project
TURTLE_NEVER_CHANGE_COLOUR = True
RENDER_STATIC = True # don't clear the screen every frame, don't fill the screen every frame, only draw when needed
RENDER_STATIC_CLEAR_INTERVAL = 1000 # MS
RENDER_STATIC_CLEAR_ON_INTERVAL = False # Clear screen on intervals to limit trail length
NORTH_ANGLE = 0
TO_RAD = 3.14 / 180.0

# ToDo:
# Give turtle more directions to travel in. Probably best to give 360 degree freedom and limit from there.
# ^DONE
# Give turtle more colours.
# ^DONE
# Better turtle grid alignment
# ^DONE
# User input for control (WASD and script-based)
# Snake game type?
# pathing (can't cross its own trail)
# use to visualise math formulas, fractals maybe
# how to take direction? as new rotation command? NESW not super diverse
# add option to not go back on itself (in random mode)
# limit trail length

# game of life. algorithm for getting number of neighbouring turtles

class Turtle:
    
    def __init__(self, path=None):
        self.path = path
        self.actions = []
        self.actionPtr = 0
        
        self.size = TURTLE_SIZE_DEFAULT
        self.moveSpeed = TURTLE_MOVE_SPEED_DEFAULT
        #self.x = random.randint(0, int(SCREEN_WIDTH / self.size) - 1) * self.size
        #self.y = random.randint(0, int(SCREEN_HEIGHT / self.size) - 1) * self.size
        if TURTLE_CHECK_NEIGHBOURS:
            self.x = random.randint(SCREEN_WIDTH // 2 - 10, SCREEN_WIDTH // 2 + 10)
            self.y = random.randint(SCREEN_HEIGHT // 2 - 10, SCREEN_HEIGHT // 2 + 10)
        else:
            self.x = random.randint(0, getHCells() - 1)
            self.y = random.randint(0, getVCells() - 1)
        self.penDown = False
        self.penPtr = 0 # pen 1 = red, pen 2 = green, pen 3 = blue
        self.rgb = TURTLE_PEN_COLOURS[self.penPtr]
        #self.memory = []
        self.target = (0, 0)
        self.hasDoneCurrentAction = False
        self.changeColourOnCollisionMode = 0 # 0 = off, 1 = when crossing same colour, 2 = when crossing any colour
        self.currentDirection = 0 # 360 deg value
        self.alive = True
        self.initColour = getRandomColour()
        self.hasStarted = False

        if self.path != None:
            self.readScript(path)
            self.performRandom = False
        else:
            self.penDown = True
            self.performRandom = True

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def setSize(self, size):
        self.size = size

    def setSpeed(self, speed):
        self.moveSpeed = speed

    def setColour(self, color):
        self.rgb = color

    def setPenPtr(self, ptr):
        self.penPtr = ptr

    def setColorRGB(self, r, g, b):
        self.rgb = r, g, b

    def getSpeed(self):
        return self.moveSpeed

    def getSize(self):
        return self.size

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getPen(self):
        return self.penPtr

    def readScript(self, path):
        with open(path, "r") as f:
            lines = list(line.strip() for line in f.readlines())
            f.close()
        for line in lines:
            if not line:
                continue
            #print(line)
            
            #parts = line.split(" ")
            parts = []

            ptr = -1
            multipleParameters = False
            parameterRead = False
            for i in range(len(line)):
                if line[i] in string.ascii_letters:
                    parts.append(line[i])

                if line[i] == "#":
                    break

                if ptr == -1:
                    try:
                        int(line[i])
                        ptr = i
                        if parameterRead:
                            multipleParameters = True
                    except ValueError:
                        pass
                else:
                    try:
                        int(line[i])
                    except ValueError:
                        # we have gone by the number part
                        parts.append(line[ptr:i])
                        ptr = -1
                        parameterRead = True
                        #break

                if i == len(line) - 1:
                    try:
                        int(line[i])
                        # last element is number
                        parts.append(line[ptr:i+1])
                        if parameterRead:
                            multipleParameters = True
                        break
                    except ValueError:
                        pass
            
            if parts:
                if multipleParameters:
                    params = tuple(int(n) for n in parts[1:])
                    parts = parts[0], params
                    
                    self.actions.append(parts)

                self.actions.append(parts)
    
    def getNeighbours(self):
        radius = 1
        num = 0

        for t in turtles:
            if t.x in tuple(range(self.x - 1, self.x + 2)) and\
                 t.y in tuple(range(self.y - 1, self.y + 2)):
                num += 1
                
                    #if t.x == x and t.y == y:
                        #num += 1
        
        return num
    
    def remember(self, data):
        exists = False

        x = data[0]
        y = data[1]
        colour = data[2]

        if RENDER_STATIC:
            if screen.get_at((x * TURTLE_SIZE_DEFAULT, y * TURTLE_SIZE_DEFAULT)) != colour:
                pygame.draw.rect(screen, colour, (x * TURTLE_SIZE_DEFAULT, y * TURTLE_SIZE_DEFAULT, TURTLE_SIZE_DEFAULT, TURTLE_SIZE_DEFAULT))
            #pygame.display.update()
            return

        cell = getCell(x, y)
        if cell != None:
            exists = True
            if cell == colour and self.changeColourOnCollisionMode == 1 or self.changeColourOnCollisionMode == 2:
                    # if the turtle is the same colour as the screen cell it occupies
                    # change the colour to something else
                    self.penPtr = random.choice(list(n for n in range(0, len(TURTLE_PEN_COLOURS)) if n != self.penPtr))
                    if TURTLE_USES_FULL_COLOUR_RANGE:
                        randColour = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                        setCell(x, y, randColour)
                    else:
                        setCell(x, y, TURTLE_PEN_COLOURS[self.penPtr])
            else:
                setCell(x, y, colour)
            #elif self.changeColourOnCollisionMode == 2:

###############
        # for i in range(len(screenBuffer)):
        #     if screenBuffer[i][0] == data[0] and screenBuffer[i][1] == data[1]:
        #         exists = True
        #         if screenBuffer[i][2] == data[2] and self.changeColourOnCollisionMode == 1:
        #             # if the turtle is the same colour as the screen cell it occupies
        #             # change the colour to something else
        #             self.penPtr = random.choice(list(n for n in range(0, len(TURTLE_PEN_COLOURS)) if n != self.penPtr))
        #             if TURTLE_USES_FULL_COLOUR_RANGE:
        #                 randColour = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        #                 setCell(x, y, randColour)
        #             else:
        #                 setCell(x, y, TURTLE_PEN_COLOURS[self.penPtr])

                # elif self.changeColourOnCollisionMode == 2:
                #     #temp = self.penPtr
                #     #while self.penPtr == temp:
                #         #self.penPtr = random.randint(0, len(TURTLE_PEN_COLOURS) - 1)
                #     self.penPtr = random.choice(list(n for n in range(0, len(TURTLE_PEN_COLOURS)) if n != self.penPtr))
                #     if TURTLE_USES_FULL_COLOUR_RANGE:
                #         screenBuffer[i][2] = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                #     else:
                #         screenBuffer[i][2] = TURTLE_PEN_COLOURS[self.penPtr]
                # else:
                #     screenBuffer[i][2] = data[2]
                # break

        if not exists:
            #screenBuffer.append(data)
            setCell(x, y, colour)

    def doNext(self):
        
        if (self.actionPtr < len(self.actions) or self.performRandom == True) or (self.alive and TURTLE_CHECK_NEIGHBOURS):
            if self.hasDoneCurrentAction == False:
                self.hasDoneCurrentAction = True
                #self.actionPtrPrev = self.actionPtr
                if self.performRandom:
                    if TURTLE_GO_DIAGONAL:
                        action = [random.choice(["P", "N", "E", "S", "W", "NE", "SE", "SW", "NW"]), None]
                    else:
                        action = [random.choice(["P", "N", "E", "S", "W"]), None]
                    if action[0] == "P":
                        if TURTLE_NEVER_CHANGE_COLOUR == False:
                            if TURTLE_USES_FULL_COLOUR_RANGE:
                                if self.hasStarted == False:
                                    action[1] = self.initColour
                                else:
                                    action[1] = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                            else:
                                action[1] = random.randint(0, len(TURTLE_PEN_COLOURS) - 1)
                        else:
                            action[1] = self.initColour
                    else:
                        action[1] = random.randint(0, TURTLE_RANDOM_DIST_MAX)
                else:
                    action = self.actions[self.actionPtr]
                #print(action)
                command = action[0]
                if len(action) > 1:
                    if isinstance(action[1], tuple):
                        value = action[1]
                    else:
                        value = int(action[1])
                #print(action)

                self.target = None
                self.direction = None
                    
                if command == "P":
                    #print(value)
                    if TURTLE_USES_FULL_COLOUR_RANGE:
                        self.rgb = value
                    else:
                        self.penPtr = value
                elif command == "D":
                    self.penDown = True
                    # need to add this point to memory because my program design is flawed :)
                    # it makes sense to "mark the paper" when the pen goes down anyway
                    if TURTLE_USES_FULL_COLOUR_RANGE:
                        self.remember([self.x, self.y, self.rgb])
                    else:
                        self.remember([self.x, self.y, TURTLE_PEN_COLOURS[self.penPtr]])
                elif command == "U":
                    self.penDown = False
                elif command == "N":
                    # turtle shouldn't have any awareness of its size
                    # but again my program design is flawed
                    #self.target = (self.x, self.y - value * self.size)
                    self.direction = NORTH_ANGLE
                elif command == "NE":
                    self.direction = NORTH_ANGLE + 45
                elif command == "E":
                    #self.target = (self.x + value * self.size, self.y)
                    self.direction = NORTH_ANGLE + 90
                elif command == "SE":
                    self.direction = NORTH_ANGLE + 135
                elif command == "S":
                    #self.target = (self.x, self.y + value * self.size)
                    self.direction = NORTH_ANGLE + 180
                elif command == "SW":
                    self.direction = NORTH_ANGLE + 225
                elif command == "W":
                    #self.target = (self.x - value * self.size, self.y)
                    self.direction = NORTH_ANGLE + 270
                elif command == "NW":
                    self.direction = NORTH_ANGLE + 315

                if self.direction != None:

                    if TURTLE_USES_FULL_DIRECTION_RANGE:
                        self.direction = random.randint(0, 359)
                    
                    x2 = self.x + (value * math.sin(self.direction * TO_RAD)) #* self.size)
                    y2 = self.y + (value * (math.cos(self.direction * TO_RAD) * -1)) #* self.size)
                    
                    #x2 = round(x2 / self.size) * self.size
                    #y2 = round(y2 / self.size) * self.size

                    x2 = round(x2)
                    y2 = round(y2)
                    
                    self.target = (x2, y2)
                    
                if self.target == None:
                    self.actionPtr += 1
                    self.hasDoneCurrentAction = False
                    self.doNext() # experiment
                                   
            else:
                # go straight to the next point if pen is up
                if self.penDown == False:
                    self.x = self.target[0]
                    self.y = self.target[1]
                else:
                    # move towards target
                    #print("hi")
                    #print(self.x, self.y, self.direction, self.target)
                    #print(self.size)
                    prevx = self.x
                    prevy = self.y
                    if abs(self.x - self.target[0]) >= abs(self.y - self.target[1]):
                        # move x
                        sign = 1 if self.target[0] > self.x else -1 # if equal?
                        diff = abs(self.x - self.target[0])
                        if diff < self.moveSpeed:
                            self.x += diff * sign
                        else:
                            self.x += self.moveSpeed * sign

                    else:
                        # move y
                        sign = 1 if self.target[1] > self.y else -1 # if equal?
                        diff = abs(self.y - self.target[1])
                        if diff < self.moveSpeed:
                            self.y += diff * sign
                        else:
                            self.y += self.moveSpeed * sign
                    
                    

                    # if [self.x, self.y] in list(cell[:2] for cell in screenBuffer) and TURTLE_CAN_OVERLAP_TRAIL == False:
                    #     #print(screenBuffer[0][:2])
                    #     self.x = prevx
                    #     self.y = prevy
                    #     self.actionPtr += 1
                    #     self.hasDoneCurrentAction = False
                    #     self.doNext()

                offScreen = False
                
                if self.x < 0:
                    self.x = 0
                    offScreen = True
                elif self.x > getHCells() - 1:
                    self.x = getHCells() - 1
                    offScreen = True

                if self.y < 0:
                    self.y = 0
                    offScreen = True
                elif self.y > getVCells() - 1:
                    self.y = getVCells() - 1
                    offScreen = True
                
                if offScreen:
                    self.actionPtr += 1
                    self.hasDoneCurrentAction = False
                    self.doNext()

                #print(self.x, self.y)

                if getCell(self.x, self.y) != None and TURTLE_CAN_OVERLAP_TRAIL == False:
                        self.x = prevx
                        self.y = prevy
                        self.actionPtr += 1
                        self.hasDoneCurrentAction = False
                        self.doNext()
                
                if TURTLE_CHECK_NEIGHBOURS:
                    if self.getNeighbours() != 3:
                        self.alive = False
                        
                if self.penDown:
                    if TURTLE_USES_FULL_COLOUR_RANGE:
                        self.remember([self.x, self.y, self.rgb])
                    else:
                        self.remember([self.x, self.y, TURTLE_PEN_COLOURS[self.penPtr]])
                    
                if (self.x, self.y) == self.target:
                    self.actionPtr += 1
                    self.hasDoneCurrentAction = False
                    self.doNext()
        elif TURTLE_CHECK_NEIGHBOURS:
            if self.getNeighbours() == 3:
                self.alive = True
        
        self.hasStarted = True
            
def getCell(x, y):
    #print((y * SCREEN_WIDTH) + x, len(screenBuffer))
    #print(getCellIndex(x, y), len(screenBuffer))
    return screenBuffer[getCellIndex(x, y)]

def setCell(x, y, colour):
    global screenBuffer
    #print((y * SCREEN_WIDTH) + x, len(screenBuffer))
    screenBuffer[getCellIndex(x, y)] = colour

def getCellIndex(x, y):
    hCells = getHCells()

    #print("raw ", x, y)
    #print("idx ", (y * (hCells)) + x)
    #print("len ", len(screenBuffer))

    return (y * (hCells)) + x

def getCellPos(i):
    y = (i // getHCells()) - 1
    x = i - (y * getHCells()) 
    #print("i", i, "x", x, "y", y)

    return x, y

def getHCells():
    return int(SCREEN_WIDTH / TURTLE_SIZE_DEFAULT)

def getVCells():
    return int(SCREEN_HEIGHT / TURTLE_SIZE_DEFAULT)

def display():
    pygameQuit = False
    timerStart = pygame.time.get_ticks()
    hasDoneInitialPause = True
    clearTimer = pygame.time.get_ticks()
    #initialDelay = 1000 # specify delay to add when program starts. before turtle starts performing actions
    #frameTime = 0

    #getCellPos(getCellIndex(100, 100))
    #input()

    #screen.flip()
    if RENDER_STATIC:
        screen.fill(BG_COLOUR)
        #screen.unlock()
        #for i in range(len(screenBuffer)):
            #pygame.draw.rect(screen, screenBuffer[i], (getCellPos(i)[0] * TURTLE_SIZE_DEFAULT, getCellPos(i)[1] * TURTLE_SIZE_DEFAULT, TURTLE_SIZE_DEFAULT, TURTLE_SIZE_DEFAULT))
        #pygame.display.flip()
        #screen.lock()
        pygame.display.update()

    while not pygameQuit:
        frameStart = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.quit()
                pygameQuit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    screen.fill(BG_COLOUR)

        if pygame.time.get_ticks() - timerStart < 15000 and hasDoneInitialPause == False:
            continue
        hasDoneInitialPause = True

        # maybe don't clear the screen to get better performance?
        if not RENDER_STATIC or (RENDER_STATIC and RENDER_STATIC_CLEAR_ON_INTERVAL and\
             (pygame.time.get_ticks() - clearTimer) > RENDER_STATIC_CLEAR_INTERVAL):
            clearTimer = pygame.time.get_ticks()
            screen.fill(BG_COLOUR)

        # logic here
        if pygame.time.get_ticks() - timerStart > TURTLE_ACTION_INTERVAL:
            timerStart = pygame.time.get_ticks()
            for t in turtles:
                t.doNext()

        #for t in turtles:
        if not RENDER_STATIC:
            if TURTLE_NO_TRAIL == False:
                for y in range(getVCells()):
                    for x in range(getHCells()):
                        if getCell(x, y) != None:
                            pygame.draw.rect(screen, getCell(x, y), (x * TURTLE_SIZE_DEFAULT, y * TURTLE_SIZE_DEFAULT, TURTLE_SIZE_DEFAULT, TURTLE_SIZE_DEFAULT))
            else:
                for t in turtles:
                    if t.alive == True:
                        pygame.draw.rect(screen, t.rgb, (t.x * TURTLE_SIZE_DEFAULT, t.y * TURTLE_SIZE_DEFAULT, TURTLE_SIZE_DEFAULT, TURTLE_SIZE_DEFAULT))

        #for element in screenBuffer:
            #pygame.draw.rect(screen, element[2], (element[0], element[1], TURTLE_SIZE_DEFAULT, TURTLE_SIZE_DEFAULT))
            #pygame.draw.circle(screen, TURTLE_PEN_COLOURS[element[2]], (element[0], element[1]), TURTLE_SIZE_DEFAULT)

        #if not RENDER_STATIC:
        pygame.display.update()

        clock.tick(frameRate)
        frameEnd = pygame.time.get_ticks()
        frameTime = frameEnd - frameStart
        if frameTime == 0:
            frameTime = 1
        pygame.display.set_caption("FrameTime: " + str(frameTime) + " FPS: " + str(int(1000 / frameTime)))


    pygame.quit()
    #sys.exit()
    #screen.quit()
    #screen.close()

def getRandomColour():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def _generateTurtleScriptFile(numActions):
    fileName = "gen" + str(int(time.time())) + ".tsf"
    with open(fileName, "w") as f:
        f.write("D\n")
        f.write("P 0\n")
        for i in range(numActions):
            command = random.choice(["N", "E", "S", "W", "P"])
            if command == "P":
                if TURTLE_USES_FULL_COLOUR_RANGE:
                    value = getRandomColour()
                else:
                    value = random.randint(0, len(TURTLE_PEN_COLOURS) - 1)
            else:
                value = random.randint(0, TURTLE_RANDOM_DIST_MAX)
            if isinstance(value, tuple):
                f.write(command + " " + " ".join(str(n) for n in value) + "\n")
                #print(" ".join(str(n) for n in value))
            else:
                f.write(command + " " + str(value) + "\n")
        f.close()
    return fileName

def waitForValidIntInput(msg, error="error: please enter a number", forcePositive=False):
    inp = None
    while inp == None:
        try:
            inp = int(input(msg))
            if forcePositive and inp <= 0:
                raise Exception(ValueError)
        except ValueError:
            print(error)
    return inp

def waitForValidFileName():
    inp = None
    while inp == None:
        try:
            inp = input("Enter a file name: ")
            if not os.path.exists(inp):
                raise Exception(FileNotFoundError)
        except FileNotFoundError:
            print("error: that file does not exist in the current directory")
    return inp

def clearScreenBuffer():
    global screenBuffer
    screenBuffer = []

    hCells = getHCells() # maybe math.floor() ?
    vCells = getVCells()
    print("setting", hCells * vCells, "cells")

    for i in range(hCells * vCells):
        if not RENDER_STATIC:
            screenBuffer.append(None)
        else:
            screenBuffer.append(BG_COLOUR)


flags = HWSURFACE | DOUBLEBUF | FULLSCREEN
bpp = 16

clock = pygame.time.Clock()
frameRate = 999

turtles = []
screenBuffer = []

clearScreenBuffer()

options = [
    ("Perform a specific TurtleScript file", "readone"),
    ("Perform all TurtleScript files in the current directory (simultaneously)", "readall"),
    ("Generate a random TurtleScript file", "genrand"),
    ("Endless random turtle", "endless"),
    ("Set frame-rate", "setfps"),
    ("Set turtle size", "setsize"),
    ("Set turtle speed", "setspeed"),
    ("Quit", "quit")
]

screen = None
choice = None
quitGame = False
start = False
print("Welcome to TurtleScript Drawing Program!")
print("\nWhat would you like to do?")
for i in range(len(options)):
    print(i+1, ")", options[i][0])

while not quitGame:
    start = True
    choice = waitForValidIntInput("Choose an option: ")
        
    if choice != None and choice in list(range(1, len(options) + 1)):
        optId = options[choice-1][1]
        if optId == "readone":
            print("\nAvailable TurtleScript files:")
            for fileName in os.listdir(os.path.abspath("")):
                if fileName.endswith(".tsf"):
                    print(fileName)
            fileName = None
            while fileName == None:
                fileName = input("File name: ")
                if not os.path.exists(fileName):
                    print("error: that file does not exist")
                    fileName = None
                else:
                    turtles.append(Turtle(fileName))

        elif optId == "readall":
            fileNames = os.listdir(os.path.abspath(""))
            for fileName in fileNames:
                if fileName.endswith(".tsf"): 
                    turtles.append(Turtle(fileName))

        elif optId == "genrand":
            numActions = waitForValidIntInput("How many actions?: ")
            if numActions <= 0:
                print("error: please enter a positive number")
            else:
                genFile = _generateTurtleScriptFile(numActions)
                turtles = [Turtle(genFile),]

        elif optId == "endless":
            #turtles = [Turtle(), ]
            turtles = []
            
            numTurtles = waitForValidIntInput("Number of turtles: ", forcePositive=True)

            for i in range(numTurtles):
                turtles.append(Turtle())

            changeColourOnCollision = None
            while changeColourOnCollision == None:
                changeColourOnCollision = input("Would you like the turtle to change colour when passing over its trail? [Y/n]: ")
                if changeColourOnCollision.lower() not in ("y", "n"):
                    print("error: please type 'y' or 'n'")
                    changeColourOnCollision = None
            if changeColourOnCollision.lower() == "y":
                #turtles[0].changeColourOnCollisionMode = 0
                mode = None
                while mode == None:
                    mode = waitForValidIntInput("Mode? [1: same colour] or [2: any colour]: ")
                    if mode not in (1, 2):
                        print("error: not an option")
                        mode = None
                    else:
                        #turtles = []
                        for i in range(numTurtles):
                            #turtles.append(Turtle())
                            turtles[i].changeColourOnCollisionMode = mode
                        #turtles[0].changeColourOnCollisionMode = mode

        elif optId == "setfps":
            # set fps
            frameRate = waitForValidIntInput("Frame-rate: ", forcePositive=True)
            start = False
        elif optId == "setsize":
            # set size
            TURTLE_SIZE_DEFAULT = waitForValidIntInput("Turtle size: ", forcePositive=True)
            #TURTLE_MOVE_SPEED_DEFAULT = TURTLE_SIZE_DEFAULT
            start = False
        elif optId == "setspeed":
            TURTLE_MOVE_SPEED_DEFAULT = waitForValidIntInput("Turtle speed: ", forcePositive=True)
            start = False
        elif optId == "quit":
            pygame.quit()
            #sys.exit()
            quitGame = True
    
    if not quitGame and start == True:
        pygame.init()
        pygame.display.set_caption("TurtleScript Drawing Program")
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, bpp)
        
        clearScreenBuffer()

        display()