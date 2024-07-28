import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
import platform
import string
from collections import Counter
from text_processor import clean_text


################################################################################
########### DECORATORS ########### DECORATORS ########### DECORATORS ###########
################################################################################

########################################
## DEFINE TEXT FIXTURES AND MISC #######
########################################

# Set the text sample from The Raven
@pytest.fixture
def text():
    return "But the Raven, sitting lonely on the placid bust, spoke only That one word, as if his soul in that one word he did outpour."

# Set the French text sample from Le Corbeau
@pytest.fixture
def french_text():
    return ("Mais le Corbeau, perché solitairement sur ce buste placide, parla "
            "ce seul mot comme si, son âme, en ce seul mot, il la répandait. Je ne "
            "proférai donc rien de plus: il n'agita donc pas de plume--jusqu'à ce "
            "que je fis à peine davantage que marmotter «D'autres amis déjà ont "
            "pris leur vol--demain il me laissera comme mes Espérances déjà ont "
            "pris leur vol.» Alors l'oiseau dit: «Jamais plus.»")

# Set English Text variable
english_text_files = [
        "gutenbooks/pg17192.txt",        # The Raven
        "gutenbooks/pg932.txt",          # Fall of the House of Usher
        "gutenbooks/pg1063.txt",         # Cask of Amontiallado
        "gutenbooks/pg10031.txt"         # The Poems
]

# INSTRUCTION: Use a decorator and write a test for each of your functions against that one text string that is intended to fail on purpose
# Fail decorator
def expected_to_fail(func):
    func = pytest.mark.xfail(func)


########################################
## GRAB TEXTS AND CREATE TEMP DIR ######
########################################

# Session-wide feature to grab texts using the makefile and storing them in a temporary directory
@pytest.fixture(scope="session", autouse=True)
def grab_texts(request):
    # Set the path to the makefile
    makefile_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'makefile')

    # Run 'make get_texts'
    result = subprocess.run(["make", "-f", makefile_path, "get_texts"], capture_output=True, text=True)

    # Print stdout and stderr to enable debugging
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)

    # Throw a stderr if get_texts fails
    if result.returncode != 0:
        pytest.fail(f"get_texts failed: {result.stderr}")

    # Function to remove the temporary books directory
    def remove_gutenbooks_dir():
        try:
            subprocess.run(["rm", "-rf", "gutenbooks"], check=True)
            print("Successfully removed temporary directory: 'gutenbooks'")
        except subprocess.CalledProcessError as error:
            print(f"Failed to remove temporary directory: 'gutenbooks'\nError: {error}")

    # Add a finalizer to remove the temporary gutenbooks directory
    request.addfinalizer(remove_gutenbooks_dir)


########################################
## GRAB ENGLISH TEXTS ##################
########################################

# Grab The Raven
@pytest.fixture
def raven_text(grab_texts):
    with open('gutenbooks/pg17192.txt', 'r') as file:
        return file.read()

# Fixture to handle a parametrized list of files
@pytest.fixture
def read_file():
    def _read_file(filename):
        with open(filename, 'r') as file:
            return file.read()
    return _read_file

# Grab and combine the English Texts
@pytest.fixture
def english_texts():
    combined = ""
    for filename in english_text_files:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                combined += file.read() + " "
    return combined.strip()


################################################################################
######## TEST FUNCTIONS ######## TEST FUNCTIONS ######## TEST FUNCTIONS ########
################################################################################

########################################
## ENGLISH AND GENERAL TESTS ###########
########################################

# INSTRUCTION: Use text and write a test for each of your functions.
# Test of the sample English text from the Raven
def test_cleaner(text):
    # Given a string of text
    # When the string of text is cleaned
    cleaned_text = clean_text(text)

    # Then the expected output should be a lowercase string with no punctuation
    assert isinstance(cleaned_text, str), f"dtype error: Clean Text output is expected a string"
    assert cleaned_text == cleaned_text.lower(), f"Text not cleaned, capital letter found!"
    assert all(x not in string.punctuation for x in cleaned_text), f"Text not cleaned, punctuation found!"

# INSTRUCTION: Use a decorator and write a test for each of your functions against that one text string that is intended to fail on purpose
# Test input type that is expected to fail
@expected_to_fail
def test_cleaner_intended_failure_type():
    # Given an integer instead of a string of text
    # When the cleaner tries to process the integer
    # Then an assertion error should be raised
    with pytest.raises(AssertionError):
        Counter(999)

# INSTRUCTION: Write a test for each of your functions now working against the whole 'The Raven' file
# Test clean_text on the Raven
def test_cleaner_raven(raven_text):
    # Given a string of text
    # When the string of text is cleaned
    cleaned_text = clean_text(raven_text)

    # Then the expected output should be a lowercase string with no punctuation 
    assert isinstance(cleaned_text, str), f"dtype error: Clean Text output is expected a string"
    assert cleaned_text == cleaned_text.lower(), f"Text not cleaned, capital letter found!"
    assert all(x not in string.punctuation for x in cleaned_text), f"Text not cleaned, punctuation found!"

# INSTRUCTION: Expand that, by following the parametrizing procedure in the book so you can pass in the list of files to a test to run each of your English files.
#              I.e. a parameter to the test is a list of the file names, and for each name a test is run independently.
# Test to check function on each English text separately
@pytest.mark.parametrize("filename", english_text_files)
def test_cleaner_english_test_files(filename, read_file):
    # Given a string of text
    english_text = read_file(filename)

    # When the string of text is cleaned
    cleaned_text = clean_text(english_text)

    # Then the expected output should be a lowercase string with no punctuation 
    assert isinstance(cleaned_text, str), f"dtype error: Clean Text output is expected a string"
    assert cleaned_text == cleaned_text.lower(), f"Text not cleaned, capital letter found!"
    assert all(x not in string.punctuation for x in cleaned_text), f"Text not cleaned, punctuation found!"

# INSTRUCTION: Now write a test for ALL the English files together.
# Test to check function on all English texts combined
def test_cleaner_combined(english_texts):
    # Given a string of text
    # When the string of text is cleaned
    cleaned_text = clean_text(english_texts)

    # Then the expected output should be a lowercase string with no punctuation 
    assert isinstance(cleaned_text, str), f"dtype error: Clean Text output is expected a string"
    assert cleaned_text == cleaned_text.lower(), f"Text not cleaned, capital letter found!"
    assert all(x not in string.punctuation for x in cleaned_text), f"Text not cleaned, punctuation found!"


########################################
## NON-ENGLISH TESTS ###################
########################################

# INSTRUCTION: Finally, write a test for Le Corbeau for each of your functions using the following as the text
# Test to check function on Le Corbeau text
def test_cleaner_french(french_text):
    # Given a string of text
    # When the string of text is cleaned
    cleaned_text = clean_text(french_text)

    # Then the expected output should be a lowercase string with no punctuation 
    assert isinstance(cleaned_text, str), f"dtype error: Clean Text output is expected a string"
    assert cleaned_text == cleaned_text.lower(), f"Text not cleaned, capital letter found!"
    assert all(x not in string.punctuation for x in cleaned_text), f"Text not cleaned, punctuation found!"

# INSTRUCTION: use the skip decorator for a test that hypothetically is expected to pass but can't be run, say we will eventually run a Japanese version but we are not ready yet
# Test for future Japanese version that is marked to be skipped
@pytest.mark.skip(reason="Japanese version in development")
def test_cleaner_japanese():
    # Given a Japanese text
    japanese_text = "insert Japanese text here"

    # When the string of text is cleaned
    cleaned_text = clean_text(japanese_text)

    # Then the expected output should be a lowercase string with no punctuation 
    assert isinstance(cleaned_text, str), f"dtype error: Clean Text output is expected a string"
    assert cleaned_text == cleaned_text.lower(), f"Text not cleaned, capital letter found!"
    assert all(x not in string.punctuation for x in cleaned_text), f"Text not cleaned, punctuation found!"

# INSTRUCTION: Make a test continional on your OS, so if the tests are run on a different OS they fail to warn you have not tested on that OS.
# Test if the current user OS is supported
def test_os():
    # Given the user os and a list of os that are supported
    user_os = platform.system()
    supported_os = ["Linux"]

    # When comparing the two
    # Then the user os should be in the list of os that are supported
    if user_os not in supported_os:
        pytest.fail(f"OS: {user_os} is not currently supported. Use one of the following OS: {supported_os}")
    else:
        assert True

# INSTRUCTION: Make a similar test for the version of python used when running the tests
# Test if the current user Python version is supported
def test_python_version():
    # Given the the user version and the minimum and maximum Python versions that are supported
    user_version = sys.version_info[:2]
    min_version = (3, 7)
    max_version = (3, 12)

    # When comparing the two
    # Then the user version must be within the min and max Python versions
    if not (min_version <= user_version <= max_version):
        pytest.fail(f"Python Version: {user_version} is not currently supported. Use a version >={min_version} or <={max_version}.")
        assert True

# INSTRUCTION: Write a test that uses bash/linux to get a result on a test string and compare it against your functions. The function should pass if the results are the same.
# Test to compare function against bash command
def test_bash_vs_clean_text(text):
    # Given a string of text using function
    function_cleaned_text = clean_text(text)

    # When a Bash command is used to clean the string of text
    bash_command = f'echo "{text}" | tr "[:upper:]" "[:lower:]" | tr -d "[:punct:]"'
    bash_output = subprocess.run(bash_command, shell=True, capture_output=True, text=True)
    bash_cleaned_text = bash_output.stdout.strip()

    # Then the Bash and Function counts should be the same
    assert function_cleaned_text == bash_cleaned_text, f"Bash Cleaned Text: {bash_cleaned_text} != Function Cleaned Text: {function_cleaned_text}"
