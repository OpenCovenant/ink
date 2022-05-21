import re

from utils.utils import TO_KEY, FROM_KEY, SUGGESTIONS_KEY, DESCRIPTION_KEY, TYPE_KEY, TYPO_KEY, SUBTYPE_KEY, \
    fetch_all_words, DISPLAY_KEY, ACTION_KEY


def check_for_a_comma_rule(text, sentence, sentence_start_index=0):
    markings = []
    SUBTYPE_VALUE = 'gabim gramatikor, shenja pikësimi'
    DESCRIPTION_VALUE = 'vendoset presje mes gjymtyrëve homogjene që bashkohen nga lidhëza dyshe '

    # TODO
    # words = fetch_all_words(sentence)

    # jo vetëm ..., por edhe ...
    if -1 < sentence.find('jo vetëm') < sentence.find('por edhe') \
            and sentence[sentence.find('por edhe') - 2] != ',':
        suggestion = {DISPLAY_KEY: "... " + text[sentence.find('por edhe') - 9:sentence.find(
            'por edhe') - 1] + ", por edhe ...", ACTION_KEY: ''}
        markings.append(
            {FROM_KEY: sentence_start_index, TO_KEY: sentence_start_index + len(sentence), TYPE_KEY: TYPO_KEY,
             SUBTYPE_KEY: SUBTYPE_VALUE,
             DESCRIPTION_KEY: DESCRIPTION_VALUE + '"jo vetëm ..., por edhe ..."',
             SUGGESTIONS_KEY: [suggestion]})

    # jo vetëm ..., po as ...
    if -1 < sentence.find('jo vetëm') < sentence.find('po as') and sentence[sentence.find('po as') - 2] != ',':
        suggestion = {DISPLAY_KEY: "... " + text[sentence.find('po as') - 6:sentence.find('po as') - 1] + ", po as ...",
                      ACTION_KEY: ''}
        markings.append(
            {FROM_KEY: sentence_start_index, TO_KEY: sentence_start_index + len(sentence), TYPE_KEY: TYPO_KEY,
             SUBTYPE_KEY: SUBTYPE_VALUE,
             DESCRIPTION_KEY: DESCRIPTION_VALUE + '"jo vetëm ..., po as ..."',
             SUGGESTIONS_KEY: [suggestion]})

    # jo vetëm ..., po as edhe ...
    if -1 < sentence.find('jo vetëm') < sentence.find('po as edhe') \
            and sentence[sentence.find('po as edhe') - 2] != ',':
        suggestion = {DISPLAY_KEY: "... " + text[sentence.find('po as edhe') - 11:sentence.find(
            'po as edhe') - 1] + ", po edhe ...", ACTION_KEY: ''}
        markings.append(
            {FROM_KEY: sentence_start_index, TO_KEY: sentence_start_index + len(sentence), TYPE_KEY: TYPO_KEY,
             SUBTYPE_KEY: SUBTYPE_VALUE,
             DESCRIPTION_KEY: DESCRIPTION_VALUE + '"jo vetëm ..., po as edhe ..."',
             SUGGESTIONS_KEY: [suggestion]})

    # si ..., ashtu ...
    if -1 < sentence.find('si') < sentence.find('ashtu') and sentence[sentence.find('ashtu') - 2] != ',':
        suggestion = {DISPLAY_KEY: "... " + text[sentence.find('ashtu') - 5:sentence.find('ashtu') - 1] + ", ashtu ...",
                      ACTION_KEY: ''}
        markings.append(
            {FROM_KEY: sentence_start_index, TO_KEY: sentence_start_index + len(sentence), TYPE_KEY: TYPO_KEY,
             SUBTYPE_KEY: SUBTYPE_VALUE,
             DESCRIPTION_KEY: DESCRIPTION_VALUE + '"si ..., ashtu ..."',
             SUGGESTIONS_KEY: [suggestion]})

    # si ..., edhe ...
    if -1 < sentence.find('si') < sentence.find('edhe') and sentence[sentence.find('edhe') - 2] != ',':
        suggestion = {DISPLAY_KEY: "... " + text[sentence.find('edhe') - 5:sentence.find('edhe') - 1] + ", edhe ...",
                      ACTION_KEY: ''}
        markings.append(
            {FROM_KEY: sentence_start_index, TO_KEY: sentence_start_index + len(sentence), TYPE_KEY: TYPO_KEY,
             SUBTYPE_KEY: SUBTYPE_VALUE,
             DESCRIPTION_KEY: DESCRIPTION_VALUE + '"si ..., edhe ..."',
             SUGGESTIONS_KEY: [suggestion]})

    # sa ..., aq edhe ...
    if -1 < sentence.find('sa') < sentence.find('aq edhe') and sentence[sentence.find('aq edhe') - 2] != ',':
        suggestion = {DISPLAY_KEY: "... " + text[sentence.find('aq edhe') - 8:sentence.find(
            'aq edhe') - 1] + ", aq edhe ...", ACTION_KEY: ''}
        markings.append(
            {FROM_KEY: sentence_start_index, TO_KEY: sentence_start_index + len(sentence), TYPE_KEY: TYPO_KEY,
             SUBTYPE_KEY: SUBTYPE_VALUE,
             DESCRIPTION_KEY: DESCRIPTION_VALUE + '"sa ..., aq edhe ..."',
             SUGGESTIONS_KEY: [suggestion]})

    return markings


def check_for_comma_before_or_and_rule(text, sentence, sentence_start_index=0):
    markings = []

    # words = fetch_all_words(sentence)
    # TODO, fetch all words, "ose" and "edhe" have to be adjacent and separated by a space

    if sentence.find('ose edhe') > -1 and sentence[sentence.find('ose edhe') - 2] != ',':
        suggestion = {DISPLAY_KEY: "... " + text[sentence.find('ose edhe') - 9:sentence.find(
            'ose edhe') - 1] + ", ose edhe ...", ACTION_KEY: ''}
        markings.append(
            {FROM_KEY: sentence_start_index, TO_KEY: sentence_start_index + len(sentence), TYPE_KEY: TYPO_KEY,
             SUBTYPE_KEY: 'gabim gramatikor, shenja pikësimi',
             DESCRIPTION_KEY: 'vendoset presje mes gjymtyrëve homogjene që bashkohen me lidhëzën veçuese "ose" të'
                              ' ndjekur nga pjëseza përforcuese "edhe"',
             SUGGESTIONS_KEY: [suggestion]})

        # TODO sentence.find('ose edhe') there might be repeating occurrences, utilize finditer

    return markings


def check_for_a_nonspace_after_comma(sentence, sentence_start_index=0):
    markings = []

    # TODO ". = any char except newline." newline...
    LOOSE_CHAR_AFTER_COMMA_FORMAT = r",."
    PRECISE_CHAR_AFTER_COMMA_FORMAT = r',[\s0-9"”»]'
    SPACE = " "

    matches = re.finditer(LOOSE_CHAR_AFTER_COMMA_FORMAT, sentence)

    for match in matches:
        matching_text = match.group()
        suggestion = {DISPLAY_KEY: matching_text, ACTION_KEY: matching_text[0] + SPACE + matching_text[1:]}
        if not re.match(PRECISE_CHAR_AFTER_COMMA_FORMAT, match.group()):
            markings.append({FROM_KEY: sentence_start_index + match.start(),
                             TO_KEY: sentence_start_index + match.end(), TYPE_KEY: TYPO_KEY,
                             SUBTYPE_KEY: 'gabim gramatikor, shenja pikësimi',
                             DESCRIPTION_KEY: 'presja ndiqet vetëm nga një hapësirë, numër ose thonjëz',
                             SUGGESTIONS_KEY: [suggestion]})
            # TODO match without the characters in .

    return markings
