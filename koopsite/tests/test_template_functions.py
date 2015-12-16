from django.test import TestCase
from koopsite.functions import round_up_division


class FunctionsTest(TestCase):

    def test_round_up_division(self):
        self.assertEqual(round_up_division(5, 5), 1)
        self.assertEqual(round_up_division(101, 100), 2)
        self.assertEqual(round_up_division(200, 100), 2)
        self.assertEqual(round_up_division(100.001, 100), 2)
        self.assertEqual(round_up_division(100.001, 100.001), 1)