"""CSC110 Fall 2024 Problem Set 1, Part 1: Interpreting Test Results

Instructions (READ THIS FIRST!)
===============================

This Python module contains the program and tests described in Problem Set 1,
Part 1. You can run this file as given to see the pytest report given in the
handout. Your task is to fix all errors in this file so that each test passes
(see problem set handout for details).

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC110 Teaching Team
"""
import math
import pytest


###############################################################################
# Professor Chirly's program
###############################################################################
def class_average(class_grades: list) -> float:
    """Return the weighted average grade of students for all grades in class_grades.

    Each element of class_grades is itself a list, containing three floats
    representing the grades of a particular student on the three assignments.

    See assignment handout for details.

    You may ASSUME that:
        - class_grades is non-empty
        - class_grades contains only lists
        - the lists in class_grades contain exactly three floats
        - each float in each list is between 0.0 and 100.0.

    """
    student_averages = [student_average(grades) for grades in class_grades]

    # Return the average grade across all students in this section
    return sum(student_averages) / len(student_averages)


def student_average(grades: list) -> float:
    """Return the weighted average of a student's grades.

    You may ASSUME that:
        - grades consists of exactly three float values
    """
    # Sort the student's grades
    sorted_grades = sorted(grades, reverse=True)
    print(sorted_grades)
    # These are the weights for the assignment grades
    weights = [0.4, 0.35, 0.25]

    return (
            weights[0] * float(sorted_grades[0]) +
            weights[1] * float(sorted_grades[1]) +
            weights[2] * float(sorted_grades[2])
    )


###############################################################################
# Tests for section_average
###############################################################################
def test_class_average_single_student_equal() -> None:
    """Test class_average with only a single student in the class
    who received the same grade on each assignment.
    """
    grades = [[70.0, 70.0, 70.0]]

    # DO NOT MODIFY ANY OF THE BELOW LINES IN THIS TEST
    expected = 70.0
    actual = class_average(grades)
    assert math.isclose(actual, expected)


def test_section_average_many_students_equal() -> None:
    """Test class_average when there are a lot of students in a section,
    and all students have the same grade on each assignment.
    """
    grades = [['80.0', '80.0', '80.0'],
              ['90.0', '90.0', '90.0'],
              ['97.0', '97.0', '97.0'],
              ['68.0', '68.0', '68.0'],
              ['77.0', '77.0', '77.0']]

    # DO NOT MODIFY ANY OF THE BELOW LINES IN THIS TEST
    expected = 82.4
    actual = class_average(grades)
    assert math.isclose(actual, expected)


def test_class_average_many_students_different() -> None:
    """Test class_average when there are a lot of students in a section.
    """
    grades = [[80.0, 70.0, 75.0],
              [90.0, 78.0, 65.0],
              [66.0, 74.0, 60.0],
              [60.0, 55.0, 75.0],
              [82.0, 80.0, 88.0],
              [50.0, 88.0, 73.0]]

    # DO NOT MODIFY ANY OF THE BELOW LINES IN THIS TEST
    expected = 74.15
    actual = class_average(grades)
    assert math.isclose(actual, expected)


if __name__ == '__main__':
    pytest.main(['ps1_part1.py', '-v'])


