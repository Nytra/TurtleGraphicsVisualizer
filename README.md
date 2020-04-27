# TurtleScript - A turtle graphics visualizer
A parser and renderer that reads TurtleScript commands from a TurtleScript file (.tsf) and then performs the specified actions on screen. Also has modes that don't read from a file. Requires PyGame.

![Insanity](https://github.com/Nytra/TurtleScript/blob/master/assets/demo3.gif)

Massively optimized rendering to support 1000 unique turtles moving on the screen at once!

![demo5](https://github.com/Nytra/TurtleGraphicsVisualizer/blob/master/assets/demo5.gif)

![demo6](https://github.com/Nytra/TurtleGraphicsVisualizer/blob/master/assets/demo6.gif)

![demo4](https://github.com/Nytra/TurtleGraphicsVisualizer/blob/master/assets/demo4.gif)

![Random TurtleScript](https://github.com/Nytra/TurtleScript/blob/master/assets/random.png)

The program is capable of generating random TurtleScript files with a specified number of actions. The program ensures that the turtle does not leave the confines of the screen.

![Random TurtleScript](https://github.com/Nytra/TurtleScript/blob/master/assets/demo2.gif)

Endless random mode!

![demo](https://github.com/Nytra/TurtleScript/blob/master/assets/demo1.gif)

Just a demonstration of a turtle drawing my name onto the screen.

![demo](https://github.com/Nytra/TurtleScript/blob/master/assets/yeah_comments.png)

The TurtleScript code for the above drawing.

---

## Intro

TurtleScript is a name that I just made up for a scripting language meant for controlling turtles (little nasties that algorithmically make a mess on the screen).

The idea for this program came from a book called "The Pragmatic Programmer" by Andrew Hunt and David Thomas (page 63 exercise 5)

The exercise just states that you must implement a *parser* for the scripting language- but, of course, I couldn't just stop there. 

This program supports ~~3 colours~~ FULL COLOUR RANGE, navigation in ~~4~~ FULL 360 DEGREES ~~directions~~, and pen up/down commands. You could draw anything from your wildest imagination.

---

## Using TurtleScript

Place your TurtleScript files in the same directory as the main program. Upon execution, the program will ask you to input the name of a TurtleScript file. Once you have done so, the program will begin drawing your beautiful artistic masterpiece on the very screen before your eyes :D

There are also other modes to choose from, such as:
- Perform all TurtleScript files in the current directory simultaneously
- Save a new finite and random TurtleScript file (of user-specified length) in the current directory and then perform it
- Endless random mode!

### Key Bindings

`P` : Clear the screen

### Syntax:

Most TurtleScript commands come in the form of an uppercase letter, followed by a space, followed by a number.

Example: `"N 12"`

Some commands do not take an argument, so for them you would just type the uppercase letter.

Example: `"D"`

The parser supports comments, but only at the end of the line.

Example: `"N 4 # this is a comment"`

The `"P"` command sets the colour, and takes RGB values in this form: `"P 255 255 255"`

The following TurtleScript code will draw a hollow square on screen.

```
# start of file
P 255 0 0    # select red pen
D      # pen down
W 5    # go west (left) 5 positions
N 5    # go north (up) 5 positions
E 5    # go east (right) 5 positions
S 5    # go south (down) 5 positions
U      # pen up
# end of file
```
