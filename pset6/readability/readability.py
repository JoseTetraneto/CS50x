from cs50 import get_string

# Runs the main program


def main():
    text = get_string("input text: ")
    i = index(count_letters(text), count_words(text), count_sentences(text))

    if i < 16 and i >= 1:
        print("Grade", int(round(i)))
    elif i >= 16:
        print("Grade 16+")
    else:
        print("Before Grade 1")
    return 0

# Creates function to count the amount of letters


def count_letters(t):
    letters_count = 0
    for i in range(len(t)):
        if t[i].islower() is True:
            letters_count += 1
        elif t[i].isupper() is True:
            letters_count += 1
        else:
            continue
    return letters_count

# Creates function to count the amount of words


def count_words(t):
    words_count = 0
    for i in range(len(t)):
        if t[i].isspace() is True:
            words_count += 1
    return words_count + 1

# Creates function to count the amount of sentences


def count_sentences(t):
    sentences_count = 0
    for i in range(len(t)):
        if t[i] is '.' or t[i] is '!' or t[i] is '?':
            sentences_count += 1
    return sentences_count

# Creates function to return Coleman-Liau index


def index(l, w, s):
    a = 100 / w
    index = 0.0588 * (l * a) - 0.296 * (s * a) - 15.8
    return index


main()