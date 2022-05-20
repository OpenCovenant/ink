from django.test import TestCase

from collections import Counter

from api.ec_specials import generate_ec_permutations


class EdiaeresisAndCcedillaTestCase(TestCase):
    def test_generated_permutations(self):
        text = None
        permutations = generate_ec_permutations(text)
        self.assertEqual(permutations, [""])

    def test_generated_permutations_empty_text(self):
        text = ""
        permutations = generate_ec_permutations(text)
        self.assertEqual(permutations, [])

    def test_generated_permutations_for_c_cedilla(self):
        text = "cjap"
        permutations = generate_ec_permutations(text)
        self.assertEqual(Counter(permutations), Counter(["çjap"]))

    def test_generated_permutations_for_e_diaeresis(self):
        text = "shtepi"
        permutations = generate_ec_permutations(text)
        self.assertEqual(permutations, ["shtëpi"])

    def test_generated_permutations_for_c_cedilla_and_e_diaeresis(self):
        text = "cokollate"
        permutations = generate_ec_permutations(text)
        self.assertEqual(Counter(permutations), Counter(["cokollatë", "çokollate", "çokollatë"]))
