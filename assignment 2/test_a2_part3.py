"""CSC110 Fall 2024 Assignment 2, Part 3: Sentiment Analysis

Module Description
===============================
This module contains starter code for the tests for a few of the functions described in Part 3.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC110 Teaching Team
"""
from hypothesis import given
from hypothesis.strategies import lists, dictionaries, text, tuples, floats

import a2_part3

@given(lst = lists(text()), x=dictionaries(text(), tuples(floats(min_value=0.0), floats(min_value=0.0))))
def test_get_keywords_no_mut(lst, x) -> None:
    """Test that get_keywords does not mutate its arguments."""
    lst_copy = lst.copy()
    x_copy = x.copy()

    a2_part3.get_keywords(lst_copy, x_copy)

    assert lst == lst_copy and x == x_copy


@given(lst = lists(text(), min_size=1), x=dictionaries(text(), tuples(floats(min_value=0.0), floats(min_value=0.0))))
def test_get_overall_score_no_mut(lst, x) -> None:
    """Test that get_overall_score does not mutate its arguments."""
    if lst:
        word_to_add = lst[0]
        x[word_to_add] = (0.5, 0.5)

        original_lst = lst.copy()
        original_x = x.copy()

        # Call the function.
        a2_part3.get_overall_score(lst, x)

        assert lst == original_lst
        assert x == original_x

if __name__ == '__main__':
    # DO NOT MODIFY ANY CODE BELOW (You can and should comment/uncomment them out for testing purposes though)
    import pytest

    pytest.main(['test_a2_part3.py', '--disable-warnings'])

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['hypothesis', 'hypothesis.strategies', 'a2_part3'],
        'max-line-length': 120
    })
