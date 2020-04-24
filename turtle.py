import string, pygame, sys, os, time, random
from pygame.locals import *
pygame.init()

WHITE = 255, 255, 255
GREY = 64, 64, 64
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
BG_COLOUR = GREY

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TURTLE_ACTION_INTERVAL = 0 # time in ms between actions
TURTLE_PEN_COLOURS = RED, GREEN, BLUE
TURTLE_SIZE_DEFAULT = 20
TURTLE_MOVE_SPEED_DEFAULT = TURTLE_SIZE_DEFAULT
TURTLE_PERFORM_CURRENT_DIRECTORY = True # perform all TurtleScript files in the current (relative) directory
TURTLE_RANDOM_DIST_MAX = 10

class Turtle:
    
    def __init__(self, path=None, pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), size=TURTLE_SIZE_DEFAULT, speed=TURTLE_MOVE_SPEED_DEFAULT):
        self.path = path
        self.actions = []
        self.actionPtr = 0
        self.x = pos[0]
        self.y = pos[1]
        self.size = size
        self.moveSpeed = speed
        self.penDown = False
        self.penPtr = 0 # pen 1 = red, pen 2 = green, pen 3 = blue
        #self.memory = []
        self.target = (0, 0)
        self.hasDoneCurrentAction = False

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
            for i in range(len(line)):
                if line[i] in string.ascii_letters:
                    parts.append(line[i])

                if line[i] == "#":
                    break

                if ptr == -1:
                    try:
                        int(line[i])
                        ptr = i
                    except ValueError:
                        pass
                else:
                    try:
                        int(line[i])
                    except ValueError:
                        # we have gone by the number part
                        parts.append(line[ptr:i])
                        break

                if i == len(line) - 1:
                    try:
                        int(line[i])
                        # last element is number
                        parts.append(line[ptr:i+1])
                        break
                    except ValueError:
                        pass
                
            self.actions.append(parts)
        #print(self.actions)
        #input()
    
    def remember(self, data):
        exists = False

        for i in range(len(screenBuffer)):
            if screenBuffer[i][0] == data[0] and screenBuffer[i][1] == data[1]:
                exists = True
                if screenBuffer[i][2] == data[2]:
                    # if the turtle is the same colour as the screen cell it occupies
                    # change the colour to something else
                    # (this way we don't lose track of where the turtle is)
                    temp = self.penPtr
                    while self.penPtr == temp:
                        self.penPtr = random.randint(0, len(TURTLE_PEN_COLOURS) - 1)
                    screenBuffer[i][2] = self.penPtr
                else:
                    screenBuffer[i][2] = data[2]
                break

        if not exists:
            screenBuffer.append(data)

    def doNext(self):
        
        if self.actionPtr < len(self.actions) or self.performRandom == True:
            if self.hasDoneCurrentAction == False:
                self.hasDoneCurrentAction = True
                #self.actionPtrPrev = self.actionPtr
                if self.performRandom:
                    action = [random.choice(["P", "N", "E", "S", "W"]), None]
                    if action[0] == "P":
                        action[1] = random.randint(0, len(TURTLE_PEN_COLOURS) - 1)
                    else:
                        action[1] = random.randint(0, TURTLE_RANDOM_DIST_MAX)
                else:
                    action = self.actions[self.actionPtr]
                command = action[0]
                if len(action) > 1:
                    value = int(action[1])
                #print(action)

                self.target = None
                    
                if command == "P":
                    self.penPtr = value
                elif command == "D":
                    self.penDown = True
                    # need to add this point to memory because my program design is flawed :)
                    # it makes sense to "mark the paper" when the pen goes down anyway
                    self.remember([self.x, self.y, self.penPtr])
                elif command == "U":
                    self.penDown = False
                elif command == "N":
                    # turtle shouldn't have any awareness of its size
                    # but again my program design is flawed
                    self.target = (self.x, self.y - value * self.size)
                elif command == "E":
                    self.target = (self.x + value * self.size, self.y)
                elif command == "S":
                    self.target = (self.x, self.y + value * self.size)
                elif command == "W":
                    self.target = (self.x - value * self.size, self.y)

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
                    if abs(self.x - self.target[0]) >= abs(self.y - self.target[1]):
                        # move x
                        if self.target[0] > self.x:
                            self.x += 1 * self.moveSpeed
                        elif self.target[0] < self.x:
                            self.x -= 1 * self.moveSpeed
                    else:
                        # move y
                        if self.target[1] > self.y:
                            self.y += 1 * self.moveSpeed
                        elif self.target[1] < self.y:
                            self.y -= 1 * self.moveSpeed

                offScreen = False
                if self.x < 0:
                    self.x = 0
                    offScreen = True
                elif self.x > SCREEN_WIDTH - self.size:
                    self.x = SCREEN_WIDTH - self.size
                    offScreen = True

                if self.y < 0:
                    self.y = 0
                    offScreen = True
                elif self.y > SCREEN_HEIGHT - self.size:
                    self.y = SCREEN_HEIGHT - self.size
                    offScreen = True
                
                if offScreen:
                    self.actionPtr += 1
                    self.hasDoneCurrentAction = False
                    self.doNext()

                #print(self.x, self.y)
                        
                if self.penDown:
                    self.remember([self.x, self.y, self.penPtr])
                    
                if (self.x, self.y) == self.target:
                    self.actionPtr += 1
                    self.hasDoneCurrentAction = False
                    self.doNext()
            

def display():
    FPS = 24
    pygameQuit = False
    timerStart = pygame.time.get_ticks()
    hasDoneInitialPause = False
    #initialDelay = 1000 # specify delay to add when program starts. before turtle starts performing actions
    
    while not pygameQuit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.quit()
                pygameQuit = True

        if pygame.time.get_ticks() - timerStart < 15000 and hasDoneInitialPause == False:
            continue
        hasDoneInitialPause = True

        screen.fill(BG_COLOUR)

        # logic here
        if pygame.time.get_ticks() - timerStart > TURTLE_ACTION_INTERVAL:
            timerStart = pygame.time.get_ticks()
            for t in turtles:
                t.doNext()

        #for t in turtles:
        for element in screenBuffer:
            pygame.draw.rect(screen, TURTLE_PEN_COLOURS[element[2]], (element[0], element[1], TURTLE_SIZE_DEFAULT, TURTLE_SIZE_DEFAULT))

        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()

def _generateTurtleScriptFile(numActions):
    fileName = "gen" + str(int(time.time())) + ".tsf"
    with open(fileName, "w") as f:
        f.write("D\n")
        f.write("P 0\n")
        for i in range(numActions):
            command = random.choice(["N", "E", "S", "W", "P"])
            if command == "P":
                value = random.randint(0, len(TURTLE_PEN_COLOURS) - 1)
            else:
                value = random.randint(0, TURTLE_RANDOM_DIST_MAX)
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

pygame.display.set_caption("TurtleScript Drawing Program")

flags = HWSURFACE | DOUBLEBUF
bpp = 16

clock = pygame.time.Clock()

turtles = []
screenBuffer = []
options = [
    "Perform a specific TurtleScript file",
    "Perform all TurtleScript files in the current directory (simultaneously)",
    "Generate a random TurtleScript file",
    "Endless random Turtle"
]

choice = None
print("Welcome to TurtleScript Drawing Program!")
print("\nWhat would you like to do?")
for i in range(len(options)):
    print(i+1, ")", options[i])

while choice == None:
    choice = waitForValidIntInput("Choose an option: ")
        
    if choice != None and choice in list(range(1, len(options) + 1)):
        if choice == 1:
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
        elif choice == 2:
            fileNames = os.listdir(os.path.abspath(""))
            for fileName in fileNames:
                if fileName.endswith(".tsf"): 
                    turtles.append(Turtle(fileName))
        elif choice == 3:
            numActions = waitForValidIntInput("How many actions?: ")
            if numActions <= 0:
                print("error: please enter a positive number")
            else:
                genFile = _generateTurtleScriptFile(numActions)
                turtles = [Turtle(genFile),]
        elif choice == 4:
            turtles = [Turtle(), ]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, bpp)

display()