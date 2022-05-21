import re

from utils.utils import FROM_KEY, DESCRIPTION_KEY, SUGGESTIONS_KEY, TO_KEY, TYPE_KEY, TYPO_KEY, SUBTYPE_KEY, \
    ACTION_KEY, DISPLAY_KEY


# TODO multiple spaces between sentences
def check_for_multiple_subsequent_spaces(sentence, words, sentence_start_index=0):
    markings = []

    # TODO ". = any char except newline." newline...
    MANY_SPACES_FORMAT = r"\s{2,}"

    matches_iter = re.finditer(MANY_SPACES_FORMAT, sentence)

    for match in matches_iter:
        # for i in range(len(words)):  # TODO BST?
        #     word = words[i]
        #     if match.start() > word.end():
        #         left = word.group()
        #         right = words[i + 1].group()
        #         break

        proper_space = sentence[match.start(): match.start() + 1]
        suggestion = {DISPLAY_KEY: sentence[match.start() - 1] + " " + sentence[match.end()], ACTION_KEY: proper_space}
        markings.append(
            {FROM_KEY: sentence_start_index + match.start(), TO_KEY: sentence_start_index + match.end(),
             TYPE_KEY: TYPO_KEY, SUBTYPE_KEY: 'gabim gramatikor, shenja pikësimi',
             DESCRIPTION_KEY: 'hapësira nuk mund të ndiqet nga një ose disa hapësira të tjera',
             SUGGESTIONS_KEY: [suggestion]})
        # TODO match without the characters in .

    return markings


# TODO should be in another file, kept here for now
def drop_multiple_subsequent_spaces(text):
    # TODO dropDoubleOrMoreSpaces
    # there might double or more spaces between sentences
    # TODO actually a marking should be created for this, probably shouldn't do re.sub
    return re.sub(r"  ", r" ", text)  # TODO use \s instead!
