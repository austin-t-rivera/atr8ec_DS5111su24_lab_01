"""Module of function for text processing"""
import string
import logging
from collections import Counter

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def clean_text(text):
    """
    Function: To clean text by removing punctuation and making text lower case
    Input: raw text
    Output: clean text
    """
    assert isinstance(text, str), "Input Error: Text != str"
    logging.debug("Cleaning your text: %s", text)

    cleaned_text = text.lower().translate(str.maketrans('', '', string.punctuation))

    assert cleaned_text, "Output Error: cleaned_text is null"
    logging.debug("Your cleaned text: %s", cleaned_text)

    return cleaned_text

def tokenize(text):
    """
    Function: To clean text and split clean text by spaces and save as a list of tokens
    Input: raw text
    Output: list of tokens
    """
    assert isinstance(text, str), "Input Error: Text is not a string!"
    logging.debug("Tokenizing your text: %s", text)

    tokens = clean_text(text).split(" ")

    assert isinstance(tokens, list), "Output Error: Tokens != list"
    assert all(isinstance(word, str) for word in tokens), "Output Error: token != str"
    logging.debug("Your tokens: %s", tokens)

    return tokens

def count_words(text):
    """
    Function: To clean, tokenize, and count tokens and save as a dictionary
    Input: raw text
    Output: clean text 
    """
    assert isinstance(text, str), "Input Error: Text != str"
    logging.debug("Counting word occurences in the text %s", text)

    word_counts = Counter(tokenize(text))

    assert word_counts, "Output Error: Word count dictionary cannot be empty!"
    assert all(isinstance(word, str) for word in word_counts.keys()), "Output Error: word != str"
    assert all(isinstance(cnt, int) for cnt in word_counts.values()), "Output Error: count != int"
    logging.debug("Counts for each word: %s", word_counts)

    return word_counts
