from django.test import TestCase

from marking.grammar_rules.comma_rules import check_for_a_comma_rule, check_for_comma_before_or_and_rule, \
    check_for_a_nonspace_after_comma
from utils.utils import FROM_KEY, TO_KEY, TYPO_KEY, TYPE_KEY, SUBTYPE_KEY, DESCRIPTION_KEY, SUGGESTIONS_KEY, \
    DISPLAY_KEY, ACTION_KEY


class CommasTestCase(TestCase):
    def test_a_comma(self):
        text = "Këngëtares i pëlqente jo vetëm mikpritja, por edhe atmosfera."
        self.assertEqual(check_for_a_comma_rule(text, text), [])

    # def test_another_comma(self):
    #     text = "Këngëtares i pëlqente jo vetëm mikpritja por edhe atmosfera."
    #     suggestion = {DISPLAY_KEY: '... ikpritja, por edhe ...', ACTION_KEY: ''}  # TODO
    #     expected_marking = [{FROM_KEY: 0, TO_KEY: 60, TYPE_KEY: TYPO_KEY,
    #                          SUBTYPE_KEY: 'gabim gramatikor, shenja pikësimi',
    #                          DESCRIPTION_KEY: 'vendoset presje mes gjymtyrëve homogjene që bashkohen nga lidhëza '
    #                                           'dyshe "jo vetëm ..., por edhe ..."',
    #                          SUGGESTIONS_KEY: [suggestion]}]
    #     self.assertEqual(check_for_a_comma_rule(text, text), expected_marking)

    def test_anotheasasdqwedr_comma(self):
        text = "Arka duhet të mbushet me fruta, ose edhe me perime."
        self.assertEqual(check_for_comma_before_or_and_rule(text, text), [])

    # def test_anotheasdr_comma(self):
    #     text = "Arka duhet të mbushet me fruta ose edhe me perime."
    #     suggestion = {DISPLAY_KEY: '... me fruta, ose edhe ...', ACTION_KEY: ''}  # TODO
    #     expected_marking = [{FROM_KEY: 0, TO_KEY: 50, TYPE_KEY: TYPO_KEY,
    #                          SUBTYPE_KEY: 'gabim gramatikor, shenja pikësimi',
    #                          DESCRIPTION_KEY: 'vendoset presje mes gjymtyrëve homogjene që bashkohen me lidhëzën'
    #                                           ' veçuese "ose" të ndjekur nga pjëseza përforcuese "edhe"',
    #                          SUGGESTIONS_KEY: [suggestion]}]
    #     self.assertEqual(check_for_comma_before_or_and_rule(text, text), expected_marking)

    def test_check_for_a_nasdonspace_after_comma1(self):
        sentence = "Këngëtares i pëlqente jo vetëm mikpritja, por edhe atmosfera."
        self.assertEqual(check_for_a_nonspace_after_comma(sentence), [])

    def test_check_for_a_nasdonspace_after_coasdmma1(self):
        sentence = "Këngëtares i pëlqente jo vetëm mikpritja,  por edhe atmosfera."
        a = check_for_a_nonspace_after_comma(sentence)
        self.assertEqual(check_for_a_nonspace_after_comma(sentence), [])

    def test_check_for_a_nasdonspace_after_coasdmma1_non_breaking_space(self):
        sentence = "Këngëtares i pëlqente jo vetëm mikpritja, por edhe atmosfera."
        a = check_for_a_nonspace_after_comma(sentence)
        self.assertEqual(check_for_a_nonspace_after_comma(sentence), [])

    # TODO ”
    def test_t234(self):
        sentence = "John Doe, “The birth of corruption and the politics of anti-corruption in " \
                   "Albania, 1991–2005,” Nationalities Papers 41, no. 6 (2018)."
        self.assertEqual(check_for_a_nonspace_after_comma(sentence), [])

    # TODO »
    def test_t2345(self):
        sentence = "John Doe, «The birth of corruption and the politics of anti-corruption in " \
                   "Albania, 1991–2005,» Nationalities Papers 41, no. 6 (2018)."
        self.assertEqual(check_for_a_nonspace_after_comma(sentence), [])

    # def test_a_comma(self):
    #     text = ", ose edhe"
    #     words = fetch_all_words(text)
    #     self.assertEqual(words, [text])
    #
    # def test_a_comma(self):
    #     text = ", "
    #     words = fetch_all_words(text)
    #     self.assertEqual(words, [text])
    #
    # def test_a_comma(self):
    #     text = ',"'
    #     words = fetch_all_words(text)
    #     self.assertEqual(words, [text])
    #
    # def test_a_comma(self):
    #     text = ',a'
    #     words = fetch_all_words(text)
    #     self.assertEqual(words, [text])
    #
    # def test_a_comma(self):
    #     text = ',1'
    #     words = fetch_all_words(text)
    #     self.assertEqual(words, [text])
    #
    # def test_a_comma(self):
    #     text = '22.1,1'
    #     words = fetch_all_words(text)
    #     self.assertEqual(words, [text])
