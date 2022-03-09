import re

DESCRIPTION_KEY = 'description'

TEXT_KEY = 'text'
TEXT_MARKINGS_KEY = 'textMarkings'

FROM_KEY = 'from'
TO_KEY = 'to'
TYPE_KEY = 'type'
CORRECTIONS_KEY = 'corrections'

TYPO_KEY = 'typo'
LOANWORD_KEY = 'loanword'
STYLISTIC_KEY = 'stylistic'

ORIGIN_KEY = 'origin'
ADAPTATIONS_KEY = 'adaptations'
ALTERNATIVES_KEY = 'alternatives'

ALPHABET = ['a', 'b', 'c', 'ç', 'd', 'dh', 'e', 'ë', 'f', 'g', 'gj', 'h', 'i', 'j', 'k', 'l', 'll', 'm', 'n', 'nj',
            'o', 'p', 'q', 'r', 'rr', 's', 'sh', 't', 'th', 'u', 'v', '	x', 'xh	', 'y', 'z', 'zh']


def fetch_all_words(text):
    return re.findall(r"[\w'-]+", text)


def fetch_all_sentences(text):
    return re.findall(r'["A-Z].*?[.?!…"](?= [A-Z]| $|$)', text)


def flatten_list(lists):
    flattened_list = []
    for element in lists:
        if isinstance(element, list):
            for sub_element in element:
                flattened_list.append(sub_element)
        else:
            flattened_list.append(element)

    return flattened_list
