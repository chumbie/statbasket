"""test_statMethods.py

Unit tests for statMethods.py

for list of TestCase assert methods visit:
https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug"""

# Standard Library Imports
import csv
import unittest

# Local Imports
from src.statMethods import StatMe as sm


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
                            # column_names_list[j-1] = sample name
                            # stat_type = type of data for sample
                            # for the above data name, add value to sample data_dict
                            data_dict[column_names_list[j - 1]][stat_type] = value
        return data_dict

    @classmethod
    def setUpClass(cls):
        # function to create large datasets

        cls.data_simple = (1, 2, 3, 4, 4, 5, 6, 10)
        cls.data_neg_float = (-1.0, -2.0, -3.0, -4.0, -4.0, -5.0, -6.0, -10.0)
        cls.data_zeroes_pop = (1, 2, 3, 4, 4, 5, 6, 10, 0, 0, 0, 0, 0)
        cls.data_large = cls.create_large_dataset(101)
        cls.data_large2 = cls.create_large_dataset(102)

        # number of places after decimal to compare results
        cls.sig_deci_places = 10

        # Get the confirmed correct stats, computed with libreOffice Calc

        filename = 'tests/test_stats_for_import.csv'
        # to retrieve data, use self.data_dict[sample_name][stat_type]
        # self.data_dict['data_simple']['n'] = 8
        cls.data_dict = cls.get_data_dict(filename)

    def test_1_data_validations(self):
        """Test to make sure methods reject empty tuple"""
        # Gets all methods in class, minus dunders
        method_list_value_error = \
            [method for method in dir(sm) if method.startswith("__") is False]
        del method_list_value_error[4]  # removing dict, TypeErrors
        del method_list_value_error[19]
        del method_list_value_error[-1]
        del method_list_value_error[-1]
        method_list_type_error = ['get_data_diff', 'get_var_pool']
        # argument to pass to each, an empty tuple
        data = ()

        # makes sure ValueError checks are working, all methods
        with self.assertRaises(ValueError):
            sm.get_data_diff((1, 2, 3), (4, 5, 6, 7))
            for i in range(len(method_list_value_error)):
                statement = f"sm.{method_list_value_error[i]}(data)"
                exec(statement)

        # makes sure TypeError checks are working, all methods
        with self.assertRaises(TypeError):
            for i in range(len(method_list_type_error)):
                statement = f"sm.{method_list_type_error[i]}(data)"
                exec(statement)
        del method_list_value_error, method_list_type_error, data

    def test_2_get_n(self):
        true_simple_n = float(self.data_dict["data_simple"]["n"])
        self.assertEqual(sm.get_n(self.data_simple), true_simple_n)

        true_negative_n = float(self.data_dict["data_negatives"]["n"])
        self.assertEqual(sm.get_n(self.data_neg_float), true_negative_n)

        true_zeroes_pop_n = float(self.data_dict["data_zeroes_pop"]["n"])
        self.assertEqual(sm.get_n(self.data_zeroes_pop), true_zeroes_pop_n)

        true_large1_n = float(self.data_dict["large_data_1"]["n"])
        self.assertEqual(sm.get_n(self.data_large), true_large1_n)

    def test_3_get_df(self):
        true_simple_df = float(self.data_dict["data_simple"]["df"])
        self.assertEqual(sm.get_df(self.data_simple), true_simple_df)

        true_negative_df = float(self.data_dict["data_negatives"]["df"])
        self.assertEqual(sm.get_df(self.data_neg_float), true_negative_df)

        true_zeroes_pop_df = float(self.data_dict["data_zeroes_pop"]["df"])
        self.assertEqual(sm.get_df(self.data_zeroes_pop), true_zeroes_pop_df)

        true_large1_df = float(self.data_dict["large_data_1"]["df"])
        self.assertEqual(sm.get_df(self.data_large), true_large1_df)

    def test_4_get_min(self):
        true_simple_min = float(self.data_dict["data_simple"]["min"])
        self.assertEqual(sm.get_min(self.data_simple), true_simple_min)

        true_negative_min = float(self.data_dict["data_negatives"]["min"])
        self.assertEqual(sm.get_min(self.data_neg_float), true_negative_min)

        true_zeroes_pop_min = float(self.data_dict["data_zeroes_pop"]["min"])
        self.assertEqual(sm.get_min(self.data_zeroes_pop), true_zeroes_pop_min)

        true_large1_min = float(self.data_dict["large_data_1"]["min"])
        self.assertEqual(sm.get_min(self.data_large), true_large1_min)

    def test_5_get_max(self):
        true_simple_max = float(self.data_dict["data_simple"]["max"])
        self.assertEqual(sm.get_max(self.data_simple), true_simple_max)

        true_negative_max = float(self.data_dict["data_negatives"]["max"])
        self.assertEqual(sm.get_max(self.data_neg_float), true_negative_max)

        true_zeroes_pop_max = float(self.data_dict["data_zeroes_pop"]["max"])
        self.assertEqual(sm.get_max(self.data_zeroes_pop), true_zeroes_pop_max)

        true_large1_max = float(self.data_dict["large_data_1"]["max"])
        self.assertEqual(sm.get_max(self.data_large), true_large1_max)

    def test_6_get_range(self):
        true_simple_range = float(self.data_dict["data_simple"]["range"])
        self.assertEqual(sm.get_range(self.data_simple), true_simple_range)

        true_negative_range = float(self.data_dict["data_negatives"]["range"])
        self.assertEqual(sm.get_range(self.data_neg_float), true_negative_range)

        true_zeroes_pop_range = float(self.data_dict["data_zeroes_pop"]["range"])
        self.assertEqual(sm.get_range(self.data_zeroes_pop), true_zeroes_pop_range)

        true_large1_range = float(self.data_dict["large_data_1"]["range"])
        self.assertEqual(sm.get_range(self.data_large), true_large1_range)

    def test_7_get_mean(self):
        true_simple_mean = float(self.data_dict["data_simple"]["mean"])
        self.assertAlmostEqual(sm.get_mean(self.data_simple), true_simple_mean,
                               places=self.sig_deci_places)

        true_negative_mean = float(self.data_dict["data_negatives"]["mean"])
        self.assertAlmostEqual(sm.get_mean(self.data_neg_float), true_negative_mean,
                               places=self.sig_deci_places)

        true_zeroes_pop_mean = float(self.data_dict["data_zeroes_pop"]["mean"])
        self.assertAlmostEqual(sm.get_mean(self.data_zeroes_pop), true_zeroes_pop_mean,
                               places=self.sig_deci_places)

        true_large1_mean = float(self.data_dict["large_data_1"]["mean"])
        self.assertAlmostEqual(sm.get_mean(self.data_large), true_large1_mean,
                               places=self.sig_deci_places)

    def test_8_get_median(self):
        true_simple_median = float(self.data_dict["data_simple"]["median"])
        self.assertAlmostEqual(sm.get_median(self.data_simple), true_simple_median,
                               places=self.sig_deci_places)

        true_negative_median = float(self.data_dict["data_negatives"]["median"])
        self.assertAlmostEqual(sm.get_median(self.data_neg_float), true_negative_median,
                               places=self.sig_deci_places)

        true_zeroes_pop_median = float(self.data_dict["data_zeroes_pop"]["median"])
        self.assertAlmostEqual(sm.get_median(self.data_zeroes_pop), true_zeroes_pop_median,
                               places=self.sig_deci_places)

        true_large1_median = float(self.data_dict["large_data_1"]["median"])
        self.assertAlmostEqual(sm.get_median(self.data_large), true_large1_median,
                               places=self.sig_deci_places)

    def test_9_get_mode(self):
        true_simple_mode = float(self.data_dict["data_simple"]["mode"])
        self.assertAlmostEqual(sm.get_mode(self.data_simple), true_simple_mode,
                               places=self.sig_deci_places)

        true_negative_mode = float(self.data_dict["data_negatives"]["mode"])
        self.assertAlmostEqual(sm.get_mode(self.data_neg_float), true_negative_mode,
                               places=self.sig_deci_places)

        true_zeroes_pop_mode = float(self.data_dict["data_zeroes_pop"]["mode"])
        self.assertAlmostEqual(sm.get_mode(self.data_zeroes_pop), true_zeroes_pop_mode,
                               places=self.sig_deci_places)

        true_large1_mode = float(self.data_dict["large_data_1"]["mode"])
        self.assertAlmostEqual(sm.get_mode(self.data_large), true_large1_mode,
                               places=self.sig_deci_places)

    def test_10_get_skew(self):
        true_simple_skew = float(self.data_dict["data_simple"]["skew"])
        self.assertAlmostEqual(sm.get_skew(self.data_simple), true_simple_skew,
                               places=self.sig_deci_places)

        true_negative_skew = float(self.data_dict["data_negatives"]["skew"])
        self.assertAlmostEqual(sm.get_skew(self.data_neg_float), true_negative_skew,
                               places=self.sig_deci_places)

        true_zeroes_pop_skew = float(self.data_dict["data_zeroes_pop"]["skew"])
        self.assertAlmostEqual(sm.get_skew(self.data_zeroes_pop, True), true_zeroes_pop_skew,
                               places=self.sig_deci_places)

        true_large1_skew = float(self.data_dict["large_data_1"]["skew"])
        self.assertAlmostEqual(sm.get_skew(self.data_large), true_large1_skew,
                               places=self.sig_deci_places)

    def test_11_get_var(self):
        true_simple_var = float(self.data_dict["data_simple"]["var"])
        self.assertAlmostEqual(sm.get_var(self.data_simple), true_simple_var,
                               places=self.sig_deci_places)

        true_negative_var = float(self.data_dict["data_negatives"]["var"])
        self.assertAlmostEqual(sm.get_var(self.data_neg_float), true_negative_var,
                               places=self.sig_deci_places)

        true_zeroes_pop_var = float(self.data_dict["data_zeroes_pop"]["var"])
        self.assertAlmostEqual(sm.get_var(self.data_zeroes_pop, True), true_zeroes_pop_var,
                               places=self.sig_deci_places)

        true_large1_var = float(self.data_dict["large_data_1"]["var"])
        self.assertAlmostEqual(sm.get_var(self.data_large), true_large1_var,
                               places=self.sig_deci_places)

    def test_12_get_stdev(self):
        true_simple_stdev = float(self.data_dict["data_simple"]["stdev"])
        self.assertAlmostEqual(sm.get_stdev(self.data_simple), true_simple_stdev,
                               places=self.sig_deci_places)

        true_negative_stdev = float(self.data_dict["data_negatives"]["stdev"])
        self.assertAlmostEqual(sm.get_stdev(self.data_neg_float), true_negative_stdev,
                               places=self.sig_deci_places)

        true_zeroes_pop_stdev = float(self.data_dict["data_zeroes_pop"]["stdev"])
        self.assertAlmostEqual(sm.get_stdev(self.data_zeroes_pop, True), true_zeroes_pop_stdev,
                               places=self.sig_deci_places)

        true_large1_stdev = float(self.data_dict["large_data_1"]["stdev"])
        self.assertAlmostEqual(sm.get_stdev(self.data_large), true_large1_stdev,
                               places=self.sig_deci_places)

    def test_13_get_sterr(self):
        true_simple_sterr = float(self.data_dict["data_simple"]["sterr"])
        self.assertAlmostEqual(sm.get_sterr(self.data_simple), true_simple_sterr,
                               places=self.sig_deci_places)

        true_negative_sterr = float(self.data_dict["data_negatives"]["sterr"])
        self.assertAlmostEqual(sm.get_sterr(self.data_neg_float), true_negative_sterr,
                               places=self.sig_deci_places)

        true_zeroes_pop_sterr = float(self.data_dict["data_zeroes_pop"]["sterr"])
        self.assertAlmostEqual(sm.get_sterr(self.data_zeroes_pop, True), true_zeroes_pop_sterr,
                               places=self.sig_deci_places)

        true_large1_sterr = float(self.data_dict["large_data_1"]["sterr"])
        self.assertAlmostEqual(sm.get_sterr(self.data_large), true_large1_sterr,
                               places=self.sig_deci_places)

    def test_14_get_cv(self):
        true_simple_cv = float(self.data_dict["data_simple"]["cv"])
        self.assertAlmostEqual(sm.get_cv(self.data_simple), true_simple_cv,
                               places=self.sig_deci_places)

        true_negative_cv = float(self.data_dict["data_negatives"]["cv"])
        self.assertAlmostEqual(sm.get_cv(self.data_neg_float), true_negative_cv,
                               places=self.sig_deci_places)

        true_zeroes_pop_cv = float(self.data_dict["data_zeroes_pop"]["cv"])
        self.assertAlmostEqual(sm.get_cv(self.data_zeroes_pop, True), true_zeroes_pop_cv,
                               places=self.sig_deci_places)

        true_large1_cv = float(self.data_dict["large_data_1"]["cv"])
        self.assertAlmostEqual(sm.get_cv(self.data_large), true_large1_cv,
                               places=self.sig_deci_places)

    def test_15_get_data_diff(self):
        self.assertEqual(sm.get_data_diff(self.data_simple, self.data_neg_float), (2, 4, 6, 8, 8, 10, 12, 20))

        statMethods_difference_list = sm.get_data_diff(self.data_large, self.data_large2)
        import csv
        csv_file = "tests/get_data_diff_large.csv"
        with open(csv_file) as file:
            csv_reader = csv.reader(file)
            diff_data_list = list(csv_reader)
            for i in range(len(statMethods_difference_list)):
                self.assertEqual(float(statMethods_difference_list[i]), float(diff_data_list[i][0]))

    def test_16_get_var_pool(self):
        data_dict_multi = self.get_data_dict('tests/test_stats_for_import_multi.csv')
        sm_sim_neg_var_pool = sm.get_var_pool(self.data_simple, self.data_neg_float)
        true_sim_neg_var_pool = float(data_dict_multi["sim_plus_neg"]["var_pool"])
        self.assertAlmostEqual(sm_sim_neg_var_pool, true_sim_neg_var_pool,
                               places=self.sig_deci_places)
        sm_larges_var_pool = sm.get_var_pool(self.data_large, self.data_large2)
        true_larges_pool = float(data_dict_multi["large1_plus_large2"]["var_pool"])
        self.assertAlmostEqual(sm_larges_var_pool, true_larges_pool,
                               places=self.sig_deci_places)

    def test_17__get_lookup_df(self):
        sm_sim_df_lookup = sm._get_lookup_df(self.data_simple)
        true_simple_df_lookup = float(self.data_dict["data_simple"]["df_lookup"])
        self.assertAlmostEqual(sm_sim_df_lookup, true_simple_df_lookup,
                               places=self.sig_deci_places)

        sm_neg_df_lookup = sm._get_lookup_df(self.data_neg_float)
        true_negative_df_lookup = float(self.data_dict["data_negatives"]["df_lookup"])
        self.assertAlmostEqual(sm_neg_df_lookup, true_negative_df_lookup,
                               places=self.sig_deci_places)

        sm_zero_pop_df_lookup = sm._get_lookup_df(self.data_zeroes_pop, True)
        true_zeroes_pop_df_lookup = float(self.data_dict["data_zeroes_pop"]["df_lookup"])
        self.assertAlmostEqual(sm_zero_pop_df_lookup, true_zeroes_pop_df_lookup,
                               places=self.sig_deci_places)

        sm_large1_df_lookup = sm._get_lookup_df(self.data_large)
        true_large1_df_lookup = float(self.data_dict["large_data_1"]["df_lookup"])
        self.assertAlmostEqual(sm_large1_df_lookup, true_large1_df_lookup,
                               places=self.sig_deci_places)

    def test_18_get_score_critical(self):
        simple_cl = float(self.data_dict["data_simple"]["cl"])
        sm_crit_sim = sm.get_score_critical(self.data_simple, cl=simple_cl)
        true_crit_sim = float(self.data_dict["data_simple"]["score_critical"])
        self.assertAlmostEqual(sm_crit_sim, true_crit_sim,
                               places=self.sig_deci_places)

        neg_cl = float(self.data_dict["data_negatives"]["cl"])
        sm_crit_neg = sm.get_score_critical(self.data_neg_float, cl=neg_cl)
        true_crit_neg = float(self.data_dict["data_negatives"]["score_critical"])
        self.assertAlmostEqual(sm_crit_neg, true_crit_neg,
                               places=self.sig_deci_places)

        zeroes_cl = float(self.data_dict["data_zeroes_pop"]["cl"])
        sm_crit_zero_pop = sm.get_score_critical(
            self.data_zeroes_pop, is_population=True, cl=zeroes_cl
        )
        true_crit_zero_pop = float(self.data_dict["data_zeroes_pop"]["score_critical"])
        self.assertAlmostEqual(sm_crit_zero_pop, true_crit_zero_pop,
                               places=self.sig_deci_places)

        large1_cl = float(self.data_dict["large_data_1"]["cl"])
        sm_crit_large1 = sm.get_score_critical(self.data_large, cl=large1_cl)
        true_crit_large1 = float(self.data_dict["large_data_1"]["score_critical"])
        self.assertAlmostEqual(sm_crit_large1, true_crit_large1,
                               places=self.sig_deci_places)

    def test_19_get_moe(self):
        simple_cl = float(self.data_dict["data_simple"]["cl"])
        sm_sim_moe = sm.get_moe(self.data_simple, cl=simple_cl)
        true_sim_moe = float(self.data_dict["data_simple"]["moe"])
        self.assertAlmostEqual(sm_sim_moe, true_sim_moe,
                               places=self.sig_deci_places)

        neg_cl = float(self.data_dict["data_negatives"]["cl"])
        sm_neg_moe = sm.get_moe(self.data_neg_float, cl=neg_cl)
        true_neg_moe = float(self.data_dict["data_negatives"]["moe"])
        self.assertAlmostEqual(sm_neg_moe, true_neg_moe,
                               places=self.sig_deci_places)

        zeroes_cl = float(self.data_dict["data_zeroes_pop"]["cl"])
        sm_zero_pop_moe = sm.get_moe(
            self.data_zeroes_pop, is_population=True, cl=zeroes_cl
        )
        true_zero_pop_moe = float(self.data_dict["data_zeroes_pop"]["moe"])
        self.assertAlmostEqual(sm_zero_pop_moe, true_zero_pop_moe,
                               places=self.sig_deci_places)

        large1_cl = float(self.data_dict["large_data_1"]["cl"])
        sm_large1_moe = sm.get_moe(self.data_large, cl=large1_cl)
        true_large1_moe = float(self.data_dict["large_data_1"]["moe"])
        self.assertAlmostEqual(sm_large1_moe, true_large1_moe,
                               places=self.sig_deci_places)

    def test_20_get_ci(self):
        simple_cl = float(self.data_dict["data_simple"]["cl"])
        sm_sim_lower, sm_sim_upper = sm.get_ci(self.data_simple, cl=simple_cl)
        true_sim_lower = float(self.data_dict["data_simple"]["ci_lower"])
        true_sim_upper = float(self.data_dict["data_simple"]["ci_upper"])
        self.assertAlmostEqual(sm_sim_lower, true_sim_lower,
                               places=self.sig_deci_places)
        self.assertAlmostEqual(sm_sim_upper, true_sim_upper,
                               places=self.sig_deci_places)

        neg_cl = float(self.data_dict["data_negatives"]["cl"])
        sm_neg_lower, sm_neg_upper = sm.get_ci(self.data_neg_float, cl=neg_cl)
        true_neg_lower = float(self.data_dict["data_negatives"]["ci_lower"])
        true_neg_upper = float(self.data_dict["data_negatives"]["ci_upper"])
        self.assertAlmostEqual(sm_neg_lower, true_neg_lower,
                               places=self.sig_deci_places)
        self.assertAlmostEqual(sm_neg_upper, true_neg_upper,
                               places=self.sig_deci_places)

        zeroes_cl = float(self.data_dict["data_zeroes"]["cl"])
        sm_zero_pop_lower, sm_zero_pop_upper = sm.get_ci(
            self.data_zeroes_pop, is_population=True, cl=zeroes_cl
        )
        true_zero_pop_lower = float(self.data_dict["data_zeroes_pop"]["ci_lower"])
        true_zero_pop_upper = float(self.data_dict["data_zeroes_pop"]["ci_upper"])
        self.assertAlmostEqual(sm_zero_pop_lower, true_zero_pop_lower,
                               places=self.sig_deci_places)
        self.assertAlmostEqual(sm_zero_pop_upper, true_zero_pop_upper,
                               places=self.sig_deci_places)

        large1_cl = float(self.data_dict["large_data_1"]["cl"])
        sm_large1_lower, sm_large1_upper = sm.get_ci(self.data_large, cl=large1_cl)
        true_large1_lower = float(self.data_dict["large_data_1"]["ci_lower"])
        true_large1_upper = float(self.data_dict["large_data_1"]["ci_upper"])
        self.assertAlmostEqual(sm_large1_lower, true_large1_lower,
                               places=self.sig_deci_places)
        self.assertAlmostEqual(sm_large1_upper, true_large1_upper,
                               places=self.sig_deci_places)

    def test_21_get_score_hyp(self):

        # test, dependent samples should be of equal length
        with self.assertRaises(ValueError):
            sm.get_score_hyp((1, 2, 3), (4, 5, 6, 7), 0, samples_dependent=True)

        sm_sim_h0 = float(self.data_dict["data_simple"]["h0"])
        sm_sim_hyp = sm.get_score_hyp(self.data_simple, h0=sm_sim_h0)
        true_sim_hyp = float(self.data_dict["data_simple"]["score_hyp"])
        self.assertAlmostEqual(sm_sim_hyp, true_sim_hyp,
                               places=self.sig_deci_places)

        sm_neg_h0 = float(self.data_dict["data_negatives"]["h0"])
        sm_neg_hyp = sm.get_score_hyp(self.data_neg_float, h0=sm_neg_h0)
        true_neg_hyp = float(self.data_dict["data_negatives"]["score_hyp"])
        self.assertAlmostEqual(sm_neg_hyp, true_neg_hyp,
                               places=self.sig_deci_places)

        # dependent
        sm_neg_h0 = float(self.data_dict["small_data_diff"]["h0"])
        sm_neg_hyp = sm.get_score_hyp(self.data_simple, self.data_neg_float, h0=sm_neg_h0, samples_dependent=True)
        true_neg_hyp = float(self.data_dict["small_data_diff"]["score_hyp"])
        self.assertAlmostEqual(sm_neg_hyp, true_neg_hyp,
                               places=self.sig_deci_places)

        sm_zero_pop_h0 = float(self.data_dict["data_zeroes_pop"]["h0"])
        sm_zero_pop_hyp = sm.get_score_hyp(self.data_zeroes_pop, is_population=True, h0=sm_zero_pop_h0)
        true_zero_pop_hyp = float(self.data_dict["data_zeroes_pop"]["score_hyp"])
        self.assertAlmostEqual(sm_zero_pop_hyp, true_zero_pop_hyp,
                               places=self.sig_deci_places)

        sm_large1_h0 = float(self.data_dict["large_data_1"]["h0"])
        sm_large1_hyp = sm.get_score_hyp(self.data_large, h0=sm_large1_h0)
        true_large1_hyp = float(self.data_dict["large_data_1"]["score_hyp"])
        self.assertAlmostEqual(sm_large1_hyp, true_large1_hyp,
                               places=self.sig_deci_places)


if __name__ == "__main__":
    unittest.main()
