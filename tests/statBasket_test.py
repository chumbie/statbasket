"""test_statMethods.py

Unit tests for statMethods.py

for list of TestCase assert methods visit:
https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug"""

# Standard Library Imports
import unittest
import sys

# Local Imports
sys.path.append("..")  # so path can see the project
from src.statBasket import StatBasket as SB


class TestStatBasketClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        def create_large_dataset(rand_seed, size=100001, max_int=255):
            from random import seed, randint
            seed(rand_seed)  # seeds random number generator for replication (101)
            return_list = list()
            for i in range(0, size):
                return_list.append(randint(1, max_int))
            return tuple(return_list)
        cls._data_large1 = create_large_dataset(101)
        cls._data_large2 = create_large_dataset(102)

    def test_1_data_validations(self):
        with self.assertRaises(ValueError):
            SB(4)
            SB((1, 2, 3), cl=0.98)
            SB((1, 2, 3), cl="spaghetti")
            SB((1, 2, 3), tail="spaghetti")
            SB((1, 2, 3), data_name=7)
            SB((1, 2, 3), second_data_name=True)
            SB((1, 2, 3), data_name=None, second_data_name=True)

    def test_2_small_cl_95(self):
        data = (1, 2, 3, 4, 4, 5, 6, 10)
        small = SB(data)
        self.assertEqual(small.n, 8)
        self.assertEqual(small.df, 7)
        self.assertEqual(small.score_critical, 2.365)
        self.assertEqual(small.mean, 4.37500000000)
        self.assertEqual(small.median, 4)
        self.assertEqual(small.mode, 4)
        self.assertEqual(small.min, 1)
        self.assertEqual(small.max, 10)
        self.assertEqual(small.range, 9)
        self.assertEqual(small.var, 7.6964285714)
        self.assertEqual(small.stdev, 2.7742437837)
        self.assertEqual(small.sterr, 0.9808432961)
        self.assertEqual(small.cv, 0.6341128648)
        self.assertEqual(small.skew, 0.7491694791)
        # same errors we see with statMethods, 1e-5 difference (float err?)
        self.assertEqual(small.moe, 2.3196943953)
        self.assertEqual(small.ci, (2.0553056047, 6.6946943953))
        del data

    def test_3_small_negatives_cl_90(self):
        data = (-1.0, -2.0, -3.0, -4.0, -4.0, -5.0, -6.0, -10.0)
        small_neg_floats_cl_90 = SB(data, cl=0.90)
        self.assertEqual(small_neg_floats_cl_90.n, 8)
        self.assertEqual(small_neg_floats_cl_90.df, 7)
        self.assertEqual(small_neg_floats_cl_90.score_critical, 1.895)
        self.assertEqual(small_neg_floats_cl_90.mean, -4.37500)
        self.assertEqual(small_neg_floats_cl_90.median, -4)
        self.assertEqual(small_neg_floats_cl_90.mode, -4)
        self.assertEqual(small_neg_floats_cl_90.min, -10)
        self.assertEqual(small_neg_floats_cl_90.max, -1)
        self.assertEqual(small_neg_floats_cl_90.range, 9)
        self.assertEqual(small_neg_floats_cl_90.var, 7.6964285714)
        self.assertEqual(small_neg_floats_cl_90.stdev, 2.7742437837)
        self.assertEqual(small_neg_floats_cl_90.sterr, 0.9808432961)
        self.assertEqual(small_neg_floats_cl_90.cv, -0.6341128648)
        self.assertEqual(small_neg_floats_cl_90.skew, -0.7491694791)
        self.assertEqual(small_neg_floats_cl_90.moe, 1.8586980461)
        # same errors we see with statMethods, 1e-5 difference (float err?)
        self.assertEqual(small_neg_floats_cl_90.ci, (-6.2336980461, -2.5163019539))
        del data

    def test_4_small_zeroes_population_true_cl_99(self):
        data = (1, 2, 3, 4, 4, 5, 6, 10, 0, 0, 0, 0, 0)
        small_zeroes_pop_true_cl_99 = SB(data, is_population=True, cl=0.99)
        self.assertEqual(small_zeroes_pop_true_cl_99.n, 13)
        self.assertEqual(small_zeroes_pop_true_cl_99.df, 12)
        self.assertEqual(small_zeroes_pop_true_cl_99.score_critical, 2.576)
        self.assertEqual(small_zeroes_pop_true_cl_99.mean, 2.69230769230)
        self.assertEqual(small_zeroes_pop_true_cl_99.median, 2)
        self.assertEqual(small_zeroes_pop_true_cl_99.mode, 0)
        self.assertEqual(small_zeroes_pop_true_cl_99.min, 0)
        self.assertEqual(small_zeroes_pop_true_cl_99.max, 10)
        self.assertEqual(small_zeroes_pop_true_cl_99.range, 10)
        self.assertEqual(small_zeroes_pop_true_cl_99.var, 8.6745562130)
        self.assertEqual(small_zeroes_pop_true_cl_99.stdev, 3.0655237558)
        self.assertEqual(small_zeroes_pop_true_cl_99.sterr, 0.8502233144)
        self.assertEqual(small_zeroes_pop_true_cl_99.cv, 1.1386231093)
        self.assertEqual(small_zeroes_pop_true_cl_99.skew, 0.9091294842)
        # same errors we see with statMethods, 1e-5 difference (float err?)
        self.assertEqual(small_zeroes_pop_true_cl_99.moe, 2.1901752579)
        self.assertEqual(small_zeroes_pop_true_cl_99.ci, (0.5021324344, 4.8824829502))
        del data

    def test_5_dependent_data_sets(self):
        data1 = (1, 2, 3, 4, 4, 5, 6, 10)
        data2 = (-1.0, -2.0, -3.0, -4.0, -4.0, -5.0, -6.0, -10.0)
        two_sets_dependent = SB(data1, data2, samples_dependent=True)
        self.assertEqual(two_sets_dependent.n, 8)
        self.assertEqual(two_sets_dependent.df, 7)
        self.assertEqual(two_sets_dependent.score_critical, 2.365)
        self.assertEqual(two_sets_dependent.mean, 8.75000000000)
        self.assertEqual(two_sets_dependent.median, 8)
        self.assertEqual(two_sets_dependent.mode, 8)
        self.assertEqual(two_sets_dependent.min, 2)
        self.assertEqual(two_sets_dependent.max, 20)
        self.assertEqual(two_sets_dependent.range, 18)
        self.assertEqual(two_sets_dependent.var, 30.7857142857)
        self.assertEqual(two_sets_dependent.stdev, 5.5484875674)
        self.assertEqual(two_sets_dependent.sterr, 1.9616865921)
        self.assertEqual(two_sets_dependent.cv, 0.6341128648)
        self.assertEqual(two_sets_dependent.skew, 0.7491694791)
        # same errors we see with statMethods, 1e-5 difference (float err?)
        self.assertEqual(two_sets_dependent.moe, 4.6393887903)
        self.assertEqual(two_sets_dependent.ci, (4.1106112097, 13.3893887903))

    def test_6_large_independent_data(self):
        data_large1 = self._data_large1
        data_large2 = self._data_large2
        two_large_independent = SB(data_large1, data_large2)

        # Large Data Set 1 (data_x)
        self.assertEqual(two_large_independent.n_x, 100001)
        self.assertEqual(two_large_independent.df_x, 100000)
        self.assertEqual(two_large_independent.score_critical_x, 1.96)
        self.assertEqual(two_large_independent.mean_x, 128.31899681000)
        self.assertEqual(two_large_independent.median_x, 129)
        self.assertEqual(two_large_independent.mode_x, 164)
        self.assertEqual(two_large_independent.min_x, 1)
        self.assertEqual(two_large_independent.max_x, 255)
        self.assertEqual(two_large_independent.range_x, 254)
        self.assertEqual(two_large_independent.var_x, 5391.9707600182)
        self.assertEqual(two_large_independent.stdev_x, 73.4300399021)
        self.assertEqual(two_large_independent.sterr_x, 0.2322050137)
        self.assertEqual(two_large_independent.cv_x, 0.5722460565)
        self.assertEqual(two_large_independent.skew_x, -0.0108565339)
        # same errors we see with statMethods, 1e-5 difference (float err?)
        self.assertEqual(two_large_independent.moe_x, 0.4551218269)
        self.assertEqual(two_large_independent.ci_x, (127.8638749831, 128.7741186369))

        # Large Data Set 2 (data_y)
        self.assertEqual(two_large_independent.n_y, 100001)
        self.assertEqual(two_large_independent.df_y, 100000)
        self.assertEqual(two_large_independent.score_critical_y, 1.96)
        self.assertEqual(two_large_independent.mean_y, 127.8019819802)
        self.assertEqual(two_large_independent.median_y, 128)
        self.assertEqual(two_large_independent.mode_y, 34)
        self.assertEqual(two_large_independent.min_y, 1)
        self.assertEqual(two_large_independent.max_y, 255)
        self.assertEqual(two_large_independent.range_y, 254)
        self.assertEqual(two_large_independent.var_y, 5402.3542284717)
        self.assertEqual(two_large_independent.stdev_y, 73.5007090338)
        self.assertEqual(two_large_independent.sterr_y, 0.2324284880)
        self.assertEqual(two_large_independent.cv_y, 0.5751139998)
        self.assertEqual(two_large_independent.skew_y, 0.0013020818)
        # same errors we see with statMethods, 1e-5 difference (float err?)
        self.assertEqual(two_large_independent.moe_y, 0.4555598365)
        self.assertEqual(two_large_independent.ci_y, (127.3464221437, 128.2575418167))

    def test_7_pooled_variance(self):
        data1 = (1, 2, 3, 4, 4, 5, 6, 10)
        data2 = (-1.0, -2.0, -3.0, -4.0, -4.0, -5.0, -6.0, -10.0)
        two_sets_pooled = SB(data1, data2)
        self.assertEqual(two_sets_pooled.var_pool, 7.6964285714)

    def test_8_test_score_calculation(self):
        data1 = (1, 2, 3, 4, 4, 5, 6, 10)
        data2 = (-1.0, -2.0, -3.0, -4.0, -4.0, -5.0, -6.0, -10.0)
        hyp_test_one_small = SB(data1)
        hyp_test_two_small = SB(data1, data2)
        hyp_test_two_small_dep = SB(data1, second_data_set=data2, samples_dependent=True)

        self.assertEqual(hyp_test_one_small.calculate_test_score(), 4.4604474717)
        self.assertEqual(hyp_test_two_small.calculate_test_score(), 6.3080253087)
        self.assertEqual(hyp_test_two_small_dep.calculate_test_score(), 4.4604474717)


if __name__ == "__main__":
    unittest.main()
