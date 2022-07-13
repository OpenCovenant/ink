import json
import os
import pickle
import re
from random import shuffle

from marking.ec_specials import generate_ec_permutations
from marking.grammar_rules.overly_long_sentence_rule import check_for_overly_long_sentence
from marking.grammar_rules.written_date_rule import check_for_a_written_date_rule
from marking.multiple_subsequent_spaces import check_for_multiple_subsequent_spaces
from marking.grammar_rules.comma_rules import check_for_comma_before_or_and_rule, check_for_a_nonspace_after_comma
from utils.utils import TEXT_KEY, TEXT_MARKINGS_KEY, FROM_KEY, TYPE_KEY, DESCRIPTION_KEY, TO_KEY, \
    TYPO_KEY, ALTERNATIVES_KEY, ORIGIN_KEY, LOANWORD_KEY, flatten_list, SUGGESTIONS_KEY, ACUTE_ACCENTS, \
    SUBTYPE_KEY, fetch_sentence_iterator, DISPLAY_KEY, ACTION_KEY, skim_text, fetch_word_iterator

# the following initialization code will be polished when a proper deployment machine is available

LOANWORDS = None
if LOANWORDS is None:
    path = 'static/loanwords.json'
    if os.path.exists(path):
        print('loading the loanwords')
        with open('static/loanwords.json', 'rb') as file:
            LOANWORDS = json.load(file)
    else:
        print('no loanwords were found, initializing to empty')
        LOANWORDS = {}
else:
    print('the loanwords are already loaded')

ADAPTATIONS_OF_LOANWORDS = list(LOANWORDS)

DICTIONARY = None
DELETES_DICTIONARY = None
if DICTIONARY is None and DELETES_DICTIONARY is None:
    dictionary_path = 'static/standalones.pickle'
    if os.path.exists(dictionary_path):
        print('loading the standalone pickle')
        with open(dictionary_path, 'rb') as file:
            DICTIONARY = pickle.load(file)
    else:
        print('no dialectisms were found, initializing to empty')
        DICTIONARY = []

    dictionary_deletes_path = 'static/deletes.pickle'
    if os.path.exists(dictionary_path):
        print('loading the standalone deletions pickle')
        with open(dictionary_deletes_path, 'rb') as file:
            DELETES_DICTIONARY = pickle.load(file)
    else:
        print('no dialectisms were found, initializing to empty')
        DELETES_DICTIONARY = []
else:
    print('the pickles are already loaded')

DIALECTISMS = None
if DIALECTISMS is None:
    path = 'static/dialectisms.pickle'
    if os.path.exists(path):
        print('loading the dialectisms')
        with open(path, 'rb') as file:
            DIALECTISMS = pickle.load(file)
    else:
        print('no dialectisms were found, initializing to empty')
        DIALECTISMS = []
else:
    print('the dialectisms are already loaded')

LATIN_WORDS = None
if LATIN_WORDS is None:
    path = 'static/latin_words.pickle'
    if os.path.exists(path):
        print('loading the latin words')
        with open(path, 'rb') as file:
            LATIN_WORDS = pickle.load(file)
    else:
        print('no latin words were found, initializing to empty')
        LATIN_WORDS = []
else:
    print('the latin words are already loaded')


def generate_markings(text, max_suggestions=-1):
    # There's currently an ongoing implicit gentleman's agreement to not deliberately spam the server. If broken, this
    # (and additional measures in this vein) will be enabled.
    # if len(text) > 5000:
    #     raise ValueError('exceedingly large text')

    # import pyink
    # async calls, these might have precedence over each other, attempt to split in different endpoints later on
    # highlighted_loanwords = pyink.spelling.checkForLoanwords(text)
    # highlighted_typos = pyink.spelling.correctTypos(text)
    # highlighted_stylistics = pyink.spelling.generateStylisticChanges(text)

    content = {TEXT_KEY: text, TEXT_MARKINGS_KEY: []}

    word_markings = iterate_words(text, max_suggestions)
    sentence_markings = iterate_sentences(text)

    content[TEXT_MARKINGS_KEY].extend(word_markings)
    content[TEXT_MARKINGS_KEY].extend(sentence_markings)

    return content


def iterate_sentences(text):
    markings = []

    for sentence_match in fetch_sentence_iterator(text):
        sentence = sentence_match.group()
        sentence_start_index = sentence_match.start()
        words = list(fetch_word_iterator(sentence))

        # # TODO
        # comma_markings = check_for_a_comma_rule(text, sentence, sentence_start_index)
        # markings.extend(comma_markings)

        other_comma_markings = check_for_comma_before_or_and_rule(text, sentence, sentence_start_index)
        markings.extend(other_comma_markings)

        more_comma_markings = check_for_a_nonspace_after_comma(sentence, sentence_start_index)
        markings.extend(more_comma_markings)

        # TODO
        overly_long_markings = check_for_overly_long_sentence(sentence, sentence_start_index)
        markings.extend(overly_long_markings)

        date_markings = check_for_a_written_date_rule(sentence, sentence_start_index)
        markings.extend(date_markings)

        # TODO
        # more_date_markings = check_for_another_written_date_rule(sentence, sentence_start_index)
        # markings.extend(more_date_markings)

        multiple_subsequent_spaces_markings = check_for_multiple_subsequent_spaces(sentence, words,
                                                                                   sentence_start_index)
        markings.extend(multiple_subsequent_spaces_markings)

    return markings


def map_To_Albanian(loanword_type):
    loanword_types_map = {'ottoman': 'otoman', 'greek': 'grek', 'slavic': 'sllav', 'english': 'anglisht'}

    return loanword_types_map[loanword_type] if loanword_type in loanword_types_map else loanword_type


def iterate_words(text, limit):
    markings = []

    skippable_intervals = skim_text(text)

    char_index = 0
    while char_index < len(text):
        if skippable_intervals:
            if char_index == skippable_intervals[0][0]:
                char_index = skippable_intervals[0][1]
                skippable_intervals.popleft()
                continue

        if re.match(r"[\w'-]", text[char_index]):
            from_index = char_index
            to_index = char_index + 1
            char_index += 1

            while char_index < len(text) and re.match(r"[\w'-]", text[char_index]):
                char_index += 1
                to_index += 1

            word = text[from_index: to_index]

            if is_word_skippable(word):  # TODO might be integrated into the skippable intervals
                char_index += 1
                continue

            if is_loanword(word):
                loanword_details = get_loanword_details(word)
                markings.append({FROM_KEY: from_index, TO_KEY: to_index, TYPE_KEY: LOANWORD_KEY,
                                 SUBTYPE_KEY: 'huazim ' + map_To_Albanian(loanword_details[ORIGIN_KEY]),
                                 DESCRIPTION_KEY: 'zëvendësime në shqip për ' + word + ' janë',
                                 SUGGESTIONS_KEY: [{DISPLAY_KEY: lw, ACTION_KEY: lw} for lw in
                                                   loanword_details[ALTERNATIVES_KEY]]})
            else:
                corrections = top_suggestions(word, limit)
                if corrections:
                    markings.append(
                        {FROM_KEY: from_index, TO_KEY: to_index, TYPE_KEY: TYPO_KEY,
                         SUBTYPE_KEY: 'gabim gramatikor, drejtshkrim',
                         DESCRIPTION_KEY: 'kjo fjalë nuk ekziston, a doje të shkruaje',
                         SUGGESTIONS_KEY: corrections})

        char_index += 1

    return markings


def has_accent(word):
    return any([True if c in ACUTE_ACCENTS else False for c in word])


def is_Latin(word):
    return word in LATIN_WORDS


def is_dialectism(word):
    return word in DIALECTISMS


def has_numbers(word):
    return any(map(str.isdigit, word))


def has_uppercase_letters(word):
    return any(map(str.isupper, word))


def is_word_skippable(word):
    # ignore words containing any uppercase letter
    if has_uppercase_letters(word):
        return True

    # ignore words containing any number
    if has_numbers(word):
        return True

    return is_Latin(word) or is_dialectism(word) or has_accent(word)


def is_loanword(word):
    return word in ADAPTATIONS_OF_LOANWORDS


def get_loanword_details(word):
    return LOANWORDS[word]


def top_suggestions(word, limit=-1):
    suggestions = []
    if word in DICTIONARY:  # correct word, besa -> besa
        return suggestions
    else:
        if word in LATIN_WORDS:
            return suggestions

        word_deletes = generate_deletes_of_word(word)

        word_deletes_keys = list(word_deletes.keys())

        if word in DELETES_DICTIONARY:  # missing character, bea -> besa
            suggestions.extend(DELETES_DICTIONARY[word])

        some_suggestions = []  # redundant characters, bbesa -> besa
        for w in word_deletes_keys:
            if w in DICTIONARY:
                some_suggestions.append(w)
        suggestions.extend(flatten_list(some_suggestions))

        other_suggestions = []  # incorrect characters, gesa -> besa
        for w in word_deletes_keys:
            if w in DELETES_DICTIONARY:
                other_suggestions.append(DELETES_DICTIONARY[w])
        suggestions.extend(flatten_list(other_suggestions))

        if 'e' in word or 'c' in word:  # missing ë or ç, qenesishem -> qenësishëm
            ec_suggestions = generate_ec_permutations(word)
            ec_suggestions = list(filter(lambda ecs: ecs not in suggestions and ecs in DICTIONARY, ec_suggestions))
            suggestions.extend(ec_suggestions)

        if not suggestions:
            pass  # hmm, probably doesn't exist

    # TODO hotfix, perhaps by definition some of the above checks produce duplicates, properly address
    suggestions = list(set(suggestions))

    shuffle(suggestions)  # as context is not relevant to the current algorithm
    suggestions = [{DISPLAY_KEY: s, ACTION_KEY: s} for s in suggestions]
    return suggestions if limit == -1 else suggestions[:limit]


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
        for k in word_deletes:
            if k in deletes:
                deletes[k].extend(word_deletes[k])
            else:
                deletes[k] = word_deletes[k]

    return deletes
