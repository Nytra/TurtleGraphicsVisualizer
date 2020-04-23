import string, pygame, sys
from pygame.locals import *
pygame.init()

class TurtleScript:
    
    def __init__(self, path):
        self.path = path
        self.actions = []
        self.actionPtr = 0
        self.x = 0
        self.y = 0
        self.size = 1
        self.penDown = False
        self.penPtr = 0 # pen 1 = red, pen 2 = green, pen 3 = blue
        self.memory = []
        self.target = (0, 0)
        #self.readNext = True
        self.actionPtrPrev = -1

        self.readScript(path)

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def setSize(self, size):
        self.size = size

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

    def doNext(self):
        
        if self.actionPtr < len(self.actions):
            if self.actionPtrPrev != self.actionPtr:
                #readNext = False
                self.actionPtrPrev = self.actionPtr
                action = self.actions[self.actionPtr]
                command = action[0]
                if len(action) > 1:
                    value = int(action[1])
                print(action)

                self.target = None
                    
                if command == "P":
                    self.penPtr = value
                elif command == "D":
                    self.penDown = True
                    # need to add this point to memory because my program design is flawed :)
                    # it makes sense to "mark the paper" when the pen goes down anyway
                    self.memory.append((self.x, self.y, self.penPtr))
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
                    #self.readNext = True
                                   
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
                            self.x += 1 * self.size
                        elif self.target[0] < self.x:
                            self.x -= 1 * self.size
                    else:
                        # move y
                        if self.target[1] > self.y:
                            self.y += 1 * self.size
                        elif self.target[1] < self.y:
                            self.y -= 1 * self.size

                #print(self.x, self.y)
                        
                if self.penDown:
                    self.memory.append((self.x, self.y, self.penPtr))
                    
                if (self.x, self.y) == self.target:
                    #self.readNext = True
                    self.actionPtr += 1
            

def display():
    FPS = 60
    t.setPos(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    t.setSize(TURTLE_SIZE)
    pygameQuit = False
    timerStart = pygame.time.get_ticks()
    initialDelay = 1000 # specify delay to add when program starts. before turtle starts performing actions
    
    while not pygameQuit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(bgColour)

        # logic here
        if initialDelay != None and pygame.time.get_ticks() - timerStart < initialDelay:
            pass
        else:
            initialDelay = None
            if pygame.time.get_ticks() - timerStart > TURTLE_ACTION_INTERVAL:
                timerStart = pygame.time.get_ticks()
                t.doNext()

        for element in t.memory:
            pygame.draw.rect(screen, TURTLE_PEN_COLOURS[element[2]], (element[0], element[1], TURTLE_SIZE, TURTLE_SIZE))
        
        pygame.display.update()

        clock.tick(FPS)


white = 255, 255, 255
grey = 64, 64, 64
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
bgColour = grey

pygame.display.set_caption("TurtleScript Drawing Program")

flags = HWSURFACE | DOUBLEBUF
bpp = 16
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TURTLE_ACTION_INTERVAL = 100 # time in ms between actions
TURTLE_PEN_COLOURS = red, green, blue
TURTLE_SIZE = 20

clock = pygame.time.Clock()

fileName = input("File name: ")
t = TurtleScript(fileName)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, bpp)

display()
#t.perform()
