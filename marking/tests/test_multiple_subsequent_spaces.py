from django.test import TestCase

from marking.multiple_subsequent_spaces import check_for_multiple_subsequent_spaces
from utils.utils import FROM_KEY, TO_KEY, TYPE_KEY, TYPO_KEY, SUBTYPE_KEY, DESCRIPTION_KEY, SUGGESTIONS_KEY, \
    DISPLAY_KEY, ACTION_KEY, fetch_word_iterator


class MultipleSpacesTestCase(TestCase):
    def test_twoas_spaces(self):
        text = "Aq  pra."
        suggestion = {DISPLAY_KEY: 'q p', ACTION_KEY: ' '}
        expected_markings = [{FROM_KEY: 2, TO_KEY: 4, TYPE_KEY: TYPO_KEY,
                              SUBTYPE_KEY: 'gabim gramatikor, shenja pikësimi',
                              DESCRIPTION_KEY: 'hapësira nuk mund të ndiqet nga një ose disa hapësira të tjera',
                              SUGGESTIONS_KEY: [suggestion]}]
        words = list(fetch_word_iterator(text))
        self.assertEqual(check_for_multiple_subsequent_spaces(text, words), expected_markings)

    def test_two_spaces(self):
        sentences = " ".join(["Kjo eshte nje fjali.", "Nje fjali  tjeter.", "Mbyllur nga nje tjeter."])
        suggestion = {DISPLAY_KEY: 'i t', ACTION_KEY: ' '}
        expected_date_markings = [{FROM_KEY: 30, TO_KEY: 32, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shenja pikësimi',
                                   DESCRIPTION_KEY: 'hapësira nuk mund të ndiqet nga një ose disa hapësira të tjera',
                                   SUGGESTIONS_KEY: [suggestion]}]
        words = list(fetch_word_iterator(sentences))
        self.assertEqual(check_for_multiple_subsequent_spaces(sentences, words), expected_date_markings)

    def test_check_for_a_nasdonspace_after_coasdmma2_non_breaking_space(self):
        sentence = "Këngëtares i pëlqente jo vetëm mikpritja, por edhe atmosfera."
        words = list(fetch_word_iterator(sentence))
        self.assertEqual(check_for_multiple_subsequent_spaces(sentence, words), [])

    def test_check_for_a_nasdonspace_after_coasdmma1_non_breaking_space(self):
        sentence = "Këngëtares i pëlqente jo vetëm mikpritja,  por edhe atmosfera."
        suggestion = {DISPLAY_KEY: ', p', ACTION_KEY: ' '}
        expected_date_markings = [{FROM_KEY: 41, TO_KEY: 43, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shenja pikësimi',
                                   DESCRIPTION_KEY: 'hapësira nuk mund të ndiqet nga një ose disa hapësira të tjera',
                                   SUGGESTIONS_KEY: [suggestion]}]
        words = list(fetch_word_iterator(sentence))
        self.assertEqual(check_for_multiple_subsequent_spaces(sentence, words), expected_date_markings)
