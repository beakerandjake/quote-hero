import os
from random import randrange

# expect a words file to exist in the data dir.
words_file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "words.txt"
)


def random_word():
    """Returns a random words from the words file"""
    result = None
    with open(words_file_path) as words_file:
        for i, word in enumerate(words_file, start=1):
            if randrange(i) == 0:
                result = word.strip()
    return result


if __name__ == "__main__":
    print(random_word())
