import time
import turtle
from rubik_solver import utils


CUBE_SIZE = 50
SIDE_SIZE = CUBE_SIZE * 3
ALL_COLORS = ['yellow', 'green', 'orange', 'blue', 'red', 'white']


class CubeSide:
    """
    The cube side datatype, storing what color each row/col currently is
    and where the side is relative to the top-left corner
    """
    def __init__(self,
                 offset_x: int,
                 offset_y: int,
                 initial_color: str):

        # Set these so we can know where to draw the side relative
        # to the top-left corner of the canvas in pixels
        self.offset_x = offset_x
        self.offset_y = offset_y

        # Generate a 3x3 matrix with the colors stored
        self.rows = []
        for x in range(3):
            col = []
            for y in range(3):
                col.append(initial_color)
            self.rows.append(col)


def draw(cube_side):
    """
    Draw all rows and columns
    """
    pen.showturtle()
    for row in range(3):
        for col in range(3):
            draw_row_col(cube_side, row, col)
    pen.hideturtle()


def draw_row_col(cube_side, row, col):
    """
    Draw a single square of a row/column
    """

    # Go to the top left position of the square to be drawn
    pen.penup()
    pen.goto(cube_side.offset_x + row * CUBE_SIZE,
             cube_side.offset_y + col * CUBE_SIZE)
    pen.pendown()

    # Turn off low-level animation to increase performance
    screen.tracer(False)
    # Set the line and background color
    pen.color('black')
    pen.fillcolor(cube_side.rows[row][col])
    pen.begin_fill()

    # Using setheading() in degrees 0-360 here
    # because of rounding errors with right()
    heading = 0
    for side in range(4):
        pen.setheading(heading)
        pen.forward(CUBE_SIZE)
        heading += 90

    pen.end_fill()
    pen.penup()
    screen.tracer(True)
    time.sleep(0.01)


def xy_coords_to_row_col(cube_side, x, y):
    """
    Convert x/y coordinates in pixels to the row/column
    of an individual square in a cube side.
    """

    def point_in_rectangle(bottom_left, top_right, point):
        return (bottom_left[0] < point[0] < top_right[0]) and \
               (bottom_left[1] < point[1] < top_right[1])

    for row in range(3):
        for col in range(3):
            if point_in_rectangle(
                [cube_side.offset_x + CUBE_SIZE*row,
                 cube_side.offset_y + CUBE_SIZE*col],
                [cube_side.offset_x + CUBE_SIZE + CUBE_SIZE*row,
                 cube_side.offset_y + CUBE_SIZE + CUBE_SIZE*col],
                [x, y]
            ):
                return [row, col]
    return None


def cycle_cube_color(cube_side, row, col):
    """
    Make a cube the next color of 6 available colors and refresh
    """

    # Figure out where relative to the start of the list the current color is
    current_color_index = ALL_COLORS.index(cube_side.rows[row][col])

    # Get the next color, starting at the start color again if we run out
    try:
        next_color = ALL_COLORS[current_color_index + 1]
    except IndexError:
        next_color = ALL_COLORS[0]

    # Remember the color+draw
    cube_side.rows[row][col] = next_color
    draw_row_col(cube_side, row, col)


def solve_and_exit():
    colors = ''
    for cube_side in CUBE_SIDES:
        for row in cube_side.rows:
            for color in row:
                # Get the first letter of each color to convert to a
                # format rubik_solver understands
                colors += color[0].lower()

    # Output the rubik_solver solutions to the console
    # It would be possible to show this using `turtle` too
    print(utils.solve(colors, 'Beginner'))
    print(utils.solve(colors, 'CFOP'))
    print(utils.solve(colors, 'Kociemba'))

    # Exit the program
    raise SystemExit()


def onclick(x, y):
    if y < 50 and x > SIDE_SIZE * 3.3:
        # "solve and exit" clicked!
        solve_and_exit()

    for cube_side in CUBE_SIDES:
        row_col = xy_coords_to_row_col(cube_side, x, y)
        if row_col:
            row, col = row_col
            cycle_cube_color(cube_side, row, col)


# Define the cube sides and where to place them
#         [Side 1]
# [Side 2][Side 3][Side 4][Side 5]
#         [Side 6]
CUBE_SIDES = [CubeSide(SIDE_SIZE, 0, 'yellow'),
              CubeSide(0, SIDE_SIZE, 'green'),
              CubeSide(SIDE_SIZE, SIDE_SIZE, 'orange'),
              CubeSide(SIDE_SIZE * 2, SIDE_SIZE, 'blue'),
              CubeSide(SIDE_SIZE * 3, SIDE_SIZE, 'red'),
              CubeSide(SIDE_SIZE, SIDE_SIZE * 2, 'white')]

# Create turtle screen and pen
screen = turtle.Screen()
screen.setworldcoordinates(0, (SIDE_SIZE*3)+7,
                           (SIDE_SIZE*4)+7, 0)
pen = turtle.Turtle(shape="turtle")
pen.speed('fast')

# Draw the cube sides
for cube_side in CUBE_SIDES:
    draw(cube_side)

# Show a "solve and exit" button in the top right
pen.showturtle()
pen.penup()
pen.goto(SIDE_SIZE * 3.3, 20)
pen.write("solve and exit >", font=("Arial", 16, "normal"))
pen.hideturtle()

screen.onclick(onclick)
screen.mainloop()
