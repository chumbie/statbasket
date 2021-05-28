"""test_statMethods.py

Unit tests for statMethods.py

for list of TestCase assert methods visit:
https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug"""

# Standard Library Imports
import unittest
import sys

# Local Imports
sys.path.append("..")  # so path can see the project
from statbasket.statBasket import StatBasket as SB


class TestStatBasketClass(unittest.TestCase):

    @staticmethod
    def create_large_dataset(rand_seed):
        """Generates a list with uniformly distributed integers"""
        from random import seed, randint
        seed(rand_seed)  # seeds random number generator (101), for replication
        return_list = list()
        for i in range(0, 100001):
            return_list.append(randint(1, 255))
        return tuple(return_list)

    @staticmethod
    def get_data_dict(filename_: str):
        from csv import reader
        with open(filename_) as file:
            CSVReader = reader(file)
            data_table = list(CSVReader)
            # Stores the data returned by program
            data_dict = dict()
            # create list of column names, which will be len(row) - 1
            column_names_list = list()
            # capture name of statistic (row)
            stat_type = str()
            for i in range(len(data_table)):
                for j in range(len(data_table[i])):
                    value = data_table[i][j]
                    if i == 0:
                        if j > 0:
                            # ignore first column, turn columns into list
                            column_names_list.append(value)
                            # add column names with empty dict to data_dict
                            data_dict[value] = dict()
                    else:
                        if j == 0:
                            # first in row is data name
                            stat_type = str(value)
                        else:
                            # column_names_list[j-1] = sample/column name
                            # stat_type = type of data for sample
                            # for the above data name, add value to sample data_dict
                            data_dict[column_names_list[j - 1]][stat_type] = value
        return data_dict

    @classmethod
    def setUpClass(cls):

        cls.data_large1 = cls.create_large_dataset(101)
        cls.data_large2 = cls.create_large_dataset(102)

        # number of places after decimal to compare results
        cls.sig_deci_places = 10

        # Get the confirmed correct stats, computed with libreOffice Calc

        filename = 'tests/test_stats_for_import.csv'
        # to retrieve data, use self.data_dict[sample_name][stat_type]
        # self.data_dict['data_simple']['n'] = 8
        cls.data_dict = cls.get_data_dict(filename)

        # for multi-data stats
        cls.data_dict_multi = cls.get_data_dict('tests/test_stats_for_import_multi.csv')

    def test_1_data_validations(self):
        with self.assertRaises(ValueError):
            SB(4)
            SB((1, 2, 3), cl=0.98)
            SB((1, 2, 3), cl="spaghetti")
            SB((1, 2, 3), tail="spaghetti")
            SB((1, 2, 3), data_name=7)
            SB((1, 2, 3), second_data_name=True)
            SB((1, 2, 3), data_name=None, second_data_name=True)

    def test_2_simple_cl_95(self):

        data = (1, 2, 3, 4, 4, 5, 6, 10)
        simple = SB(data)
        self.assertAlmostEqual(simple.n,
                               float(self.data_dict["data_simple"]["n"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(simple.df,
                               float(self.data_dict["data_simple"]["df"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(simple.mean,
                               float(self.data_dict["data_simple"]["mean"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(simple.median,
                               float(self.data_dict["data_simple"]["median"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(simple.mode,
                               float(self.data_dict["data_simple"]["mode"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(simple.min,
                               float(self.data_dict["data_simple"]["min"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(simple.max,
                               float(self.data_dict["data_simple"]["max"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(simple.range,
                               float(self.data_dict["data_simple"]["range"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(simple.var,
                               float(self.data_dict["data_simple"]["var"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(simple.stdev,
                               float(self.data_dict["data_simple"]["stdev"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(simple.sterr,
                               float(self.data_dict["data_simple"]["sterr"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(simple.cv,
                               float(self.data_dict["data_simple"]["cv"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(simple.skew,
                               float(self.data_dict["data_simple"]["skew"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(simple.moe,
                               float(self.data_dict["data_simple"]["moe"]),
                               places=self.sig_deci_places)
        true_simple_lower = float(self.data_dict["data_simple"]["ci_lower"])
        true_simple_upper = float(self.data_dict["data_simple"]["ci_upper"])
        self.assertAlmostEqual(simple.ci[0], true_simple_lower, places=self.sig_deci_places)
        self.assertAlmostEqual(simple.ci[1], true_simple_upper, places=self.sig_deci_places)
        self.assertAlmostEqual(simple.score_critical, float(self.data_dict["data_simple"]["score_critical"]),
                               places=self.sig_deci_places)
        del data

    def test_3_negatives_cl_90(self):
        data = (-1.0, -2.0, -3.0, -4.0, -4.0, -5.0, -6.0, -10.0)
        neg_float_cl90 = SB(data, cl=0.90)
        self.assertAlmostEqual(neg_float_cl90.n,
                               float(self.data_dict["data_negatives"]["n"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.df,
                               float(self.data_dict["data_negatives"]["df"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.mean,
                               float(self.data_dict["data_negatives"]["mean"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.median,
                               float(self.data_dict["data_negatives"]["median"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.mode,
                               float(self.data_dict["data_negatives"]["mode"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.min,
                               float(self.data_dict["data_negatives"]["min"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.max,
                               float(self.data_dict["data_negatives"]["max"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.range,
                               float(self.data_dict["data_negatives"]["range"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.var,
                               float(self.data_dict["data_negatives"]["var"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.stdev,
                               float(self.data_dict["data_negatives"]["stdev"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.sterr,
                               float(self.data_dict["data_negatives"]["sterr"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.cv,
                               float(self.data_dict["data_negatives"]["cv"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.skew,
                               float(self.data_dict["data_negatives"]["skew"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.moe,
                               float(self.data_dict["data_negatives"]["moe"]),
                               places=self.sig_deci_places)
        true_neg_float_cl90_lower = float(self.data_dict["data_negatives"]["ci_lower"])
        true_neg_float_cl90_upper = float(self.data_dict["data_negatives"]["ci_upper"])
        self.assertAlmostEqual(neg_float_cl90.ci[0], true_neg_float_cl90_lower, places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.ci[1], true_neg_float_cl90_upper, places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.score_critical, float(self.data_dict["data_negatives"]["score_critical"]),
                               places=self.sig_deci_places)
        del data

    def test_4_zeroes_population_true_cl_99(self):
        data = (1, 2, 3, 4, 4, 5, 6, 10, 0, 0, 0, 0, 0)
        zeroes_pop_cl99 = SB(data, cl=0.99, is_population=True)
        self.assertAlmostEqual(zeroes_pop_cl99.n,
                               float(self.data_dict["data_zeroes_pop"]["n"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.df,
                               float(self.data_dict["data_zeroes_pop"]["df"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.mean,
                               float(self.data_dict["data_zeroes_pop"]["mean"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.median,
                               float(self.data_dict["data_zeroes_pop"]["median"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.mode,
                               float(self.data_dict["data_zeroes_pop"]["mode"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.min,
                               float(self.data_dict["data_zeroes_pop"]["min"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.max,
                               float(self.data_dict["data_zeroes_pop"]["max"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.range,
                               float(self.data_dict["data_zeroes_pop"]["range"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.var,
                               float(self.data_dict["data_zeroes_pop"]["var"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.stdev,
                               float(self.data_dict["data_zeroes_pop"]["stdev"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.sterr,
                               float(self.data_dict["data_zeroes_pop"]["sterr"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.cv,
                               float(self.data_dict["data_zeroes_pop"]["cv"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.skew,
                               float(self.data_dict["data_zeroes_pop"]["skew"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.moe,
                               float(self.data_dict["data_zeroes_pop"]["moe"]),
                               places=self.sig_deci_places)
        true_neg_float_cl90_lower = float(self.data_dict["data_zeroes_pop"]["ci_lower"])
        true_neg_float_cl90_upper = float(self.data_dict["data_zeroes_pop"]["ci_upper"])
        self.assertAlmostEqual(zeroes_pop_cl99.ci[0],
                               true_neg_float_cl90_lower,
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.ci[1],
                               true_neg_float_cl90_upper,
                               places=self.sig_deci_places)
        self.assertAlmostEqual(zeroes_pop_cl99.score_critical,
                               float(self.data_dict["data_zeroes_pop"]["score_critical"]),
                               places=self.sig_deci_places)
        del data

    def test_5_dependent_data_sets(self):
        data1 = (1, 2, 3, 4, 4, 5, 6, 10)
        data2 = (-10.0, -6.0, -5.0, -4.0, -4.0, -3.0, -2.0, -1.0)
        two_sets_dep = SB(data1, data2, samples_dependent=True)
        self.assertAlmostEqual(two_sets_dep.n_diff,
                               float(self.data_dict["small_data_diff"]["n"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.df_diff,
                               float(self.data_dict["small_data_diff"]["df"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.mean_diff,
                               float(self.data_dict["small_data_diff"]["mean"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.median_diff,
                               float(self.data_dict["small_data_diff"]["median"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.mode_diff,
                               float(self.data_dict["small_data_diff"]["mode"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.min_diff,
                               float(self.data_dict["small_data_diff"]["min"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.max_diff,
                               float(self.data_dict["small_data_diff"]["max"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.range_diff,
                               float(self.data_dict["small_data_diff"]["range"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.var_diff,
                               float(self.data_dict["small_data_diff"]["var"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.stdev_diff,
                               float(self.data_dict["small_data_diff"]["stdev"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.sterr_diff,
                               float(self.data_dict["small_data_diff"]["sterr"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.cv_diff,
                               float(self.data_dict["small_data_diff"]["cv"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.skew_diff,
                               float(self.data_dict["small_data_diff"]["skew"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.moe_diff,
                               float(self.data_dict["small_data_diff"]["moe"]),
                               places=self.sig_deci_places)
        true_neg_float_cl90_lower = float(self.data_dict["small_data_diff"]["ci_lower"])
        true_neg_float_cl90_upper = float(self.data_dict["small_data_diff"]["ci_upper"])
        self.assertAlmostEqual(two_sets_dep.ci_diff[0],
                               true_neg_float_cl90_lower,
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.ci_diff[1],
                               true_neg_float_cl90_upper,
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_sets_dep.score_critical_diff,
                               float(self.data_dict["small_data_diff"]["score_critical"]),
                               places=self.sig_deci_places)
        del data1, data2

    def test_6_large_independent_data(self):
        large1 = self.data_large1
        large2 = self.data_large2
        two_large_ind = SB(large1, large2)

        # Large Data Set 1 (data_x)
        self.assertAlmostEqual(two_large_ind.n_x,
                               float(self.data_dict["large_data_1"]["n"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.df_x,
                               float(self.data_dict["large_data_1"]["df"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.mean_x,
                               float(self.data_dict["large_data_1"]["mean"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.median_x,
                               float(self.data_dict["large_data_1"]["median"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.mode_x,
                               float(self.data_dict["large_data_1"]["mode"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.min_x,
                               float(self.data_dict["large_data_1"]["min"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.max_x,
                               float(self.data_dict["large_data_1"]["max"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.range_x,
                               float(self.data_dict["large_data_1"]["range"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.var_x,
                               float(self.data_dict["large_data_1"]["var"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.stdev_x,
                               float(self.data_dict["large_data_1"]["stdev"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.sterr_x,
                               float(self.data_dict["large_data_1"]["sterr"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.cv_x,
                               float(self.data_dict["large_data_1"]["cv"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.skew_x,
                               float(self.data_dict["large_data_1"]["skew"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.moe_x,
                               float(self.data_dict["large_data_1"]["moe"]),
                               places=self.sig_deci_places)
        true_neg_float_cl90_lower = float(self.data_dict["large_data_1"]["ci_lower"])
        true_neg_float_cl90_upper = float(self.data_dict["large_data_1"]["ci_upper"])
        self.assertAlmostEqual(two_large_ind.ci_x[0], true_neg_float_cl90_lower,
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.ci_x[1], true_neg_float_cl90_upper,
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.score_critical_x,
                               float(self.data_dict["large_data_1"]["score_critical"]),
                               places=self.sig_deci_places)

        # Large Data Set 2 (data_y)
        self.assertAlmostEqual(two_large_ind.n_y,
                               float(self.data_dict["large_data_2"]["n"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.df_y,
                               float(self.data_dict["large_data_2"]["df"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.mean_y,
                               float(self.data_dict["large_data_2"]["mean"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.median_y,
                               float(self.data_dict["large_data_2"]["median"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.mode_y,
                               float(self.data_dict["large_data_2"]["mode"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.min_y,
                               float(self.data_dict["large_data_2"]["min"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.max_y,
                               float(self.data_dict["large_data_2"]["max"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.range_y,
                               float(self.data_dict["large_data_2"]["range"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.var_y,
                               float(self.data_dict["large_data_2"]["var"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.stdev_y,
                               float(self.data_dict["large_data_2"]["stdev"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.sterr_y,
                               float(self.data_dict["large_data_2"]["sterr"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.cv_y,
                               float(self.data_dict["large_data_2"]["cv"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.skew_y,
                               float(self.data_dict["large_data_2"]["skew"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.moe_y,
                               float(self.data_dict["large_data_2"]["moe"]),
                               places=self.sig_deci_places)
        true_neg_float_cl90_lower = float(self.data_dict["large_data_2"]["ci_lower"])
        true_neg_float_cl90_upper = float(self.data_dict["large_data_2"]["ci_upper"])
        self.assertAlmostEqual(two_large_ind.ci_y[0], true_neg_float_cl90_lower,
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.ci_y[1], true_neg_float_cl90_upper,
                               places=self.sig_deci_places)
        self.assertAlmostEqual(two_large_ind.score_critical_y,
                               float(self.data_dict["large_data_2"]["score_critical"]),
                               places=self.sig_deci_places)
        del large1, large2

    def test_7_pooled_variance(self):
        data1 = (1, 2, 3, 4, 4, 5, 6, 10)
        data2 = (-1.0, -2.0, -3.0, -4.0, -4.0, -5.0, -6.0, -10.0)
        sim_neg_pool = SB(data1, data2)
        true_sim_neg_pool = float(self.data_dict_multi["sim_plus_neg"]["var_pool"])
        # two_sets_pooled = SB(data1, data2)
        self.assertAlmostEqual(sim_neg_pool.var_pool, true_sim_neg_pool, places=self.sig_deci_places)

        del data1, data2

    def test_8_test_score_calculation(self):
        data1 = (1, 2, 3, 4, 4, 5, 6, 10)
        data2 = (-1.0, -2.0, -3.0, -4.0, -4.0, -5.0, -6.0, -10.0)
        data3 = (1, 2, 3, 4, 4, 5, 6, 10, 0, 0, 0, 0, 0)
        hyp_test_sim = SB(data1)
        hyp_test_neg_h05 = SB(data2)
        hyp_test_two_small_ind = SB(data1, data2)
        hyp_test_two_small_dep = SB(data1, data2, samples_dependent=True)
        hyp_test_zeroes_pop = SB(data3, is_population=True)

        self.assertAlmostEqual(hyp_test_sim.calculate_test_score(),
                               float(self.data_dict["data_simple"]["score_hyp"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(hyp_test_neg_h05.calculate_test_score(h0=5),
                               float(self.data_dict["data_negatives"]["score_hyp"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(hyp_test_two_small_ind.calculate_test_score(),
                               float(self.data_dict_multi["sim_plus_neg"]["two_hyp"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(hyp_test_two_small_dep.calculate_test_score(),
                               float(self.data_dict["data_simple"]["score_hyp"]),
                               places=self.sig_deci_places)
        self.assertAlmostEqual(hyp_test_zeroes_pop.calculate_test_score(),
                               float(self.data_dict["data_zeroes_pop"]["score_hyp"]),
                               places=self.sig_deci_places)

    def test_9_negative_left_tail_cl_95(self):
        data = (-1.0, -2.0, -3.0, -4.0, -4.0, -5.0, -6.0, -10.0)
        neg_float_cl90 = SB(data, tail="left")
        self.assertAlmostEqual(neg_float_cl90.moe,
                               float(self.data_dict["data_neg_left_tail"]["moe"]),
                               places=self.sig_deci_places)
        true_neg_float_cl90_lower = float(self.data_dict["data_neg_left_tail"]["ci_lower"])
        true_neg_float_cl90_upper = float(self.data_dict["data_neg_left_tail"]["ci_upper"])
        self.assertAlmostEqual(neg_float_cl90.ci[0], true_neg_float_cl90_lower, places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.ci[1], true_neg_float_cl90_upper, places=self.sig_deci_places)
        self.assertAlmostEqual(neg_float_cl90.score_critical, float(self.data_dict["data_neg_left_tail"]["score_critical"]),
                               places=self.sig_deci_places)
        del data

    def test_10_remove_outliers(self):
        data = (1, 2, 3, 4, 4, 5, 6, 11)
        simple = SB(data, remove_outliers=True)
        self.assertEqual(simple.data, (1, 2, 3, 4, 4, 5, 6))


if __name__ == "__main__":
    unittest.main()
