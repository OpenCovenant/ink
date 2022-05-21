from django.test import TestCase

from marking.grammar_rules.written_date_rule import check_for_a_written_date_rule, check_for_another_written_date_rule
from utils.utils import FROM_KEY, TYPE_KEY, TYPO_KEY, DESCRIPTION_KEY, SUGGESTIONS_KEY, TO_KEY, SUBTYPE_KEY, \
    DISPLAY_KEY, ACTION_KEY


class DatesTestCase(TestCase):
    def test_a_date1(self):
        text = "Nuk duhet të shkruajmë 1/12/1998."
        date_marking = check_for_another_written_date_rule(text)
        expected_date_markings = [{FROM_KEY: 23, TO_KEY: 32, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                                   DESCRIPTION_KEY: 'vihet një pikë pas shënimit të datës dhe të muajit, në datat e'
                                                    ' plota ku muaji shkruhet me shifra arabe',
                                   SUGGESTIONS_KEY: [{DISPLAY_KEY: "1.12.1998", ACTION_KEY: "1.12.1998"}]}]
        self.assertEqual(date_marking, expected_date_markings)

    # def test_a_date1a(self):  # TODO
    #     text = "Pra vallëzuan gjatë periudhës qershor 2020-qershor 2022."
    #     date_marking = check_for_another_written_date_rule(text)
    #     expected_date_markings = [{FROM_KEY: 23, TO_KEY: 32, TYPE_KEY: TYPO_KEY,
    #                                SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
    #                                DESCRIPTION_KEY: 'vihet një pikë pas shënimit të datës dhe të muajit, në datat e'
    #                                                 ' plota ku muaji shkruhet me shifra arabe',
    #                                SUGGESTIONS_KEY: [{DISPLAY_KEY: "1.12.1998", ACTION_KEY: "1.12.1998"}]}]
    #     self.assertEqual(date_marking, expected_date_markings)

    def test_a_date1b(self):
        text = "Muaji i dytë është muaji shkurt."
        date_marking = check_for_another_written_date_rule(text)
        self.assertEqual(date_marking, [])

    def test_a_date1c(self):
        text = "Muaji i dytë është muaji shkurt."
        date_marking = check_for_another_written_date_rule(text)
        self.assertEqual(date_marking, [])

    def test_a_date1d(self):
        text = "Muaji i dytë është muaji shkurt."
        date_marking = check_for_a_written_date_rule(text)
        self.assertEqual(date_marking, [])

    def test_a_date2(self):
        text = "Nuk duhet të shkruajmë 01/12/1998."
        date_marking = check_for_another_written_date_rule(text)
        expected_date_markings = [{FROM_KEY: 23, TO_KEY: 33, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                                   DESCRIPTION_KEY: 'vihet një pikë pas shënimit të datës dhe të muajit, në datat e'
                                                    ' plota ku muaji shkruhet me shifra arabe',
                                   SUGGESTIONS_KEY: [{DISPLAY_KEY: "01.12.1998", ACTION_KEY: "01.12.1998"}]}]
        self.assertEqual(date_marking, expected_date_markings)

    def test_a_date3(self):
        text = "Nuk duhet të shkruajmë 1/12/1998. Gabim është edhe 2/12/1998."
        date_marking = check_for_another_written_date_rule(text)
        expected_date_markings = [{FROM_KEY: 23, TO_KEY: 32, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                                   DESCRIPTION_KEY: 'vihet një pikë pas shënimit të datës dhe të muajit, në datat e'
                                                    ' plota ku muaji shkruhet me shifra arabe',
                                   SUGGESTIONS_KEY: [{DISPLAY_KEY: "1.12.1998", ACTION_KEY: "1.12.1998"}]},
                                  {FROM_KEY: 51, TO_KEY: 60, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                                   DESCRIPTION_KEY: 'vihet një pikë pas shënimit të datës dhe të muajit, në datat e'
                                                    ' plota ku muaji shkruhet me shifra arabe',
                                   SUGGESTIONS_KEY: [{DISPLAY_KEY: "2.12.1998", ACTION_KEY: "2.12.1998"}]}]
        self.assertEqual(date_marking, expected_date_markings)

    def test_a_date4(self):
        text = "Nuk duhet te shkruajme as 1/12/1998, as 2/12/1998."
        date_marking = check_for_another_written_date_rule(text)
        expected_date_markings = [{FROM_KEY: 26, TO_KEY: 35, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                                   DESCRIPTION_KEY: 'vihet një pikë pas shënimit të datës dhe të muajit, në datat e'
                                                    ' plota ku muaji shkruhet me shifra arabe',
                                   SUGGESTIONS_KEY: [{DISPLAY_KEY: "1.12.1998", ACTION_KEY: "1.12.1998"}]},
                                  {FROM_KEY: 40, TO_KEY: 49, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                                   DESCRIPTION_KEY: 'vihet një pikë pas shënimit të datës dhe të muajit, në datat e'
                                                    ' plota ku muaji shkruhet me shifra arabe',
                                   SUGGESTIONS_KEY: [{DISPLAY_KEY: "2.12.1998", ACTION_KEY: "2.12.1998"}]}]
        self.assertEqual(date_marking, expected_date_markings)

    def test_a_date5(self):
        text = "Nuk duhet te shkruajme 1/dhjetor/1998."
        expected_date_markings = [{FROM_KEY: 23, TO_KEY: 37, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                                   DESCRIPTION_KEY: 'nuk vihet asnjë shenjë midis ditës, muajit dhe vitit, në datat e'
                                                    ' plota ku muaji shkruhet me shkronja',
                                   SUGGESTIONS_KEY: [{DISPLAY_KEY: "1 dhjetor 1998", ACTION_KEY: "1 dhjetor 1998"}]}]
        date_marking = check_for_a_written_date_rule(text)
        self.assertEqual(date_marking, expected_date_markings)

    def test_a_date6(self):
        text = "Nuk duhet te shkruajme 1/dhjetor/1998. Gabim eshte edhe 2/dhjetor/1998."
        date_marking = check_for_a_written_date_rule(text)
        expected_date_markings = [{FROM_KEY: 23, TO_KEY: 37, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                                   DESCRIPTION_KEY: 'nuk vihet asnjë shenjë midis ditës, muajit dhe vitit, në datat e'
                                                    ' plota ku muaji shkruhet me shkronja',
                                   SUGGESTIONS_KEY: [{DISPLAY_KEY: "1 dhjetor 1998", ACTION_KEY: "1 dhjetor 1998"}]},
                                  {FROM_KEY: 56, TO_KEY: 70, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                                   DESCRIPTION_KEY: 'nuk vihet asnjë shenjë midis ditës, muajit dhe vitit, në datat e'
                                                    ' plota ku muaji shkruhet me shkronja',
                                   SUGGESTIONS_KEY: [{DISPLAY_KEY: "2 dhjetor 1998", ACTION_KEY: "2 dhjetor 1998"}]}]
        self.assertEqual(date_marking, expected_date_markings)

    def test_a_date7(self):
        text = "Nuk duhet te shkruajme as 1/dhjetor/1998, dhe as 5/mars/1998."
        expected_date_markings = [{FROM_KEY: 26, TO_KEY: 40, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                                   DESCRIPTION_KEY: 'nuk vihet asnjë shenjë midis ditës, muajit dhe vitit, në datat e'
                                                    ' plota ku muaji shkruhet me shkronja',
                                   SUGGESTIONS_KEY: [{DISPLAY_KEY: "1 dhjetor 1998", ACTION_KEY: "1 dhjetor 1998"}]},
                                  {FROM_KEY: 49, TO_KEY: 60, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                                   DESCRIPTION_KEY: 'nuk vihet asnjë shenjë midis ditës, muajit dhe vitit, në datat e'
                                                    ' plota ku muaji shkruhet me shkronja',
                                   SUGGESTIONS_KEY: [{DISPLAY_KEY: "5 mars 1998", ACTION_KEY: "5 mars 1998"}]}]
        date_marking = check_for_a_written_date_rule(text)
        self.assertEqual(date_marking, expected_date_markings)

    def test_a_date8(self):
        text = "Nuk duhet te shkruajme as 1/dhjetor/1998, dhe as 5/mars/1998, madje dhe as 8/shkurt/1998."
        expected_date_markings = [{FROM_KEY: 26, TO_KEY: 40, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                                   DESCRIPTION_KEY: 'nuk vihet asnjë shenjë midis ditës, muajit dhe vitit, në datat e'
                                                    ' plota ku muaji shkruhet me shkronja',
                                   SUGGESTIONS_KEY: [{DISPLAY_KEY: "1 dhjetor 1998", ACTION_KEY: "1 dhjetor 1998"}]},
                                  {FROM_KEY: 49, TO_KEY: 60, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                                   DESCRIPTION_KEY: 'nuk vihet asnjë shenjë midis ditës, muajit dhe vitit, në datat e'
                                                    ' plota ku muaji shkruhet me shkronja',
                                   SUGGESTIONS_KEY: [{DISPLAY_KEY: "5 mars 1998", ACTION_KEY: "5 mars 1998"}]},
                                  {FROM_KEY: 75, TO_KEY: 88, TYPE_KEY: TYPO_KEY,
                                   SUBTYPE_KEY: 'gabim gramatikor, shkrimi i datave',
                                   DESCRIPTION_KEY: 'nuk vihet asnjë shenjë midis ditës, muajit dhe vitit, në datat e'
                                                    ' plota ku muaji shkruhet me shkronja',
                                   SUGGESTIONS_KEY: [{DISPLAY_KEY: "8 shkurt 1998", ACTION_KEY: "8 shkurt 1998"}]}]
        date_marking = check_for_a_written_date_rule(text)
        self.assertEqual(date_marking, expected_date_markings)
