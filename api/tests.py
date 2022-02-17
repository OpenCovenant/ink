from django.test import TestCase

from api.marking_generator import generate_markings
from utils.utils import TEXT_KEY, TEXT_MARKINGS_KEY, ALPHABET, fetch_all_words


def _generate_empty_marking_with_text(text):
    return {TEXT_KEY: text, TEXT_MARKINGS_KEY: []}


class TextParsingTestCase(TestCase):
    def test_a_character(self):
        text_with_a_character = "a"
        words = fetch_all_words(text_with_a_character)
        self.assertEqual(words, [text_with_a_character])

    def test_words_with_a_hyphen(self):
        text_with_a_hyphen = "ab-cd"
        words = fetch_all_words(text_with_a_hyphen)
        self.assertEqual(words, [text_with_a_hyphen])

    def test_words_with_an_apostrophe(self):
        text_with_an_apostrophe = "a'bc"
        words = fetch_all_words(text_with_an_apostrophe)
        self.assertEqual(words, [text_with_an_apostrophe])


class MarkingsTestCase(TestCase):
    def test_empty_marking(self):
        empty_text = ""
        empty_marking = _generate_empty_marking_with_text(empty_text)
        self.assertEqual(empty_marking[TEXT_KEY], empty_text)
        self.assertEqual(type(empty_marking[TEXT_MARKINGS_KEY]), list)
        self.assertEqual(len(empty_marking[TEXT_MARKINGS_KEY]), 0)

    def test_number_of_suggs_in_a_marking(self):
        import secrets
        len_of_word = secrets.randbelow(10)

        text = ""
        for _ in range(len_of_word):
            text += ALPHABET[secrets.randbelow(len(ALPHABET))]

        max_suggs = 5
        markings = generate_markings(text, max_suggs)
        self.assertLessEqual(len(markings[TEXT_MARKINGS_KEY]), max_suggs)

    def test_markings_on_empty_text(self):
        empty_text = ""
        markings = generate_markings(empty_text)
        self.assertEqual(markings, _generate_empty_marking_with_text(empty_text))

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
        text_with_an_apostrophe = "a'bc"
        markings = generate_markings(text_with_an_apostrophe)
        self.assertEqual(markings[TEXT_KEY], text_with_an_apostrophe)

    def test_markings_on_a_hyphen(self):
        text_with_a_hyphen = "ab-cd"
        markings = generate_markings(text_with_a_hyphen)
        self.assertEqual(markings[TEXT_KEY], text_with_a_hyphen)

    def test_markings_on_a_space_after_sentence(self):
        text = "a. "
        markings = generate_markings(text)
        self.assertEqual(markings[TEXT_KEY], text)


class EvolvingMarkingsTestCase(TestCase):
    def setUp(self):
        pass

    def test_sth_that_i_dont_expect_to_change_often(self):
        pass
