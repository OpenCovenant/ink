from django.test import TestCase

from api.marking_generator import generate_markings
from utils.utils import TEXT_KEY, TEXT_MARKINGS_KEY, ALPHABET, fetch_all_words, fetch_all_sentences


def _generate_empty_marking_with_text(text):
    return {TEXT_KEY: text, TEXT_MARKINGS_KEY: []}


class SentenceParsingTestCase(TestCase):
    def test_a_declarative_sentence(self):
        sentence = "Veç disa yje dallohen, ndoshta Venusi, ndonjë bisht arushe, e ndonjë gjurmë aeroplani."
        self.assertEqual(fetch_all_sentences(sentence), [sentence])

    def test_an_interrogative_sentence(self):
        sentence = "A e zuri gjumi?"
        self.assertEqual(fetch_all_sentences(sentence), [sentence])

    def test_an_exclamatory_sentence(self):
        sentence = "Sikur të ishte ushtruar më shumë."
        self.assertEqual(fetch_all_sentences(sentence), [sentence])

    def test_a_sentence_with_a_question_mark_and_an_exclamation_mark(self):
        sentence = "Pra ende nuk kemi makina fluturuese?!"
        self.assertEqual(fetch_all_sentences(sentence), [sentence])

    def test_a_sentence_with_an_exclamation_mark_and_a_question_mark(self):
        sentence = "Pse me detyrim është blerja e revistës!?"
        self.assertEqual(fetch_all_sentences(sentence), [sentence])

    def test_a_sentence_with_many_question_marks(self):
        sentence = "Mos na kaloi para syve???"
        self.assertEqual(fetch_all_sentences(sentence), [sentence])

    def test_a_declarative_sentence_and_a_half(self):
        sentences = "Veç disa yje dallohen, ndoshta Venusi, ndonjë bisht arushe, e ndonjë gjurmë aeroplani. Djali del"
        sentences_list = ["Veç disa yje dallohen, ndoshta Venusi, ndonjë bisht arushe, e ndonjë gjurmë aeroplani."]
        self.assertEqual(fetch_all_sentences(sentences), sentences_list)

    def test_two_sentences(self):
        sentences = "Ndez cigaren e nxjerr tymin e parë. Dikush që do ta shihte nga larg, nuk do ta kuptonte n.q.s." \
                    " ishte tym apo avull."
        sentences_list = ["Ndez cigaren e nxjerr tymin e parë.",
                          "Dikush që do ta shihte nga larg, nuk do ta kuptonte n.q.s. ishte tym apo avull."]
        self.assertEqual(fetch_all_sentences(sentences), sentences_list)

    def test_two_sentences_with_appended_space(self):
        sentences = "Ndez cigaren e nxjerr tymin e parë. Dikush që do ta shihte nga larg, nuk do ta kuptonte n.q.s." \
                    " ishte tym apo avull. "
        sentences_list = ["Ndez cigaren e nxjerr tymin e parë.",
                          "Dikush që do ta shihte nga larg, nuk do ta kuptonte n.q.s. ishte tym apo avull."]
        self.assertEqual(fetch_all_sentences(sentences), sentences_list)

    def test_a_sentence_with_a_date(self):
        sentence = "Manastir, më 14.11.1908."
        self.assertEqual(fetch_all_sentences(sentence), [sentence])

    def test_a_sentence_with_an_ellipsis(self):
        sentence = "Njerëzit po fillojnë të shtohen tek bari, ndoshta është momenti që të lëvizë…"
        self.assertEqual(fetch_all_sentences(sentence), [sentence])

    def test_sentence_with_quotes(self):
        sentence = '"Le të punojmë më fort, - kishte thënë Genti, - sa më shpejt të jetë e mundur!"'
        self.assertEqual(fetch_all_sentences(sentence), [sentence])

    def test_many_sentences(self):
        sentences = '"Le të punojmë më fort, - kishte thënë Artani, - sa më shpejt të jetë e mundur!" Mëngjesi erdhi.'
        sentences_list = ['"Le të punojmë më fort, - kishte thënë Artani, - sa më shpejt të jetë e mundur!"',
                          'Mëngjesi erdhi.']
        self.assertEqual(fetch_all_sentences(sentences), sentences_list)

    def test_more_sentences(self):
        sentences = "Vazhdon ecën duke mos menduar shumë, me kokën poshtë. Shihte hijen e tij, të krijuar nga mijëra" \
                    " dritat sipër kokës, të vendosura nga bashkia për sa më shumë foto nga ata që vijnë në qytet apo" \
                    " dhe nga banorët e saj. Lokali i tij i preferuar qenka hapur, qenka dhe kamerieri i tij i" \
                    " preferuar, ai që të lodh me muhabet… Kafen me qumësht anash?"
        sentences_list = ["Vazhdon ecën duke mos menduar shumë, me kokën poshtë.",
                          "Shihte hijen e tij, të krijuar nga mijëra dritat sipër kokës, të vendosura nga bashkia për"
                          " sa më shumë foto nga ata që vijnë në qytet apo dhe nga banorët e saj.",
                          "Lokali i tij i preferuar qenka hapur, qenka dhe kamerieri i tij i preferuar, ai që të lodh"
                          " me muhabet…", "Kafen me qumësht anash?"]
        self.assertEqual(fetch_all_sentences(sentences), sentences_list)


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

    def test_number_of_corrs_in_a_marking(self):
        import secrets
        len_of_word = secrets.randbelow(10)

        text = ""
        for _ in range(len_of_word):
            text += ALPHABET[secrets.randbelow(len(ALPHABET))]

        max_corrs = 5
        markings = generate_markings(text, max_corrs)
        self.assertLessEqual(len(markings[TEXT_MARKINGS_KEY]), max_corrs)

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
