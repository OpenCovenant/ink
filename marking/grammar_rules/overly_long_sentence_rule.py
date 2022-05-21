from utils.utils import fetch_all_words, DESCRIPTION_KEY, FROM_KEY, SUGGESTIONS_KEY, TYPE_KEY, STYLISTIC_KEY, TO_KEY, \
    SUBTYPE_KEY


def check_for_overly_long_sentence(sentence, sentence_start_index=0):
    marking = []
    MAX_NUMBER_OF_WORDS = 70

    # TODO hotfix to skip cited text as `fetch_sentence_iterator` still doesn't account for it
    if ':' in sentence or '"' in sentence or ';' in sentence:
        return marking

    if len(fetch_all_words(sentence)) > MAX_NUMBER_OF_WORDS:
        marking.append(
            {FROM_KEY: sentence_start_index, TO_KEY: sentence_start_index + len(sentence), TYPE_KEY: STYLISTIC_KEY,
             SUBTYPE_KEY: 'stilistikë, fjali tepër e gjatë',
             DESCRIPTION_KEY: 'mungesë qartësie dhe kuptueshmerie, perpiqu ta ndash', SUGGESTIONS_KEY: []})
        # TODO empty here for now, maybe through AI in the future we can provide a decent breakdown of the sentence

    return marking
