"""CSC110 Fall 2024 Problem Set 1, Part 2: Predicate Logic

Instructions (READ THIS FIRST!)
===============================
This Python module contains the functions you should complete for PS1, Part 2.
Your task is to:

1. Implement functions `statement1` and `statement2` so that they translate the statements given in
Part 2.
2. Define `example_p`, and `example_q` as an example input to `statement1` and `statement2`, then
use `test_statements_different` to show that these two functions don't compute the same things.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC110 Teaching Team
"""
# See the 'readings' in the handout for explanations about Any and Callable below
from typing import Any, Callable


###############################################################################
# Part 2, Question 2
###############################################################################
def statement1(my_set: set,
               my_p: Callable[[Any], bool],
               my_q: Callable[[Any, Any], bool]) -> bool:
    """Implementation of Statement 1 from Part 2, Question 2.

    This statement is represented as a function that takes three arguments:
        - a set my_set (corresponds to "S" from the statement)
        - a predicate my_p (corresponds to the predicate "P" from the statement);
          its domain is my_set
        - a predicate my_q (corresponds to the predicate "Q" from the statement);
          its domain is my_set x my_set

    Note that my_p is a *function* and can be called inside the body below, e.g. my_p(...).
    Similarly, my_q is a binary function and can be called using my_q(..., ...).

    Because my_set could contain elements of different types, we use the "Any" type
    annotation for the parameter types of my_p and my_q. (See the readings from the
    assignment handout.)

    Preconditions:
        - my_p can be called on every element from my_set
        - my_q can be called on every pair of two elements from my_set
    """
    return all(any(not my_p(x) or my_q(x, y) for y in my_set) for x in my_set)

def statement2(my_set: set,
               my_p: Callable[[Any], bool],
               my_q: Callable[[Any, Any], bool]) -> bool:
    """Implementation of Statement 2 from Part 2, Question 2.
    """
    return all(any(not my_q(x,y) or my_p(x) for y in my_set) for x in my_set)

###############################################################################
# Part 2, Question 3
###############################################################################
def test_statements_different() -> None:
    """A test that verifies that statement1 and statement2 are not equivalent.
    """
    my_set = {1,2,3,4}
    assert statement1(my_set, example_p, example_q) != statement2(my_set, example_p, example_q)

def example_p(x: Any) -> bool:
    """An example predicate for "my_p" that can be used in test_statements_different.
    """
    return x>3

def example_q(x: Any, y: Any) -> bool:
    """An example predicate for "my_q" that can be used in test_statements_different.
    """
    return x+3 >= y

if __name__ == '__main__':
    import pytest
    pytest.main(['ps1_part2.py', '-v'])

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['R1705']
    })
