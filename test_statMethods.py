"""test_statMethods.py

Unit tests for statMethods.py

for list of TestCase assert methods visit:
https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug"""

# Standard Library Imports
import unittest

# Third-Party Imports
from statMethods import StatMe as sm


class TestStatBasketClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.data_simple = sm((1, 2, 3, 4, 4, 5, 6, 10)),
        cls.data_negatives = sm((-1, -2, -3, -4, -4, -5, -6, -10), cl=0.90),
        cls.data_population_zeroes = sm((1, 2, 3, 4, 4, 5, 6, 10, 0, 0, 0, 0, 0), cl=0.99, is_population=True)

        cls.data_dict = [cls.data_simple,
                         cls.data_negatives,
                         cls.data_population_zeroes]

    def test_data_validations(self):
        with self.assertRaises(AssertionError):
            sm(4)
            sm((1, 2, 3), cl=0.98)
            sm((1, 2, 3), cl="spaghetti")
            sm((1, 2, 3), tail="spaghetti")
            sm((1, 2, 3), first_name=7)
            sm((1, 2, 3), first_name=True)
            sm((1, 2, 3), first_name=6.022)

    def test_get_lookup_df(self):
        self.assertEqual(self.data_simple.n, 8)
        self.assertEqual(self.data_population_zeroes.n, 13)
        self.assertEqual(self.data_simple._dflookup, 7)
        self.assertEqual(self.data_population_zeroes._dflookup, 999)

    def test_mean_calculation(self):
        self.assertEqual(self.data_simple.mean, 4.375)
        self.assertEqual(self.data_negatives.mean, -4.375)
        self.assertEqual(round(self.data_population_zeroes.mean, 4), 2.6923)

    def test_median_calculation(self):
        self.assertEqual(self.data_simple.median, 4)
        self.assertEqual(self.data_negatives.median, -4)
        self.assertEqual(self.data_population_zeroes.median, 2)

    def test_mode_calculation(self):
        self.assertEqual(self.data_simple.mode, (4,))
        self.assertEqual(self.data_negatives.mode, (-4,))
        self.assertEqual(self.data_population_zeroes.mode, (0,))
        self.assertEqual(sm((1, 1, 2, 2)).mode, (1, 2))

    def test_min_max_and_range(self):
        self.assertEqual((self.data_simple.min,
                          self.data_simple.max,
                          self.data_simple.range), (1, 10, 9))
        self.assertEqual((self.data_negatives.min,
                          self.data_negatives.max,
                          self.data_negatives.range), (-10, -1, 9))
        self.assertEqual((self.data_population_zeroes.min,
                          self.data_population_zeroes.max,
                          self.data_population_zeroes.range), (0, 10, 10))

    def test_variance_calculation(self):
        self.assertEqual(round(self.data_simple.var, 4), 7.6964)
        self.assertEqual(round(self.data_negatives.var, 4), 7.6964)
        self.assertEqual(round(self.data_population_zeroes.var, 4), 8.6746)

    def test_standard_deviation_calculation(self):
        self.assertEqual(round(self.data_simple.stdev, 4), 2.7742)
        self.assertEqual(round(self.data_negatives.stdev, 4), 2.7742)
        self.assertEqual(round(self.data_population_zeroes.stdev, 4), 2.9453)

    def test_standard_error_calculation(self):
        self.assertEqual(round(self.data_simple.sterr, 4), 0.9808)
        self.assertEqual(round(self.data_negatives.sterr, 4), 0.9808)
        self.assertEqual(round(self.data_population_zeroes.sterr, 4), 0.8169)

    def test_coeff_of_var_calculation(self):
        self.assertEqual(round(self.data_simple.cv, 4), 0.6341)
        self.assertEqual(round(self.data_negatives.cv, 4), -0.6341)
        self.assertEqual(round(self.data_population_zeroes.cv, 4), 1.094)

    def test_skewness_calculation(self):
        self.assertEqual(round(self.data_simple.skew, 4), 0.7492)
        self.assertEqual(round(self.data_negatives.skew, 4), -0.7492)
        self.assertEqual(round(self.data_population_zeroes.skew, 4), 1.0251)

    def test_score_calculations(self):
        self.assertEqual((self.data_simple.score_type,
                          self.data_simple.score_critical), ("t", 2.365))
        self.assertEqual((self.data_negatives.score_type,
                          self.data_negatives.score_critical), ("t", 1.895))
        self.assertEqual((self.data_population_zeroes.score_type,
                          self.data_population_zeroes.score_critical), ("z", 2.576))

    def test_confidence_interval_calculation(self):
        self.assertEqual(  # data_simple
            (round(self.data_simple.moe, 4),
             round(self.data_simple.ci[0], 4),
             round(self.data_simple.ci[1], 4)), (2.3197, 2.0553, 6.6947))
        self.assertEqual(  # data_negatives
            (round(self.data_negatives.moe, 4),
             round(self.data_negatives.ci[0], 4),
             round(self.data_negatives.ci[1], 4)), (1.8587, -6.2337, -2.5163))
        self.assertEqual(  # data_population_zeroes
            (round(self.data_population_zeroes.moe, 4),
             round(self.data_population_zeroes.ci[0], 4),
             round(self.data_population_zeroes.ci[1], 4)), (2.1043, 0.5881, 4.7966))


if __name__ == "__main__":
    unittest.main()
