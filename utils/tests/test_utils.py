from django.test import TestCase

from utils.utils import TEXT_KEY, TEXT_MARKINGS_KEY, fetch_all_words, fetch_sentence_iterator, \
    fetch_quoted_texts_iterator, fetch_email_iterator, fetch_link_iterator, fetch_abbreviation_iterator, \
    fetch_hashtag_iterator


def _generate_empty_marking_with_text(text):
    return {TEXT_KEY: text, TEXT_MARKINGS_KEY: []}


class SentenceParsingTestCase(TestCase):
    def test_unterminated_sentence(self):
        words = "Fjali e papërfunduar"
        self.assertEqual([s.group() for s in fetch_sentence_iterator(words)], [])

    def test_a_declarative_sentence(self):
        sentence = "Veç disa yje dallohen, ndoshta Venusi, ndonjë bisht arushe, e ndonjë gjurmë aeroplani."
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentence)], [sentence])

    def test_a_declarative_sentence_appended_space(self):
        sentence = "Veç disa yje dallohen, ndoshta Venusi, ndonjë bisht arushe, e ndonjë gjurmë aeroplani."
        space = " "
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentence + space)], [sentence])

    # def test_a_sentence_and_some_text(self):  # TODO rethink
    #     sentence = "Duhet te vallëzojmë shume ose edhe te kërcejmë."
    #     words = "pra kaq"
    #     space = " "
    #     self.assertEqual([s.group() for s in fetch_sentence_iterator(sentence + space + words)], [sentence])

    def test_an_interrogative_sentence(self):
        sentence = "A e zuri gjumi?"
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentence)], [sentence])

    def test_an_exclamatory_sentence(self):
        sentence = "Sikur të ishte ushtruar më shumë!"
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentence)], [sentence])

    def test_a_sentence_with_a_question_mark_and_an_exclamation_mark(self):
        sentence = "Pra ende nuk kemi makina fluturuese?!"
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentence)], [sentence])

    def test_a_sentence_with_an_exclamation_mark_and_a_question_mark(self):
        sentence = "Pse me detyrim është blerja e revistës!?"
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentence)], [sentence])

    def test_a_sentence_with_many_question_marks(self):
        sentence = "Mos na kaloi para syve???"
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentence)], [sentence])

    def test_a_sentence_with_many_ending_spaces(self):
        sentence = "Macja vazhdoi."
        space = " "
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentence + space * 5)], [sentence])

    def test_a_sentence_with_an_abbreviation(self):
        sentence = "Ai e mban dorën e varur, n.q.s. është duke e mbajtur cigaren me përtesë."
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentence)], [sentence])

    def test_a_declarative_sentence_and_a_half(self):
        sentences = "Veç disa yje dallohen, ndoshta Venusi, ndonjë bisht arushe, e ndonjë gjurmë aeroplani. Djali del"
        sentences_list = ["Veç disa yje dallohen, ndoshta Venusi, ndonjë bisht arushe, e ndonjë gjurmë aeroplani."]
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentences)], sentences_list)

    def test_two_sentences(self):
        sentences = "Ndez cigaren e nxjerr tymin e parë. Dikush që do ta shihte nga larg, nuk do ta kuptonte n.q.s." \
                    " ishte tym apo avull."
        sentences_list = ["Ndez cigaren e nxjerr tymin e parë.",
                          "Dikush që do ta shihte nga larg, nuk do ta kuptonte n.q.s. ishte tym apo avull."]
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentences)], sentences_list)

    def test_two_sentences_with_appended_space(self):
        sentences = "Ndez cigaren e nxjerr tymin e parë. Dikush që do ta shihte nga larg, nuk do ta kuptonte n.q.s." \
                    " ishte tym apo avull. "
        sentences_list = ["Ndez cigaren e nxjerr tymin e parë.",
                          "Dikush që do ta shihte nga larg, nuk do ta kuptonte n.q.s. ishte tym apo avull."]
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentences)], sentences_list)

    def test_a_sentence_with_a_date(self):
        sentence = "Manastir, më 14.11.1908."
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentence)], [sentence])

    def test_a_sentence_with_an_ellipsis(self):
        sentence = "Njerëzit po fillojnë të shtohen tek bari, ndoshta është momenti që të lëvizë…"
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentence)], [sentence])

    def test_sentence_with_quotes(self):
        sentence = '"Le të punojmë më fort, - kishte thënë Genti, - sa më shpejt të jetë e mundur!"'
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentence)], [sentence])

    def test_many_sentences(self):
        sentences = '"Le të punojmë më fort, - kishte thënë Artani, - sa më shpejt të jetë e mundur!" Mëngjesi erdhi.'
        sentences_list = ['"Le të punojmë më fort, - kishte thënë Artani, - sa më shpejt të jetë e mundur!"',
                          'Mëngjesi erdhi.']
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentences)], sentences_list)

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
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentences)], sentences_list)

    def test_even_more_sentences(self):
        sentences = 'Ligjërimi u sqarua. Është i vështirë.'
        sentences_list = ['Ligjërimi u sqarua.', 'Është i vështirë.']
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentences)], sentences_list)

    def test_even_more_sentences2(self):
        sentences = 'Artani u ngrit. Çaloi disa here dhe pastaj vazhdoi.'
        sentences_list = ['Artani u ngrit.', 'Çaloi disa here dhe pastaj vazhdoi.']
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentences)], sentences_list)

    def test_even_more_sentences3(self):
        sentences = 'Kemi pergatitur ushqimin.\n\n\nÇfarë ka ngelur?'
        sentences_list = ['Kemi pergatitur ushqimin.', 'Çfarë ka ngelur?']
        self.assertEqual([s.group() for s in fetch_sentence_iterator(sentences)], sentences_list)


class WordParsingTestCase(TestCase):
    def test_a_character(self):
        text = "a"
        words = fetch_all_words(text)
        self.assertEqual(words, [text])

    def test_words_with_a_hyphen(self):
        text = "ab-cd"
        words = fetch_all_words(text)
        self.assertEqual(words, [text])

    def test_words_with_an_apostrophe(self):
        text = "a'bc"
        words = fetch_all_words(text)
        self.assertEqual(words, [text])


class TextParsingTestCase(TestCase):
    # def test_an_emote(self):  # TODO
    #     text = ""
    #     words = fetch_all_words(text)
    #     self.assertEqual(words, [text])

    def test_a_non_Albanian_letter(self):
        text = "løfte"
        words = fetch_all_words(text)
        self.assertEqual(words, [text])

    def test_a_Latin_word(self):
        text = "capita"
        words = fetch_all_words(text)
        self.assertEqual(words, [text])

    # def test_a_dialectism(self):  # TODO
    #     text = ""
    #     words = fetch_all_words(text)
    #     self.assertEqual(words, [text])

    def test_it_has_accent(self):
        text = "a"
        words = fetch_all_words(text)
        self.assertEqual(words, [text])

    def test_words(self):
        words = "disa shkrime"
        expected_words = ["disa", "shkrime"]
        self.assertEqual(fetch_all_words(words), expected_words)


class QuotedTextParsingTestCase(TestCase):
    def test_unquoted_texts(self):
        text = "Kryqëzoi këmbët, u shtri pak në karrige dhe nxori tymin…"
        self.assertEqual([quoted_text for quoted_text in fetch_quoted_texts_iterator(text)], [])

    def test_another_unquoted_texts(self):
        text = 'Kryqëzoi këmbët, u "shtri pak në karrige dhe nxori tymin…'
        self.assertEqual([quoted_text for quoted_text in fetch_quoted_texts_iterator(text)], [])

    def test_quoted_text1(self):
        text = 'S’ka qenë ndonjherë ndonjë "pirës" i madh.'
        self.assertEqual([quoted_text.group() for quoted_text in fetch_quoted_texts_iterator(text)], ['"pirës"'])

    def test_more_quoted_text(self):
        text = "Kryqëzoi këmbët dhe “kaq” u shtri pak në karrige dhe nxori tymin!"
        self.assertEqual([quoted_text.group() for quoted_text in fetch_quoted_texts_iterator(text)], ['“kaq”'])

    def test_even_more_quoted_text(self):
        text = "Kryqëzoi këmbët dhe «martesa» u shtri pak në karrige dhe nxori tymin!"
        self.assertEqual([quoted_text.group() for quoted_text in fetch_quoted_texts_iterator(text)], ['«martesa»'])

    def test_even_more_quoted_text2(self):
        text = "Kryqëzoi këmbët dhe martesa u shtri pak në „karrige“ dhe nxori tymin!"
        self.assertEqual([quoted_text.group() for quoted_text in fetch_quoted_texts_iterator(text)], ['„karrige“'])

    def test_even_more_quoted_text3(self):
        text = "Kryqëzoi ‘këmbët’ dhe martesa u shtri pak në karrige dhe nxori tymin!"
        self.assertEqual([quoted_text.group() for quoted_text in fetch_quoted_texts_iterator(text)], ['‘këmbët’'])

    def test_quoted_text(self):
        text = 'S’ka qenë ndonjherë ndonjë pirës i madh. Në gjimnaz e shtynin shokët dhe dëshira për të qënë më' \
               ' "cool" në sytë e atyre që mendonin se të pije cigare ishte "cool", të gjithëve me një fjalë.'
        self.assertEqual([quoted_text.group() for quoted_text in fetch_quoted_texts_iterator(text)],
                         ['"cool"', '"cool"'])


class LinkParsingTestCase(TestCase):
    """
    links to forbid:
    www.google.com
    https://localhost
    https://localhost:4200
    http://localhost
    http://localhost

    links to allow:
    somesite.xy
    """

    def test_a_link(self):
        link = "www.google.com"
        self.assertEqual([l.group() for l in fetch_link_iterator(link)], [link])

    # def test_links(self):  # TODO
    #     links = ["www.google.com", "https://localhost:4200"]
    #     sentence = links[0] + " " + links[1]
    #     self.assertEqual([l.group() for l in fetch_link_iterator(sentence)], links)

    def test3(self):
        link = "https://www.youtube.com/"
        sentence = "ishte tek " + link + " dhe aq"
        self.assertEqual([l.group() for l in fetch_link_iterator(sentence)], [link])

    # def test_urls(self):
    #     text = ""
    #     self.assertEqual(fetch_link_iterator(), 0)


class EmailParsingTestCase(TestCase):
    """
    emails to forbid:
    www.google.com

    email to allow:
    somesite.xy
    """

    def test_email(self):
        email = "johndoe@gmail.com"
        self.assertEqual([e.group() for e in fetch_email_iterator(email)], [email])

    def test_email_in_a_sentence(self):
        email = "johndoe@gmail.com"
        sentence = "Pra njera ishte " + email + " dhe kaq."
        self.assertEqual([e.group() for e in fetch_email_iterator(sentence)], [email])

    def test_an_email(self):
        word = 'john.doe@mail.com'
        for email in fetch_email_iterator(word):
            self.assertEqual(email.group(), word)

    def test_an_email_in_a_sentence(self):
        w = 'john.doe@mail.com'
        word = 'Shpesh mund te hasesh ' + w + ', nder disa adresa.'
        for email in fetch_email_iterator(word):
            self.assertEqual(email.group(), w)


class AbbreviationParsingTestCase(TestCase):
    def test_abbreviations(self):
        abbreviation = "p.sh."
        self.assertEqual([s.group() for s in fetch_abbreviation_iterator(abbreviation)], [abbreviation])

    def test_abbreviations1(self):
        abbreviation = "jokal."
        sentence = "pra kemi nje " + abbreviation + "ketu "
        self.assertEqual([s.group() for s in fetch_abbreviation_iterator(sentence)], [abbreviation])

    def test_abbreviations7(self):
        abbreviation = "arkeol."
        sentence = "pra kemi nje ketu " + abbreviation
        self.assertEqual([s.group() for s in fetch_abbreviation_iterator(sentence)], [abbreviation])

    def test_abbreviations2(self):
        abbreviations = ["aviac.", "anat."]
        sentence = "pra kemi nje ketu " + abbreviations[0] + " dhe " + abbreviations[1] + "."
        self.assertEqual([s.group() for s in fetch_abbreviation_iterator(sentence)], abbreviations)

    # TODO sentences ending with an acronym, do not have an extra ., should this contain the check or a rule?
    def test_abbreviations3(self):  # TODO this is not a correct sentence
        abbreviation = "bised."
        sentence = "Pra dhe " + abbreviation + "."
        self.assertEqual([s.group() for s in fetch_abbreviation_iterator(sentence)], [abbreviation])

    def test_abbreviations5(self):
        abbreviation = "elektr."
        sentence = "Pra dhe " + abbreviation + "?"
        self.assertEqual([s.group() for s in fetch_abbreviation_iterator(sentence)], [abbreviation])

    def test_abbreviations4(self):
        abbreviation = "botan."
        sentence = "Buka " + abbreviation + " dhe kaq."
        self.assertEqual([s.group() for s in fetch_abbreviation_iterator(sentence)], [abbreviation])

    # TODO this is hard to detect if the last word of such a sentence is an abbreviation or not
    def test_abbreviations6(self):
        abbreviation = "dipl."
        sentence = "Nje fjali " + abbreviation
        self.assertEqual([s.group() for s in fetch_abbreviation_iterator(sentence)], [abbreviation])

    def test_abbreviations27(self):
        abbreviation = "abcdefghi."
        sentence = "Nje fjali " + abbreviation + " dhe disa fjale te tjera."
        self.assertEqual([s.group() for s in fetch_abbreviation_iterator(sentence)], [])


class HashtagParsingTestCase(TestCase):
    def test_a_hashtag(self):
        word = '#hashtag'
        for hashtag in fetch_hashtag_iterator(word):
            self.assertEqual(hashtag.group(), word)

    def test_a_hashtag_with_an_appended_space(self):
        word = "#hashtag"
        space = " "
        for hashtag in fetch_hashtag_iterator(word + space):
            self.assertEqual(hashtag.group(), word)

    def test_words_with_a_hashtag(self):
        word = "#hashtag"
        space = " "
        for hashtag in fetch_hashtag_iterator(word + space):
            self.assertEqual(hashtag.group(), word)

    def test_words_with_hashtags(self):
        hashtags = ["#epara", "#njëtjetër", "#përmbyllëse"]
        word = hashtags[0] + " dhe " + hashtags[1] + " , madje dhe " + hashtags[2]
        for index, hashtag in enumerate(fetch_hashtag_iterator(word)):
            self.assertEqual(hashtag.group(), hashtags[index])

    def test_a_sentence_with_a_hashtag(self):
        hashtag = "#tani"
        sentence = "Se fundmi eshte vene re te perdoren dhe " + hashtag + " ne rrjetet shoqerore."
        self.assertEqual([h.group() for h in fetch_hashtag_iterator(sentence)], [hashtag])

    def test_sentences_with_a_hashtag(self):
        hashtag = "#dicka"
        sentence = "Se fundmi eshte vene re te perdoren dhe " + hashtag + " ne rrjetet shoqerore."
        self.assertEqual([h.group() for h in fetch_hashtag_iterator(sentence)], [hashtag])

    def test_sentences_with_hashtags(self):
        hashtags = ["#njera", "#tjetra"]
        sentence = "Se fundmi eshte vene re te perdoren #njera dhe #tjetra ne rrjetet shoqerore."
        self.assertEqual([h.group() for h in fetch_hashtag_iterator(sentence)], hashtags)
