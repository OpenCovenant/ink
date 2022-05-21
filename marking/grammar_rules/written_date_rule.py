import re

from utils.utils import FROM_KEY, TO_KEY, DESCRIPTION_KEY, TYPE_KEY, SUGGESTIONS_KEY, TYPO_KEY, SUBTYPE_KEY, \
    ACTION_KEY, DISPLAY_KEY


def check_for_a_written_date_rule(sentence, sentence_start_index=0):
    markings = []

    # TODO bug here, "shkurt 2020-shkurt 2022"

    # TODO ". = any char except newline." newline...
    LOOSE_DATE_FORMAT = r'([0-9]+).(janar|shkurt|mars|prill|maj|qershor|korrik|gusht|shtator|tetor|nëntor|dhjetor).([0-9]+)'
    PRECISE_DATE_FORMAT = r'(([0-9]+)+?)(.+?)(janar|shkurt|mars|prill|maj|qershor|korrik|gusht|shtator|tetor|nëntor|dhjetor+?)(.+?)(([0-9]+)+?)'

    matches = re.finditer(LOOSE_DATE_FORMAT, sentence)

    for match in matches:
        finding = re.search(PRECISE_DATE_FORMAT, match.group())
        if finding and (finding.group(3) != " " or finding.group(5) != " "):
            proper_date = finding.group(1) + " " + finding.group(4) + " " + finding.group(6)
            suggestion = {DISPLAY_KEY: proper_date, ACTION_KEY: proper_date}
            markings.append(
                {FROM_KEY: sentence_start_index + match.start(), TO_KEY: sentence_start_index + match.end(),
                 TYPE_KEY: TYPO_KEY, SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                 DESCRIPTION_KEY: 'nuk vihet asnjë shenjë midis ditës, muajit dhe vitit, në datat e plota ku muaji'
                                  ' shkruhet me shkronja',
                 SUGGESTIONS_KEY: [suggestion]})
            # TODO match without the characters in .

    return markings


def check_for_another_written_date_rule(sentence, sentence_start_index=0):
    markings = []

    # TODO ". = any char except newline." newline...
    LOOSE_DATE_FORMAT = r'([0-9]+).([0-9]+).([0-9]+)'
    PRECISE_DATE_FORMAT = r'(([0-9]+)+?)(.+?)(([0-9]+)+?)(.+?)(([0-9]+)+?)'

    matches = re.finditer(LOOSE_DATE_FORMAT, sentence)

    for match in matches:
        finding = re.search(PRECISE_DATE_FORMAT, match.group())
        if finding and (finding.group(3) != "." or finding.group(6) != "."):
            proper_date = finding.group(1) + "." + finding.group(4) + "." + finding.group(7)
            suggestion = {DISPLAY_KEY: proper_date, ACTION_KEY: proper_date}
            markings.append(
                {FROM_KEY: sentence_start_index + match.start(), TO_KEY: sentence_start_index + match.end(),
                 TYPE_KEY: TYPO_KEY, SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                 DESCRIPTION_KEY: 'vihet një pikë pas shënimit të datës dhe të muajit, në datat e plota ku muaji'
                                  ' shkruhet me shifra arabe',
                 SUGGESTIONS_KEY: [suggestion]})
            # TODO match without the characters in .

    return markings
