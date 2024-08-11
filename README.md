[![Python package](https://github.com/austin-t-rivera/atr8ec_DS5111su24_lab_01/actions/workflows/validations.yml/badge.svg)](https://github.com/austin-t-rivera/atr8ec_DS5111su24_lab_01/actions/workflows/validations.yml)
# README

## text_processor.py
The text_processor.py module contains three fucntions that process a string of string to either clean, tokenize, or count:  

### clean_text(text)
`Function`: Cleans string of text by making all letters lowercase and removing all punctuation characters. <br>
`Example Input`: clean_text("Hello world! The World says, 'hi'.") <br>
`Example Output`: "hello world the world says hi" <br>

### tokenize(text)
`Function`: Utilizes clean_text() to clean a string of text and then splits the cleaned text into a list of strings. <br>
`Example Input`: tokenize("Hello world! The World says, 'hi'.") <br>
`Example Output`: ["hello", "world", "the", "world", "says", "hi"] <br>

### count_words(text)  
`Function`: Utilizes tokenize to clean and split a string of text into tokens, then counts the frequency of each token, returning a dictionary of tokens and counts. <br>
`Example Input`: count_words("Hello world! The World says, 'hi'.") <br>
`Example Output`: {"hello":1, "world":2, "the":1, "says":1, "hi":1} <br>
