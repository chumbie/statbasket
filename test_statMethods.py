"""test_statMethods.py

Unit tests for statMethods.py

for list of TestCase assert methods visit:
https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug"""

# Standard Library Imports
import csv
import unittest

# Local Imports
from statMethods import StatMe as sm


class TestStatBasketClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        def create_large_dataset(rand_seed):
            from random import seed, randint
            seed(rand_seed)  # seeds random number generator (101), for replication
            return_list = list()
            for i in range(0, 100001):
                return_list.append(randint(1, 255))
            return tuple(return_list)
        cls.data_simple = (1, 2, 3, 4, 4, 5, 6, 10)
        cls.data_neg_float = (-1.0, -2.0, -3.0, -4.0, -4.0, -5.0, -6.0, -10.0)
        cls.data_pop_zeroes = (1, 2, 3, 4, 4, 5, 6, 10, 0, 0, 0, 0, 0)
        cls.data_large = create_large_dataset(101)
        cls.data_large2 = create_large_dataset(102)

    # 1
    def test_data_validations(self):
        """Test to make sure methods reject empty tuple"""
        # Gets all methods in class, minus dunders
        method_list_value_error = \
            [method for method in dir(sm) if method.startswith("__") is False]
        del method_list_value_error[4]  # removing dict, TypeErrors
        del method_list_value_error[19]
        del method_list_value_error[-1]
        del method_list_value_error[-1]
        method_list_type_error = ['get_data_diff', 'get_var_pool']
        # argument to pass to each
        data = ()

        with self.assertRaises(ValueError):
            sm.get_data_diff((1, 2, 3), (4, 5, 6, 7))
            for i in range(len(method_list_value_error)):
                statement = f"sm.{method_list_value_error[i]}(data)"
                exec(statement)

        with self.assertRaises(TypeError):
            for i in range(len(method_list_type_error)):
                statement = f"sm.{method_list_type_error[i]}(data)"
                exec(statement)
        del method_list_value_error, method_list_type_error, data

    # 2
    def test_get_n(self):
        self.assertEqual(sm.get_n(self.data_simple), 8)
        self.assertEqual(sm.get_n(self.data_neg_float), 8)
        self.assertEqual(sm.get_n(self.data_pop_zeroes), 13)
        self.assertEqual(sm.get_n(self.data_large), 100001)

    # 3
    def test_get_df(self):
        self.assertEqual(sm.get_df(self.data_simple), 7)
        self.assertEqual(sm.get_df(self.data_neg_float), 7)
        self.assertEqual(sm.get_df(self.data_pop_zeroes), 12)
        self.assertEqual(sm.get_df(self.data_large), 100000)

    # 4
    def test_get_min(self):
        self.assertEqual(sm.get_min(self.data_simple), 1)
        self.assertEqual(sm.get_min(self.data_neg_float), -10)
        self.assertEqual(sm.get_min(self.data_pop_zeroes), 0)
        self.assertEqual(sm.get_min(self.data_large), 1)

    # 5
    def test_get_max(self):
        self.assertEqual(sm.get_max(self.data_simple), 10)
        self.assertEqual(sm.get_max(self.data_neg_float), -1)
        self.assertEqual(sm.get_max(self.data_pop_zeroes), 10)
        self.assertEqual(sm.get_max(self.data_large), 255)

    # 6
    def test_get_range(self):
        self.assertEqual(sm.get_range(self.data_simple), 9)
        self.assertEqual(sm.get_range(self.data_neg_float), 9)
        self.assertEqual(sm.get_range(self.data_pop_zeroes), 10)
        self.assertEqual(sm.get_range(self.data_large), 254)

    # 7
    def test_get_mean(self):
        self.assertEqual(sm.get_mean(self.data_simple), 4.3750)
        self.assertEqual(sm.get_mean(self.data_neg_float), -4.3750)
        self.assertEqual(sm.get_mean(self.data_pop_zeroes), 2.69231)
        self.assertEqual(sm.get_mean(self.data_large), 128.319)

    # 8
    def test_get_median(self):
        self.assertEqual(sm.get_median(self.data_simple), 4)
        self.assertEqual(sm.get_median(self.data_neg_float), -4)
        self.assertEqual(sm.get_median(self.data_pop_zeroes), 2)
        self.assertEqual(sm.get_median(self.data_large), 129)

    # 9
    def test_get_mode(self):
        self.assertEqual(sm.get_mode(self.data_simple), (4,))
        self.assertEqual(sm.get_mode(self.data_neg_float), (-4,))
        self.assertEqual(sm.get_mode(self.data_pop_zeroes), (0,))
        self.assertEqual(sm.get_mode(self.data_large), (164,))

    # 10
    def test_get_skew(self):
        self.assertEqual(sm.get_skew(self.data_simple), 0.74917)
        self.assertEqual(sm.get_skew(self.data_neg_float), -0.74917)
        self.assertEqual(sm.get_skew(self.data_pop_zeroes), 0.90913)
        self.assertEqual(sm.get_skew(self.data_large), -0.01086)

    # 11
    def test_get_var(self):
        self.assertEqual(sm.get_var(self.data_simple), 7.69643)
        self.assertEqual(sm.get_var(self.data_neg_float), 7.69643)
        self.assertEqual(sm.get_var(self.data_pop_zeroes), 9.39744)
        self.assertEqual(sm.get_var(self.data_large), 5391.97076)

    # 12
    def test_get_stdev(self):
        self.assertEqual(sm.get_stdev(self.data_simple), 2.77424)
        self.assertEqual(sm.get_stdev(self.data_neg_float), 2.77424)
        self.assertEqual(sm.get_stdev(self.data_pop_zeroes), 3.06552)
        self.assertEqual(sm.get_stdev(self.data_large), 73.43004)

    # 13
    def test_get_sterr(self):
        self.assertEqual(sm.get_sterr(self.data_simple), 0.98084)
        self.assertEqual(sm.get_sterr(self.data_neg_float), 0.98084)
        self.assertEqual(sm.get_sterr(self.data_pop_zeroes), 0.85022)
        self.assertEqual(sm.get_sterr(self.data_large), 0.23221)

    # 14
    def test_get_cv(self):
        self.assertEqual(sm.get_cv(self.data_simple), 0.63411)
        self.assertEqual(sm.get_cv(self.data_neg_float), -0.63411)
        self.assertEqual(sm.get_cv(self.data_pop_zeroes), 1.13862)
        self.assertEqual(sm.get_cv(self.data_large), 0.57225)

    # 15
    def test_get_data_diff(self):
        self.assertEqual(sm.get_data_diff(self.data_simple, self.data_neg_float),
                                                    (2, 4, 6, 8, 8, 10, 12, 20))
        import csv
        csv_file = "get_data_diff_large.csv"
        with open(csv_file) as file:
            csv_reader = csv.reader(file)
            diff_data_list = list(csv_reader)

            for i in range(len(self.data_large)):
                self.assertEqual(
                    sm.get_data_diff((self.data_large[i],),
                                     (self.data_large2[i],)),
                    (int(diff_data_list[i][0]),))

    # 16
    def test_get_var_pool(self):
        self.assertEqual(sm.get_var_pool(self.data_simple, self.data_neg_float), 7.69643)
        self.assertEqual(sm.get_var_pool(self.data_large, self.data_large2, ), 5397.16249)

    # 17
    def test__get_lookup_df(self):
        self.assertEqual(sm._get_lookup_df(self.data_simple), 7)
        self.assertEqual(sm._get_lookup_df(self.data_neg_float), 7)
        self.assertEqual(sm._get_lookup_df(self.data_pop_zeroes), 12)
        self.assertEqual(sm._get_lookup_df(self.data_large), 999)

    # 18
    def test_get_score_critical(self):
        self.assertEqual(sm.get_score_critical(self.data_simple), 2.365)
        self.assertEqual(sm.get_score_critical(self.data_neg_float, cl=0.90), 1.895)
        self.assertEqual(sm.get_score_critical(
            self.data_pop_zeroes, cl=0.99, pop_var_known=True), 2.576)
        self.assertEqual(sm.get_score_critical(self.data_large), 1.96)

    # 19
    def test_get_moe(self):
        # for whatever reason, these tests are off by 1e-5
        # probably floating-point precision error
        self.assertEqual(sm.get_moe(self.data_simple), 2.31969)
        self.assertEqual(sm.get_moe(self.data_neg_float, cl=0.90), 1.85869)
        self.assertEqual(sm.get_moe(self.data_pop_zeroes, cl=0.99, pop_var_known=True), 2.19017)
        self.assertEqual(sm.get_moe(self.data_large), 0.45513)

    # 20
    def test_get_ci(self):
        # for whatever reason, these tests are off by exactly 1e-5
        # probably floating-point precision error
        self.assertEqual(sm.get_ci(self.data_simple), (2.05531, 6.69469))
        self.assertEqual(sm.get_ci(self.data_neg_float, cl=0.90), (-6.23369, -2.51631))
        self.assertEqual(sm.get_ci(self.data_pop_zeroes, cl=0.99, pop_var_known=True), (0.50214, 4.88248))
        self.assertEqual(sm.get_ci(self.data_large), (127.86387, 128.77413))

    # 21
    def test_get_score_hyp(self):

        with self.assertRaises(ValueError):
            sm.get_score_hyp((1, 2, 3), (4, 5, 6, 7), 0, samples_dependent=True)

        self.assertEqual(sm.get_score_hyp(self.data_simple), 4.46045)
        # this one's off by 2e-5
        self.assertEqual(sm.get_score_hyp(self.data_large), 552.61081)
        # this one is off significantly, per LibreOffice 1.57253
        self.assertEqual(sm.get_score_hyp(self.data_large, self.data_large2, samples_dependent=True), 1.57366)
        # off by 1e-5
        self.assertEqual(sm.get_score_hyp(self.data_large, self.data_large2), 1.57366)
        # off by 1e-5
        self.assertEqual(sm.get_score_hyp(self.data_simple, self.data_neg_float), 6.30802)


if __name__ == "__main__":
    unittest.main()
