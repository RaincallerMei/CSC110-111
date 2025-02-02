"""CSC110 Fall 2024 Assignment 1, Part 1: Colour Rows

Instructions (READ THIS FIRST!)
===============================

Please follow the instructions in the assignment handout to complete this file.

Note that you only need to complete the function bodies.
You are not required to add more doctest examples, though you may do so to help
with your own understanding/testing.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC110 Teaching Team
"""
import a1_helpers


###################################################################################################
# 0. Warmup
###################################################################################################
def warmup1() -> None:
    """Visualize an example colour row using pygame.

    This function illustrates the use of the helper function a1_helpers.show_colours_pygame
    that we have provided you. We encourage you to use that function to visualize your
    work on the various questions in this part of the assignment!
    """
    example_colours = [[0, 255, 200], [1, 2, 3], [100, 100, 100], [181, 57, 173], [33, 0, 197]]
    a1_helpers.show_colours_pygame(example_colours)

###################################################################################################
# 1. Cropping colour rows
###################################################################################################


def crop_row(colour_row: list, start: int, num_colours: int) -> list:
    """Return a colour row containing the specified colours from the given colour_row.

    Notes:
    1. start is the index of the first colour to take from colour_row.
    2. num_colours specifies the number of colours to take from colour_row.
        If num_colours == 0, no colours are taken (and an empty list is returned)

    You may ASSUME that:
    - colour_row is a valid colour row (i.e., is a list of RGB sublists)
    - start >= 0
    - num_colours >= 0
    - start + num_colours <= len(colour_row)

    >>> example_colours = [[0, 255, 200], [1, 2, 3], [100, 100, 100], [181, 57, 173], [33, 0, 197]]
    >>> crop_row(example_colours, 1, 2)  # Take two colours from example_colours starting at index 1
    [[1, 2, 3], [100, 100, 100]]
    """
    return [colour_row[index] for index in range(start, start + num_colours)]


def crop_row_border_single(colour_row: list) -> list:
    """Return a colour row with the colours from the given colour_row, except with the first and last colour removed.

    You may ASSUME that:
    - colour_row is a valid colour row (i.e., is a list of RGB sublists)
    - len(colour_row) >= 2

    >>> example_colours = [[0, 255, 200], [1, 2, 3], [100, 100, 100], [181, 57, 173], [33, 0, 197]]
    >>> crop_row_border_single(example_colours)
    [[1, 2, 3], [100, 100, 100], [181, 57, 173]]

    You may implement this function by using a list comprehension OR by calling crop_row
    with the appropriate arguments. (For extra practice, try both ways!)
    """
    return [colour_row[color] for color in range(1, len(colour_row) - 1)]


def crop_row_border_multiple(colour_row: list, border_size: int) -> list:
    """Return a colour row with the colours from the given colour_row, except with
    the first and last border_size colours removed.

    Note: when border_size == 1, this function does the same thing as crop_row_border_single.

    You may ASSUME that:
    - colour_row is a valid colour row (i.e., is a list of RGB sublists)
    - 1 <= border_size <= len(colour_row) // 2

    >>> example_colours = [[0, 255, 200], [1, 2, 3], [100, 100, 100], [181, 57, 173], [33, 0, 197]]
    >>> crop_row_border_multiple(example_colours, 1)  # Remove the first and last colours
    [[1, 2, 3], [100, 100, 100], [181, 57, 173]]
    >>> crop_row_border_multiple(example_colours, 2)  # Remove the first 2 and last 2 colours
    [[100, 100, 100]]

    You may implement this function by using a list comprehension OR by calling crop_row
    with the appropriate arguments. (For extra practice, try both ways!)
    """
    return [colour_row[color] for color in range(border_size, len(colour_row) - border_size)]


###################################################################################################
# 2. Changing colours
###################################################################################################
def remove_red_in_row(colour_row: list) -> list:
    """Return a new colour row consisting of the same colours as the given row, except each colour
    has its "red" value changed to 0.

    You may ASSUME that:
    - colour_row is a valid colour row (i.e., is a list of RGB sublists)

    >>> example_colours = [[0, 255, 200], [1, 2, 3], [100, 100, 100], [181, 57, 173], [33, 0, 197]]
    >>> remove_red_in_row(example_colours)
    [[0, 255, 200], [0, 2, 3], [0, 100, 100], [0, 57, 173], [0, 0, 197]]
    """
    return [[0, b, c] for [a, b, c] in colour_row]


def greyscale(colour_row: list) -> list:
    """
    Return a new colour row consisting of the *grayscale version* of each
    colour in the given row.

    The grayscale version of a colour (r, g, b) is equal to (x, x, x), where
    x is the average of r, g, and b, rounded down to the nearest integer.

    You may ASSUME that:
    - colour_row is a valid colour row (i.e., is a list of RGB sublists)

    >>> example_colours = [[100, 100, 100], [200, 100, 0], [25, 30, 20]]
    >>> greyscale(example_colours)
    [[100, 100, 100], [100, 100, 100], [25, 25, 25]]
    """
    return [[int((a + b + c) / 3), int((a + b + c) / 3), int((a + b + c) / 3)] for [a, b, c] in colour_row]


def sepia(colour_row: list) -> list:
    """
    Return a new colour row consisting of new colours calculated based on the following
    rules:

    - Get the RGB value of each pixel in the given colour_row
    - Calculate new values using the formula below, where R, G and B each refer to
    the original R, G and B values of the given pixel:

        new red value = 0.393*R + 0.769*G + 0.189*B
        new green value = 0.349*R + 0.686*G + 0.168*B
        new blue value = 0.272*R + 0.534*G + 0.131*B
        (Round each resulting new value down to the nearest integer --
        Hint: convert the resulting float to an int)

        If any of these output values is greater than 255, simply set it to 255
        (Hint: the built-in function min will be useful for this).

        These specific values are the recommended values for sepia tone.

    You may ASSUME that:
    - colour_row is a valid colour row (i.e., is a list of RGB sublists)

    >>> sepia([[255, 0, 0], [0, 0, 255], [255, 255, 255]])
    [[100, 88, 69], [48, 42, 33], [255, 255, 238]]
    """
    return [[min(int(0.393 * r + 0.769 * g + 0.189 * b), 255), min(int(0.349 * r + 0.686 * g + 0.168 * b), 255),
             min(int(0.272 * r + 0.534 * g + 0.131 * b), 255)] for [r, g, b] in colour_row]


###################################################################################################
# 3. Distorting colours
###################################################################################################
def pixelate_row(colour_row: list, block_size: int) -> list:
    """
    Return pixelated version of the row where block_size adjacent pixels are grouped together
    and replaced with a single representative color, using the following rule:
    - block_size pixels are grouped together
    - each pixel in the group is replaced with the same colour as the left-most pixel
        in that group

    You may ASSUME that:
    - colour_row is a valid colour row (i.e., is a list of RGB sublists)
    - len(colour_row) can be divided evenly by block_size

    >>> example_colour = [[0, 0, 0], [255, 255, 255], [0, 0, 255], [67, 67, 67], \
    [255, 0, 0], [100, 0, 100]]
    >>> size = 2
    >>> pixelate_row(example_colour, size)
    [[0, 0, 0], [0, 0, 0], [0, 0, 255], [0, 0, 255], [255, 0, 0], [255, 0, 0]]
    """
    return [colour_row[index] for index in range(0, len(colour_row), block_size) for time in range(block_size)]

###################################################################################################
# "Main block" (we'll discuss what this means in lecture)
###################################################################################################


if __name__ == '__main__':
    import doctest

    # To run the doctest examples for a single function only, you can right-click on that
    # function's code above and choose "Run 'Doctest <function name>'"
    # If you want to run ALL the doctests included in this file at once, uncomment
    # the following line by deleting the # symbol and the space before it.

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['a1_helpers'],
        'max-line-length': 120
    })
