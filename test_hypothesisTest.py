"""test_zTable.py

Unit tests for zTable function(s).

for list of TestCase assert methods visit:
https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug"""

# Standard Library Imports
import unittest
# Third-Party Imports
from hypothesisTest import HypothesisTest as ht


class ZTablePValueFunctionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.positive_z_score_not_significant = 1.01
        cls.positive_z_score_significant = 3.17
        cls.positive_z_score_large = 521.00
        cls.negative_z_score_not_significant = -1.01
        cls.negative_z_score_significant = -3.17
        cls.negative_z_score_large = -512.00
        cls.nonsense_z_score = "spaghetti"

    def test_p_value_function_data_validation(self):
        with self.assertRaises(AssertionError):
            p_value(self.nonsense_z_score)

    def test_p_value_function_left_tail(self):
        tail = "left"
        self.assertEqual(p_value(self.positive_z_score_not_significant, tail=tail), 0.8438)
        self.assertEqual(p_value(self.positive_z_score_significant, tail=tail), 0.9992)
        self.assertEqual(p_value(self.positive_z_score_large, tail=tail), 0.9999)
        self.assertEqual(p_value(self.negative_z_score_not_significant, tail=tail), 0.1562)
        self.assertEqual(p_value(self.negative_z_score_significant, tail=tail), 0.0008)
        self.assertEqual(p_value(self.negative_z_score_large, tail=tail), 0.0001)

    def test_p_value_function_right_tail(self):
        tail = "right"
        self.assertEqual(p_value(self.positive_z_score_not_significant, tail=tail), 0.1562)
        self.assertEqual(p_value(self.positive_z_score_significant, tail=tail), 0.0008)
        self.assertEqual(p_value(self.positive_z_score_large, tail=tail), 0.0001)
        self.assertEqual(p_value(self.negative_z_score_not_significant, tail=tail), 0.8438)
        self.assertEqual(p_value(self.negative_z_score_significant, tail=tail), 0.9992)
        self.assertEqual(p_value(self.negative_z_score_large, tail=tail), 0.9999)

    def test_p_value_function_two_tail(self):
        tail = "two"
        self.assertEqual(p_value(self.positive_z_score_not_significant, tail=tail), 0.3124)
        self.assertEqual(p_value(self.positive_z_score_significant, tail=tail), 0.0016)
        self.assertEqual(p_value(self.positive_z_score_large, tail=tail), 0.0001)
        self.assertEqual(p_value(self.negative_z_score_not_significant, tail=tail), 0.3124)
        self.assertEqual(p_value(self.negative_z_score_significant, tail=tail), 0.0016)
        self.assertEqual(p_value(self.negative_z_score_large, tail=tail), 0.0001)


if __name__ == "__main__":
    unittest.main()
