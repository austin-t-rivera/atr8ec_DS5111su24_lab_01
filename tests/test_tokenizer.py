import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
import platform
from text_processor import clean_text, tokenize


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
def test_tokenizer(text):
    # Given a string of text
    # When the string of text is tokenized
    tokens = tokenize(text)

    # Then the expected output should be a list of cleaned strings
    assert isinstance(tokens, list), f"dtype error: Tokenizer output is expected to be a list"
    assert tokens == clean_text(text).split(), f"Text was not split properly"
    assert tokens == ['but','the', 'raven', 'sitting', 'lonely', 'on', 'the', 'placid',
                      'bust', 'spoke', 'only', 'that', 'one', 'word', 'as', 'if', 'his', 'soul',
                      'in', 'that', 'one', 'word', 'he', 'did', 'outpour']


# INSTRUCTION: Use a decorator and write a test for each of your functions against that one text string that is intended to fail on purpose
# Test of the input type that is expected to fail
@expected_to_fail
def test_tokenizer_intended_failure_type():
    # Given an integer instead of a string of text
    # When the tokenizer tries to process the integer
    # Then an assertion error should be raised
    with pytest.raises(AssertionError):
        tokenize(999)

# INSTRUCTION: Write a test for each of your functions now working against the whole 'The Raven' file
# Test to check function on just the Raven
def test_tokenizer_raven(raven_text):
    # Given a string of text
    # When the string of text is tokenized
    tokens = tokenize(raven_text)

    # Then the expected output should be a list of cleaned strings
    assert isinstance(tokens, list), f"dtype error: Tokenizer output is expected to be a list"
    assert tokens == clean_text(raven_text).split(" "), f"Text was not split properly"

# INSTRUCTION: Expand that, by following the parametrizing procedure in the book so you can pass in the list of files to a test to run each of your English files.
#              I.e. a parameter to the test is a list of the file names, and for each name a test is run independently.
# Test to check function on each English text separately
@pytest.mark.parametrize("filename", english_text_files)
def test_tokenizer_english_test_files(filename, read_file):
    # Given the text from a file
    # When the string of text from the file is tokenized
    tokens = tokenize(filename)

    # Then the expected output should be a list of cleaned strings
    assert isinstance(tokens, list), f"dtype error: Tokenizer output is expected to be a list"
    assert tokens == clean_text(filename).split(" "), f"Text was not split properly"

# INSTRUCTION: Now write a test for ALL the English files together.
# Test to check function on all English texts combined
def test_tokenizer_combined(english_texts):
    # Given a text string
    # When the string of text is tokenized
    tokens = tokenize(english_texts)

    # Then the expected output should be a list of cleaned strings
    assert isinstance(tokens, list), f"dtype error: Tokenizer output is expected to be a list"
    assert tokens == clean_text(english_texts).split(" "), f"Text was not split properly"


########################################
## NON-ENGLISH TESTS ###################
########################################

# INSTRUCTION: Finally, write a test for Le Corbeau for each of your functions using the following as the text
# Test to check function on Le Corbeau text
def test_tokenizer_french(french_text):
    # Given a text string
    # When the string of text is tokenized
    tokens = tokenize(french_text)

    # Then the expected output should be a list of cleaned strings
    assert isinstance(tokens, list), f"dtype error: Tokenizer output is expected to be a list"
    assert tokens == clean_text(french_text).split(" "), f"Text was not split properly"

# INSTRUCTION: use the skip decorator for a test that hypothetically is expected to pass but can't be run, say we will eventually run a Japanese version but we are not ready yet
# Test for future Japanese version that is marked to be skipped
@pytest.mark.skip(reason="Japanese version in development")
def test_tokenizer_japanese():
    # Given a Japanese text
    japanese_text = "insert Japanese text here"

    # When the string of text is tokenized
    tokens = tokenize(japanese_text)

    # Then the expected output should be a list of cleaned strings
    assert isinstance(tokens, list), f"dtype error: Tokenizer output is expected to be a list"
    assert tokens == clean_text(japanese_text).split(" "), f"Text was not split properly"

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
def test_bash_vs_tokenize(text):
    # Given a string of text using function
    function_tokens = tokenize(text)

    # When a Bash command is used to clean a string of text and then tokenize
        # Clean string of text
    bash_command = f'echo "{text}" | tr "[:upper:]" "[:lower:]" | tr -d "[:punct:]" | tr " " "\n"'
    bash_output = subprocess.run(bash_command, shell=True, capture_output=True, text=True)
        # Tokenize the cleaned string
    bash_tokens = bash_output.stdout.strip().split("\n")


    # Then the Bash and Function tokens should be the same
    assert function_tokens == bash_tokens, f"Bash Tokens: {bash_tokens} != Function Tokens: {function_tokens}"
