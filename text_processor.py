import string
import logging
from collections import Counter

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def clean_text(text):

        assert isinstance(text, str), "Input Error: Text is not a string!"
        logging.debug(f"Cleaning your text: {text}")

        cleaned_text = text.lower().translate(str.maketrans('', '', string.punctuation))

        assert cleaned_text, "Output Error: Cleaned text cannot be null! Non-punctuation characters are required!"
        logging.debug(f"Your cleaned text: {cleaned_text}")

        return cleaned_text

def tokenize(text):

        assert isinstance(text, str), "Input Error: Text is not a string!"
        logging.debug(f"Tokenizing your text: {text}")

        tokens = clean_text(text).split(" ")

        assert isinstance(tokens, list) and all(isinstance(word, str) for word in tokens), "Output Error: Tokens should be a list of strings!"
        logging.debug(f"Your tokens: {tokens}")

        return tokens

def count_words(text):

        assert isinstance(text, str), "Input Error: Text is not a string!"
        logging.debug(f"Counting word occurences in the text: {text}")

	word_count = Counter(tokenize(text))

	assert word_counts, "Output Error: Word count dictionary cannot be empty!"
	assert all(isinstance(word, str) for word in word_counts.keys()), "Output Error: All words must be strings."
	assert all(isinstance(count, int) for count in word_counts.values()), "Output Error: All counts must be integers."
	logging.debug(f"Counts for each word: {word_count}")

	return word_count
