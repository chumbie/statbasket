"""test_ctDescStats.py

Unit tests for ctDescStats.py

for list of TestCase assert methods visit:
https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug"""

# Standard Library Imports
import unittest
# Third-Party Imports
from ctDescStats import DescriptiveStats as ds


class TestDescrtiptiveStatsClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_simple = ds((1, 2, 3, 4, 4, 5, 6, 10))
        cls.data_negatives = ds((-1, -2, -3, -4, -4, -5, -6, -10), cl=0.98)
        cls.data_with_zeroes = ds((1, 2, 3, 4, 4, 5, 6, 10, 0, 0, 0, 0, 0), cl=0.99)

    def test_data_validations(self):
        self.assertEqual(self.data_simple.n, 8)
        self.assertEqual(self.data_with_zeroes.n, 13)
        self.assertEqual(self.data_simple.df, 7)
        self.assertEqual(self.data_with_zeroes.df, 12)
        with self.assertRaises(AssertionError):
            ds((1, 2, 3), cl=0.97)
            ds((1, 2, 3), cl="spaghetti")
            ds((1, 2, 3), data_name=7)
            ds((1, 2, 3), data_name=True)
            ds((1, 2, 3), data_name=6.022)

    def test_t_score_calculate(self):
        self.assertEqual(self.data_simple.t_score_calculate(), 2.365)
        self.assertEqual(self.data_negatives.t_score_calculate(), 2.988)
        self.assertEqual(self.data_with_zeroes.t_score_calculate(), 3.055)

    def test_mean_calculate(self):
        self.assertEqual(self.data_simple.mean_calculate(), 4.375)
        self.assertEqual(self.data_negatives.mean_calculate(), -4.375)
        self.assertEqual(round(self.data_with_zeroes.mean_calculate(), 4), 2.6923)

    def test_median_calculate(self):
        self.assertEqual(self.data_simple.median_calculate(), 4)
        self.assertEqual(self.data_negatives.median_calculate(), -4)
        self.assertEqual(self.data_with_zeroes.median_calculate(), 2)

    def test_mode_calculate(self):
        self.assertEqual(self.data_simple.mode_calculate(), (4,))
        self.assertEqual(self.data_negatives.mode_calculate(), (-4,))
        self.assertEqual(self.data_with_zeroes.mode_calculate(), (0,))
        self.assertEqual(ds((1, 1, 2, 2)).mode_calculate(), (1, 2))

    def test_min_max_and_range(self):
        self.assertEqual((self.data_simple.min,
                          self.data_simple.max,
                          self.data_simple.range), (1, 10, 9))
        self.assertEqual((self.data_negatives.min,
                          self.data_negatives.max,
                          self.data_negatives.range), (-10, -1, 9))
        self.assertEqual((self.data_with_zeroes.min,
                          self.data_with_zeroes.max,
                          self.data_with_zeroes.range), (0, 10, 10))

    def test_variance_calculate(self):
        self.assertEqual(self.data_simple.variance_calculate(), 7.696)
        self.assertEqual(self.data_negatives.variance_calculate(), 7.696)
        self.assertEqual(self.data_with_zeroes.variance_calculate(), 9.397)

    def test_standard_deviation_calculate(self):
        self.assertEqual(self.data_simple.standard_deviation_calculate(), 2.774)


if __name__ == "__main__":
    ds((1, 2, 3, 4, 4, 5, 6, 10)).t_score_calculate()
    unittest.main()