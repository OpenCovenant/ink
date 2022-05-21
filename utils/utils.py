import json
import os
import re
from itertools import chain

DESCRIPTION_KEY = 'description'

TEXT_KEY = 'text'
TEXT_MARKINGS_KEY = 'textMarkings'

FROM_KEY = 'from'
TO_KEY = 'to'
TYPE_KEY = 'type'
SUBTYPE_KEY = 'subtype'
SUGGESTIONS_KEY = 'suggestions'
DISPLAY_KEY = 'display'
ACTION_KEY = 'action'

TYPO_KEY = 'typo'
LOANWORD_KEY = 'loanword'
STYLISTIC_KEY = 'stylistic'

ORIGIN_KEY = 'origin'
ADAPTATIONS_KEY = 'adaptations'
ALTERNATIVES_KEY = 'alternatives'

ALPHABET = ['a', 'b', 'c', 'ç', 'd', 'dh', 'e', 'ë', 'f', 'g', 'gj', 'h', 'i', 'j', 'k', 'l', 'll', 'm', 'n', 'nj',
            'o', 'p', 'q', 'r', 'rr', 's', 'sh', 't', 'th', 'u', 'v', '	x', 'xh	', 'y', 'z', 'zh']

bashketingellore_e_shurdhet = ['f', 'k', 'p', 'q', 't', 'th']
bashketingellore_e_zeshme = ['b', 'd', 'dh' 'g', 'gj', 'v', 'x', 'xh', 'z', 'zh']
bashketingellore_e_tingullt = ['l', 'll', 'r', 'rr', 'm', 'n', 'nj', 'j']

# theks i mprehte
ACUTE_ACCENTS = ['á', 'é', 'í', 'ó', 'ú']

ABBREVIATIONS = None
if ABBREVIATIONS is None:
    print('loading the abbreviations')
    path = 'static/abbreviations.json'
    if os.path.exists(path):
        with open(path, 'rb') as file:
            ABBREVIATIONS = [abbreviation for abbreviation in json.load(file)]
    else:
        print('no dialectisms were found, initializing to empty')
        ABBREVIATIONS = []
else:
    print('the abbreviations are already loaded')


def fetch_all_words(text):
    return re.findall(r"[\w'-]+", text)


def fetch_word_iterator(text):
    return re.finditer(r"[\w'-]+", text)


def fetch_sentence_iterator(text):
    return re.finditer(r'["A-ZÇË].*?[.?!…"](?=[\r\n\s]+[A-ZÇË]|[\r\n\s]+$|$)', text)
    # return re.finditer(r'["A-Z].*?[.?!…"](?= [A-Z]| $|$)', text)


def fetch_email_iterator(text):
    return re.finditer(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", text)


def fetch_abbreviation_iterator(text):
    abbreviation_iterator = re.finditer(r'(?:[a-zA-Z]+\.)+(?![\r\n\s]+$)', text)
    abbreviation_iterator = filter(lambda abbreviation_match: abbreviation_match.group() in ABBREVIATIONS,
                                   abbreviation_iterator)
    return abbreviation_iterator


def fetch_link_iterator(text):
    return re.finditer(
        r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})",
        text)


def fetch_hashtag_iterator(text):
    """kane numra hashtags?"""
    # return re.finditer(r"#[a-zA-z]+", text)
    # return re.finditer(r"#\w", text)  # TODO why +?
    return re.finditer(r"#\w+", text)


def fetch_quoted_texts_iterator(text):
    # TODO improve
    return chain(re.finditer(r'"(.+?)"', text), re.finditer(r'“(.+?)”', text), re.finditer(r'„(.+?)“', text),
                 re.finditer(r'‘(.+?)’', text), re.finditer(r'«(.+?)»', text))


# TODO remove?
# def drop_all_links(text):
#     return re.finditer(
#         r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})",
#         text)


def merge_overlapping_intervals():
    pass


def skim_text(text):
    """text parts to be ignored"""
    # drop emails, URLs, quoted text (including quotes)

    email_intervals = fetch_email_iterator(text)
    url_intervals = fetch_link_iterator(text)
    quoted_text_intervals = fetch_quoted_texts_iterator(text)
    hashtags_intervals = fetch_hashtag_iterator(text)
    abbreviations_intervals = fetch_abbreviation_iterator(text)

    skimming_iterator = chain(email_intervals, url_intervals, quoted_text_intervals, hashtags_intervals,
                              abbreviations_intervals)

    skippable_intervals = []

    # TODO streamline the following two lines with the call to the "merge" method
    for match in skimming_iterator:
        skippable_intervals.append([match.start(), match.end()])

    skippable_intervals = merge(skippable_intervals)

    # skippable_intervals = merge_overlapping_intervals(skippable_intervals)

    return skippable_intervals


# def merge_overlapping_intervals(intervals):
#     intervals.sort()
#
#     merged_intervals = []
#
#     for i in range(len(intervals) - 1):
#         if intervals[i][0] ... some logic
#
#     pass


def merge(intervals):
    from collections import deque
    merged_intervals = deque([])
    for interval in sorted(intervals, key=lambda v: v[0]):
        if merged_intervals and interval[0] <= merged_intervals[-1][1]:
            merged_intervals[-1][1] = max(merged_intervals[-1][1], interval[1])
        else:
            merged_intervals.append(interval),
    return merged_intervals


def flatten_list(lists):
    flattened_list = []
    for element in lists:
        if isinstance(element, list):
            for sub_element in element:
                flattened_list.append(sub_element)
        else:
            flattened_list.append(element)

    return flattened_list
