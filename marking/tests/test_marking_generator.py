from django.test import TestCase
import secrets

from marking.marking_generator import generate_markings, has_numbers, has_uppercase_letters
from utils.utils import TEXT_KEY, TEXT_MARKINGS_KEY, ALPHABET


def _generate_empty_marking_with_text(text):
    return {TEXT_KEY: text, TEXT_MARKINGS_KEY: []}


class MarkingsTestCase(TestCase):
    def test_empty_marking(self):
        text = ""
        empty_marking = _generate_empty_marking_with_text(text)
        self.assertEqual(empty_marking[TEXT_KEY], text)
        self.assertEqual(type(empty_marking[TEXT_MARKINGS_KEY]), list)
        self.assertEqual(len(empty_marking[TEXT_MARKINGS_KEY]), 0)

    def test_number_of_suggestions_in_a_marking(self):
        len_of_word = secrets.randbelow(10)

        text = ""
        for _ in range(len_of_word):
            text += ALPHABET[secrets.randbelow(len(ALPHABET))]

        max_suggestions = 5
        markings = generate_markings(text, max_suggestions)
        self.assertLessEqual(len(markings[TEXT_MARKINGS_KEY]), max_suggestions)

    def test_markings_on_empty_text(self):
        text = ""
        markings = generate_markings(text)
        self.assertEqual(markings, _generate_empty_marking_with_text(text))

    def test_markings_on_a_space(self):
        text = " "
        markings = generate_markings(text)
        self.assertEqual(markings, _generate_empty_marking_with_text(text))

    def test_markings_on_a_proper_noun(self):
        text = "Opqrstuvw"
        markings = generate_markings(text)
        self.assertEqual(markings, _generate_empty_marking_with_text(text))

    def test_markings_on_two_proper_nouns(self):
        text = "Abcdefg Hijkl"
        markings = generate_markings(text)
        self.assertEqual(markings, _generate_empty_marking_with_text(text))

    def test_markings_on_all_caps(self):
        text = "ABC"
        markings = generate_markings(text)
        self.assertEqual(markings, _generate_empty_marking_with_text(text))

    def test_markings_on_one_digit(self):
        text = "9"
        markings = generate_markings(text)
        self.assertEqual(markings, _generate_empty_marking_with_text(text))

    def test_markings_on_many_digits(self):
        text = "893215"
        markings = generate_markings(text)
        self.assertEqual(markings, _generate_empty_marking_with_text(text))

    def test_markings_on_an_apostrophe(self):
        text = "a'bc"
        markings = generate_markings(text)
        self.assertEqual(markings[TEXT_KEY], text)

    def test_markings_on_a_hyphen(self):
        text = "ab-cd"
        markings = generate_markings(text)
        self.assertEqual(markings[TEXT_KEY], text)

    def test_markings_on_a_space_after_sentence(self):
        text = "a. "
        markings = generate_markings(text)
        self.assertEqual(markings[TEXT_KEY], text)

    def test_text_markings_for_overly_long_sentences(self):
        pass

    def test_text_markings_for_dates(self):
        pass

    def test_text_markings_for_numerics(self):
        "një"
        "njëmbëdhjetë"
        "shtatëmbëdhjetë"
        "njëzet"
        "njëzet e tre"
        "dyzet e tetë"
        "gjashtëdhjetë"
        "pesëdhjetë e një"
        "pesëdhjetë e shtatë"
        "pesëdhjetë e tetë"
        "shtatëdhjetë"
        "pesëqind e gjashtëdhjetë e një"
        "dy mijë e tetëdhjetë e nëntë"
        "shtatëmbëdhjetë mijë e gjashtëqind e dy"

    # def test_markings_on_a_hash(self):
    #     text = "#"
    #     markings = generate_markings(text)
    #     self.assertEqual(markings, _generate_empty_marking_with_text(text))
    #
    # def test_markings_on_a_hash_followed_by_words(self):
    #     text = "#abc"
    #     markings = generate_markings(text)
    #     self.assertEqual(markings, _generate_empty_marking_with_text(text))


class SkippableWordsTestCase(TestCase):
    def test_word_with_numbers(self):
        word = '1337'
        self.assertTrue(has_numbers(word))

    def test_word_with_numerical_quantity(self):
        word = '20mg'
        self.assertTrue(has_numbers(word))

    def test_word_with_numerical_quantity_and_an_uppercase_letter(self):
        word = '2L'
        self.assertTrue(has_uppercase_letters(word))

    def test_an_uppercase_letter(self):
        word = 'A'
        self.assertTrue(has_uppercase_letters(word))

    def test_word_with_an_uppercase_letter(self):
        word = 'Madje'
        self.assertTrue(has_uppercase_letters(word))

    def test_word_with_uppercase_letters(self):
        word = 'IGJEUM'
        self.assertTrue(has_uppercase_letters(word))

    def test_word_with_a_camel_case(self):
        word = 'camelCase'
        self.assertTrue(has_uppercase_letters(word))


class SkimmingWordsTestCase(TestCase):
    pass
