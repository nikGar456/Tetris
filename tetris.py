# Tetris code
# Original source: tynker.com
# Modified: Nikolay Z
# Date: 03/04/2021

import turtle
import random

"""Setup screen first"""
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("TETRIS by Nikolay")
screen.setup(width=600, height=800)
screen.tracer(0)
screen.delay(0)

"""
Shapes Information
blocks: stores color and offset information for each letter
shapes: stores shape information for each letter 
"""
blocks = {'j': ("blue", [(0, 0), (-20, -20), (-20, 0), (20, 0)]),
          'o': ("red", [(0, 0), (0, -20), (-20, -20), (-20, 0)]),
          'z': ("green", [(0, 0), (0, -20), (-20, 0), (-20, 20)]),
          'l': ("yellow", [(0, 0), (20, 0), (-20, 0), (-20, 20)]),
          'i': ("brown", [(0, 0), (-20, 0), (20, 0), (40, 0)]),
          's': ("violet", [(0, 0), (0, 20), (-20, 0), (-20, -20)]),
          't': ("purple", [(0, 0), (20, 0), (0, -20), (0, 20)])}

shapes = {'p': ((-10, -10), (-10, 10), (10, 10), (10, -10)),
          'j': ((-30, -30), (-30, 10), (30, 10), (30, -10), (-10, -10), (-10, -30)),
          'o': ((-30, -30), (-30, 10), (10, 10), (10, -30)),
          'z': ((-30, -10), (-30, 30), (-10, 30), (-10, 10), (10, 10), (10, -30), (-10, -30), (-10, -10)),
          'l': ((-30, -10), (-30, 30), (-10, 30), (-10, 10), (30, 10), (30, -10)),
          'i': ((-30, -10), (-30, 10), (50, 10), (50, -10)),
          's': ((-30, -30), (-30, 10), (-10, 10), (-10, 30), (10, 30), (10, -10), (-10, -10), (-10, -30)),
          't': ((-10, -30), (-10, 30), (10, 30), (10, 10), (30, 10), (30, -10), (10, -10), (10, -30))}

for i, j in shapes.items():
    screen.register_shape(i, j)

"""
Game Set Up 
"""

"""Setup the grid (background)"""
grid = turtle.Turtle()
grid.penup()
grid.speed(0)
grid.color('white')
grid.ht()

"""Grid is represented as a pixel which is shape 'p' """
grid.shape('p')
block = grid.clone()

"""At this point, the code show single block at the center of the window """
block.st()
screen.update()

""" Define top, left, right and bottom corner of a grid. Size is the size of the block """
Left = -100
Right = 80
Bottom = -160
Top = 140
size = 20

""" pixels in computer language are the smallest blocks that a screen can be divided into. Size of pixel 
    is important as it dictates the resolution of a screen
"""

""" In this code, pixels is a dictionary that stores key as Y-coordinate of the row
    and value as another dictionary where key is X-coordinate and value is the block (pixel) itself
    Structure of pixels dictionary looks something like this:
    
    pixels
        key: Y-Coordinate of row
        value:
            key: X-coordinate of each pixel inside a given row
            value: pixel itself (this is a clone of block that we drew above)  
"""
pixels = {}

for i in range(Bottom, Top + size, size):
    pixels[i] = {}
    for j in range(Left, Right + size, size):
        pixels[i][j] = grid.clone()
        pixels[i][j].goto(j, i)
        pixels[i][j].stamp()

""" Summary of pixels"""
""" Basically a pixels dictionary can provide you with 3 informations
    1. Y coordinate of a pixel
    2. X coordinate of a pixel
    3. pixel block itself
"""


""" To visualize how pixels look, try enable below prints and see how it is organized"""
"""
for row in pixels:
    print("Y=", row)
    for block in pixels[row]:
        print("\t\tX=", block, "  pixel=", pixels[row][block])
"""


""" Setup Global Game variables here"""
letter = ""
shape = ""

"""Game Loop"""


def reset():
    """
    The goal of this function is to reset the shape
    to a another random shape whenever reset() function
    is called.
    Step 1: gets random letter out of "jozlist"
    Step 2: "shape_info" variable stores color and offset information of the shape for chosen letter
    Step 3: "block" shape is changed to letter shape, set heading to "downward" and block is sent to top
    Step 4: store the offset of the Shape in "shape" variable
    :return: None
    """
    global letter, shape
    letter = "jozlist"[random.randint(0, 6)]
    shape_info = blocks[letter]
    block.seth(0)
    block.goto(0, Top)
    block.shape(letter)
    block.color(shape_info[0])
    shape = shape_info[1][:]  # shape is nothing but stores the offset
    drop()


def drop():
    """
    drop() is a recursive function meaning it calls itself using ontimer() function every 800 milliseconds
    The loop has two conditions:
        1. If the block is inside the bound, let it drop
        2. Else, if the block is not at TOP, then update the boundaries using function add_to_bound()

        Now, Update boundary only if the block is inside the GRID, else we dont care
        Why update the boundary?
        It is simply because when next block comes down it cannot occupy the same space as previous block. So that is
        like a boundary to the new block

        Also, we need to check if row is complete. If yes, we scored some points and we need to remove the row
        from the screen and update the boundaries. check_row() function does that

    :return: None
    """
    if check_bound(0, -size, shape):
        block.goto(block.xcor(), block.ycor() - size)
        screen.ontimer(drop, 800)
    else:
        if block.ycor() != Top:
            add_to_bound()
            check_row()
            reset()
    screen.update()


"""Just like pixels are stored as a dictionary, Bounding Area is also stored as a dictionary """
bound = {}


def check_bound(dx, dy, offsets):
    """
    Check bound is a very simple function to check if we are not overlapping other blocks or
    we are not going outside the boundaries of the grid
    :param dx: denotes change in x direction
    :param dy: denotes change in y direction
    :param offsets: shape offset that is provided at the beginning using blocks dictionary
    :return: True if inside boundary, else False
    """
    x = block.xcor()
    y = block.ycor()
    # ty and tx are total y and x positions, includes the offset of a block as well as the direction
    # in which block is moving denoted by dy or dx.
    for ii in offsets:
        ty = y + ii[0] + dy
        tx = x + ii[1] + dx
        # check bottom, left and right first
        # check if ty is in bound dictionary, this is also not allowed as we cannot overlap previous
        # blocks that are on the screen
        if ty < Bottom or tx < Left or tx > Right or (ty in bound.keys() and tx in bound[ty]):
            return False

    return True


def add_to_bound():
    """
    The function simply updates the bound dictionary with
    all the pixels that are either out of grid or already occupied
    by previous block.

    This function is called when check_bound() function has returned false, means block has
    not space to drop further.
    In this function,
        First we check y-position of the block,
                if already in bound keys then we go ahead and add the x-position
                if not in bound then we create a new set using in-build function (set())
        Second we create a pixel at a given Y and X position, and color that pixel with same color as block
        Third we set the pixel turtle to show turtle.

    :return: None
    """
    x = block.xcor()
    y = block.ycor()
    for ii in shape:
        ty = y + ii[0]
        tx = x + ii[1]
        # Create a set if current y-position is not in bound dictionary
        if ty not in bound.keys():
            bound[ty] = set()

        bound[ty].add(tx)
        pixel = pixels[ty][tx]
        pixel.color(block.fillcolor())
        pixel.st()


"""Collapsing Rows"""


def check_row():
    """
    This function helps collapse rows if row is completely occupied.
    This is where we should update score.

    We have 10 blocks in one row.
    Logic starts checking rows from bottom to top by sorting the bound keys
    If size of bound[y] is equal to 10, then keep moving up until we reach the top

    If we find a row that can be collapsed, next step is to actually collapse it

    :return:
    """
    full = (Right - Left + size) / size
    t = sorted(bound.keys())
    up = 0
    for ii in t:
        while ii + up in bound.keys() and len(bound[ii + up]) == full:
            up += size

        if up > 0:
            if ii + up in bound.keys():
                bound[ii] = set(bound[ii + up])
                for k in pixels[ii].keys():
                    if pixels[ii + up][k].isvisible():
                        pixels[ii][k].color(pixels[ii + up][k].fillcolor())
                        pixels[ii][k].st()
                    else:
                        pixels[ii][k].ht()
            else:
                del bound[i]
                for v in pixels[ii].values():
                    v.ht()


"""Keyboard Controls"""


def move_by(dx, dy):
    """
    Checks bound before moving the block
    :param dx: change in x direction
    :param dy: change in y direction
    :return: None
    """
    if check_bound(dx, dy, shape):
        block.goto(block.xcor() + dx, block.ycor() + dy)


def left():
    """
    Function to move block left
    :return: None
    """
    move_by(-size, 0)


def right():
    """
    Function to move block right
    :return: None
    """
    move_by(size, 0)


def down():
    """
    Function to move block down
    :return: None
    """
    move_by(0, -size)


def rotate_left():
    """
    Used to change shape of the block

    Before rotating the block by 90 degrees, we need to check boundaries of rotated block
    just to make sure we don't go out of bound when rotation is actually applied.

    Once check_bound() returns True, then need to update shape variable as well with new shape

    :return: None
    """
    global shape
    t = []
    for ii in shape:
        t.append((ii[1], -ii[0]))

    if check_bound(0, 0, t):
        shape = t
        block.left(90)


def rotate_right():
    """
    Used to change shape of the block

    Before rotating the block by 90 degrees, we need to check boundaries of rotated block
    just to make sure we don't go out of bound when rotation is actually applied.

    Once check_bound() returns True, then need to update shape variable as well with new shape

    :return: None
    """
    global shape
    t = []
    for ii in shape:
        t.append((-ii[1], ii[0]))

    if check_bound(0, 0, t):
        shape = t
        block.right(90)


screen.onkey(left, "Left")
screen.onkey(right, "Right")
screen.onkey(down, "Down")
screen.onkey(rotate_left, "a")
screen.onkey(rotate_right, "d")
screen.listen()

reset()
turtle.done()
