"""CSC110 Fall 2024 Assignment 2, Part 3: Sentiment Analysis

Module Description
===============================
This module contains starter code for the program described in Part 3.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC110 Teaching Team
"""
# Constant representing a small subset of our larger sentiment scores data
# You may use this smaller dictionary for testing purposes
SAMPLE_SENTIMENTS = {'shine': (0.375, 0.125),
                     'wrong': (0.125, 0.75),
                     'lovely': (0.625, 0.0),
                     'worst': (0.25, 0.75),
                     'broken': (0.0, 0.125),
                     'chill': (0.0, 0.25),
                     'good': (0.625, 0.0),
                     'glad': (0.75, 0.125),
                     'cruel': (0.0, 0.125),
                     'fine': (0.625, 0.125),
                     'trick': (0.0, 0.125),
                     'ideal': (0.0, 0.0),
                     'favorite': (0.125, 0)}

POSITIVE, NEGATIVE, NEUTRAL = 'positive', 'negative', 'neutral'

###############################################################################
# Complete the functions below
###############################################################################


def normalize_text(text: str) -> str:
    """
    Return a copy of text with all alphabetical characters turned lowercase and
    all non-alphabetical characters removed and replaced with a space.

    >>> normalize_text("Hey! How are you? I'm fine. ;D")
    'hey  how are you  i m fine   d'

    Hint: Use appropriate string methods as helpers
    """
    text2 = ""
    for char in text:
        if char.isalpha():
            text2 += char.lower()
        else:
            text2 += ' '
    return text2


def get_keywords(word_list: list[str], sentiment_scores: dict[str, tuple[float, float]]) -> \
        tuple[dict[str, int], dict[str, int]]:
    """Return a tuple of two dictionaries that map each keyword that occurs in word_list (keywords are all words
    that appear in the given sentiment_scores dictionary) with its total number of occurrences in word_list.

    The first dictionary should contain only positive words (words whose positivity score is
    greater than its negativitiy score). The second dictionary should contain only negative words
    (words whose positivity score is less than its negativity score). Neutral words are not added to either dictionary.

    >>> get_keywords(['we', 'will', 'be', 'fine', 'just', 'let', 'it', 'shine', 'shine', 'shine'], SAMPLE_SENTIMENTS)
    ({'fine': 1, 'shine': 3}, {})

    >>> get_keywords(['so', 'wrong', 'but', 'so', 'lovely', 'ideal', 'utopia'], SAMPLE_SENTIMENTS)
    ({'lovely': 1}, {'wrong': 1})
    """
    good = {}
    bad = {}
    for word in word_list:
        if word in sentiment_scores:
            if sentiment_scores[word][0] > sentiment_scores[word][1]:
                good[word] = good.get(word, 0) + 1
            elif sentiment_scores[word][0] < sentiment_scores[word][1]:
                bad[word] = bad.get(word, 0) + 1
    return (good, bad)


def get_overall_score(word_list: list[str], sentiment_scores: dict[str, tuple[float, float]]) -> float:
    """
    Return the overall sentiment score of the text contained in word_list, rounded to up to 3 decimal places,
    based on keyword scores in the sentiment_scores dictionary and the instructions in the a2 handout.

    Preconditions:
    - any({word in sentiment_scores for word in word_list})

    >>> get_overall_score(['we', 'will', 'be', 'fine', 'just', 'let', 'it', 'shine', 'shine', 'shine'], \
    SAMPLE_SENTIMENTS)
    0.312
    >>> get_overall_score(['so', 'wrong', 'but', 'so', 'lovely', 'ideal', 'utopia'], SAMPLE_SENTIMENTS)
    0.0
    >>> get_overall_score(['so', 'wrong', 'wrong', 'wrong', 'but', 'so', 'lovely', 'ideal', 'utopia', 'a', 'trick'], \
    SAMPLE_SENTIMENTS)
    -0.229
    """
    total_score = 0.0
    tot_words = 0
    for word in word_list:
        if word in sentiment_scores:
            total_score += sentiment_scores[word][0]
            total_score -= sentiment_scores[word][1]
            tot_words += 1
    return round(total_score / tot_words, 3)


def get_sentiment_info(filename: str, sentiment_scores: dict[str, tuple[float, float]]) -> \
        tuple[tuple[dict[str, int], dict[str, int]], str, float]:
    """Return the following information about the text in the given filename:
    1. A tuple of two dictionaries mapping each sentiment keyword that appears in the text to its total
        number of occurrences – the first dict only contains positive keywords, and the second only negative keywords
    2. The overall sentiment category (POSITIVE, NEGATIVE or NEUTRAL)
    3. The overall sentiment score rounded to up to 3 decimal places

    Preconditions:
    - filename refers to a valid file
    - at least one word in the file referred to by filename appears in the sentiment_scores
    dictionary


    >>> get_sentiment_info('data/texts/dance_the_night.txt', SAMPLE_SENTIMENTS)
    (({'shine': 1}, {}), 'positive', 0.25)
    >>> get_sentiment_info('data/texts/cruel_summer.txt', SAMPLE_SENTIMENTS)
    (({'fine': 2}, {'cruel': 6, 'worst': 2}), 'negative', -0.075)

    # An example with the much larger sentiment file is below
    # Note: the formatting below may seem odd, but that's a way to make doctest accept multi-line outputs and we
    # are using multiple lines below to make our code be at a readable width (that also makes pyTA happy)
    >>> get_sentiment_info('data/texts/uptown_funk.txt', build_sentiment_score_dict('data/sentiment_scores.txt'))
    (({'good': 1, 'masterpieces': 1, 'saint': 1, 'pretty': 1, 'hot': 18, 'sexy': 2, 'well': 1, 'woo': 3}, \
{'cold': 1, 'damn': 9, 'break': 2}), 'positive', 0.242)
    """

    # NOTE: Much of this function is completed for you, you just need to fill in the gaps to
    # complete it as instructed below

    text = read_text(filename)

    # Clean the text
    cleaned_text = normalize_text(text)

    word_list = cleaned_text.split()

    keyword_counts = get_keywords(word_list, sentiment_scores)
    overall_sentiment = get_overall_score(word_list, sentiment_scores)

    # Do not change any of the code below
    if overall_sentiment >= 0.05:
        category = POSITIVE
    elif overall_sentiment <= -0.05:
        category = NEGATIVE
    else:
        category = NEUTRAL

    return keyword_counts, category, overall_sentiment


###############################################################################
# DO NOT EDIT THE CODE BELOW
# Note: You do not need to understand how the functions below work.
###############################################################################
def build_sentiment_score_dict(filename: str) -> dict[str, tuple[float, float]]:
    """Return the movie review stored in the given file.

    The file is a CSV file with two rows, a header row and a row of actual
    movie review data. These files are based on real movie review data from Metacritic,
    though they have been altered slightly to fit this assignment.
    """

    sentiments = {}

    with open(filename) as f:

        for line in f:
            if not line.startswith("#"):  # skip header rows
                [positive, negative, word] = line.strip().split("\t")
                # add to dict: key is word, value is tuple with positive and negative scores for that word
                sentiments[word] = (float(positive), float(negative))

    return sentiments


def read_text(filename: str) -> str:
    """Return the text stored in the given file.
    """
    with open(filename) as file:
        return file.read()


def run_analysis(filename: str, sentiment_scores: dict[str, tuple[float, float]]) -> None:
    """Display sentiment analysis results for text in the given filename.
    """

    keywords, category, score = get_sentiment_info(filename, sentiment_scores)

    print("The positive/neutral sentiment keywords found in this text were:")

    for key, value in keywords[0].items():
        print(f"{key} occurred {value} time(s)")

    print("============================")
    print("The negative sentiment keywords found in this text were:")

    for key, value in keywords[1].items():
        print(f"{key} occurred {value} time(s)")

    print("============================")
    print(f"Based on these keywords, the overall sentiment of this text is <{category}> with a score of {score}")


if __name__ == '__main__':
    # Once you complete the above functions, uncomment the lines below to do a full analysis of your chosen file

    text_file = 'data/texts/cruel_summer.txt'  # change the filename here, to be used with the code below
    sentiment_scores_large = build_sentiment_score_dict('data/sentiment_scores.txt')

    run_analysis(text_file, SAMPLE_SENTIMENTS)  # change the second argument to sentiment_scores_large to analyze
    # the file with the larger sentiment score data

    # DO NOT MODIFY ANY CODE BELOW (You can and should comment/uncomment them out for testing purposes though)
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E9998', 'C9103']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
