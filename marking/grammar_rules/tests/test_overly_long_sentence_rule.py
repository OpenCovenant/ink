from django.test import TestCase

from marking.grammar_rules.overly_long_sentence_rule import check_for_overly_long_sentence
from utils.utils import FROM_KEY, SUBTYPE_KEY, DESCRIPTION_KEY, SUGGESTIONS_KEY, TO_KEY, TYPE_KEY, STYLISTIC_KEY


class OverlyLongSentenceTestCase(TestCase):
    def test_a_sentence(self):
        sentence = "Nga një dritë e ngrohtë zjarri në një dritë të bardhë, të ftohtë, deri diku praktike."
        self.assertEqual(check_for_overly_long_sentence(sentence, sentence), [])

    def test_an_overly_long_sentence(self):
        sentence = "A a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a" \
                   " a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a" \
                   " a a a a a a a a a a a a a a a a a a a a a a a a a a."
        expected_date_markings = [{FROM_KEY: 0, TO_KEY: 242, TYPE_KEY: STYLISTIC_KEY,
                                   SUBTYPE_KEY: 'stilistikë, fjali tepër e gjatë',
                                   DESCRIPTION_KEY: 'mungesë qartësie dhe kuptueshmerie, perpiqu ta ndash',
                                   SUGGESTIONS_KEY: []}]
        self.assertEqual(check_for_overly_long_sentence(sentence), expected_date_markings)
