import json
import pickle
from random import shuffle

from utils.utils import fetch_all_words, TEXT_KEY, TEXT_MARKINGS_KEY, FROM_KEY, TYPE_KEY, \
    DESCRIPTION_KEY, CORRECTIONS_KEY, TO_KEY, TYPO_KEY, ALTERNATIVES_KEY, ORIGIN_KEY, LOANWORD_KEY, ADAPTATIONS_KEY, \
    flatten_list

# the following initialization code will be polished when a proper deployment machine is available

LOANWORDS = None
if LOANWORDS is None:
    print('loading the loanwords')
    with open('static/loanwords.json', 'rb') as file:
        LOANWORDS = json.load(file)
else:
    print('the loanwords are already loaded')

ADAPTATIONS_OF_LOANWORDS = [adaptation for loanword in LOANWORDS for adaptation in loanword[ADAPTATIONS_KEY]]

DICTIONARY = None
DELETES_DICTIONARY = None
if DICTIONARY is None and DELETES_DICTIONARY is None:
    print('loading the pickles')
    with open('static/standalones.pickle', 'rb') as file:
        DICTIONARY = pickle.load(file)

    with open('static/deletes.pickle', 'rb') as file:
        DELETES_DICTIONARY = pickle.load(file)
else:
    print('the pickles are already loaded')


def generate_markings(text, max_corrs=5):
    # There's currently an ongoing implicit gentleman's agreement to not deliberately spam the server. If broken, this
    # (and additional measures in this vein) will be enabled.
    # if len(text) > 5000:
    #     raise ValueError('exceedingly large text')

    all_written_words = fetch_all_words(text)

    # import pyink
    # async calls, these might have precedence over each other, attempt to split in different endpoints later on
    # highlighted_loanwords = pyink.spelling.checkForLoanwords(text)
    # highlighted_typos = pyink.spelling.correctTypos(text)
    # highlighted_stylistics = pyink.spelling.generateStylisticChanges(text)

    content = {TEXT_KEY: text, TEXT_MARKINGS_KEY: []}

    word_index = 0
    char_index = 0
    while char_index < len(text):
        if word_index >= len(all_written_words):  # e.g. for texts with added spaces at the end
            break

        incoming_word = all_written_words[word_index]

        if text[char_index] == incoming_word[0]:
            from_index = char_index
            to_index = char_index + 1
            char_index += 1
            other_index = 1

            if other_index == len(incoming_word):
                word_index += 1
                char_index += 1
                continue

            while text[char_index] == incoming_word[other_index]:
                char_index += 1
                other_index += 1
                to_index += 1

                if other_index == len(incoming_word):
                    word_index += 1
                    break

            if other_index == len(incoming_word):
                if incoming_word[0].isdigit():  # ignore numbers
                    char_index += 1
                    continue

                # words beginning with an uppercase letter are skipped (should they?), what about all uppercase words?
                if incoming_word[0].isupper():
                    char_index += 1
                    continue

                if is_loanword(incoming_word):
                    loanword_details = get_loanword_details(incoming_word)
                    content[TEXT_MARKINGS_KEY].extend([
                        {FROM_KEY: from_index, TO_KEY: to_index,
                         TYPE_KEY: LOANWORD_KEY,
                         DESCRIPTION_KEY: 'huazim jo i standardizuar, ' + loanword_details[ORIGIN_KEY],
                         CORRECTIONS_KEY: loanword_details[ALTERNATIVES_KEY]}])
                else:
                    corrections = top_n_corrections(incoming_word, max_corrs)
                    if corrections:
                        content[TEXT_MARKINGS_KEY].extend([
                            {FROM_KEY: from_index, TO_KEY: to_index, TYPE_KEY: TYPO_KEY,
                             DESCRIPTION_KEY: 'gabim gramatikor, drejtshkrim',
                             CORRECTIONS_KEY: corrections}])

        if word_index == len(all_written_words):
            break

        char_index += 1
    return content


def is_loanword(word):
    return word in ADAPTATIONS_OF_LOANWORDS


def get_loanword_details(word):
    loanword_details = list(filter(lambda loanword: word in loanword[ADAPTATIONS_KEY], LOANWORDS))

    if len(loanword_details) > 1:
        raise ValueError('we encountered a word that was adapted the same across different loanwords')

    return loanword_details[0]


def top_n_corrections(word, n=-1):
    corrections = []
    if word in DICTIONARY:  # correct word, besa -> besa
        return corrections
    else:
        word_deletes = generate_deletes_of_word(word)

        word_deletes_keys = list(word_deletes.keys())

        if word in DELETES_DICTIONARY:  # missing character, bea -> besa
            corrections.extend(DELETES_DICTIONARY[word])

        some_suggs = []  # redundant characters, bbesa -> besa
        for w in word_deletes_keys:
            if w in DICTIONARY:
                some_suggs.append(w)
        corrections.extend(flatten_list(some_suggs))

        other_suggs = []  # incorrect characters, gesa -> besa
        for w in word_deletes_keys:
            if w in DELETES_DICTIONARY:
                other_suggs.append(DELETES_DICTIONARY[w])
        corrections.extend(flatten_list(other_suggs))

        if not corrections:
            pass  # hmm, probably doesn't exist

    shuffle(corrections)  # as context is not relevant to the current algorithm
    return corrections if n == -1 else corrections[:n]


def generate_deletes_of_word(word):
    """does not include the original word"""
    deletes = {}
    for i in range(len(word)):
        deletes[word[:i] + word[i + 1:]] = [word]
    return deletes


def generate_deletes_of_words(words):
    deletes = {}

    for word in words:
        word_deletes = generate_deletes_of_word(word)
        for k in word_deletes.keys():
            if k in deletes:
                deletes[k].extend(word_deletes[k])
            else:
                deletes[k] = word_deletes[k]

    return deletes
