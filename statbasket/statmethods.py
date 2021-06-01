"""statMethods.py

Contains the class StatMe, which is a collection of methods used for
simple statistics calculations."""

# Standard System Imports
from math import fsum


class StatMe:
    """
    A class of class methods used to perform simple statistics calculations.

    Example Usage:
        >>> from statbasket.statbasket import StatMe as sm
        >>> data = (1, 2, 3, 4, 4, 5)
        >>> sm.get_mean(data)
        3.1666666666666665
        >>> sm.get_median(data)
        3.5
        >>> sm.get_mode(data)
        4
    Methods::
        get_n:
            Return the sample size of the data

        get_df:
            Return the degrees of freedom of the data

        get_min:
            Return the minimum data value in the sample

        get_max:
            Return the maximum data value in the sample

        get_range:
            Return the range of the sample

        get_mean:
            Return the mean of the sample

        get_median:
            Return the median of the sample

        get_quartile_data:
            Return tuple of sample's quartiles data (Q1, Q2, Q3, IQR)

        get_outlier_data:
            Return the outliers in the dataset

        get_mode:
            Return the mode of the dataset

        get_var:
            Return the variance of the sample

        get_stdev:
            Return the standard deviation of the dataset
<<<<<<< HEAD:statbasket/statmethods.py

        get_sterr:
            Return the standard error of the dataset

=======

        get_sterr:
            Return the standard error of the dataset

>>>>>>> 9b139656718d8deddbe47c473991cd01b6ca7ef4:statbasket/statMethods.py
        get_cv:
            Return the coefficient of variation of the dataset

        get_data_diff:
            Return the difference of each value between two dependent datasets.

        get_var_pool:
            Return the pooled variance between two independent datasets.

        get_score_critical:
            Return the critical z- or t-score for the dataset.

        get_moe:
            Return the margin of error for the dataset, used to calculate a confidence interval.

        get_ci:
            Return the confidence interval for the dataset.

        get_score_hyp:
            Return the hypothesis test score for the dataset(s)

    """

    @staticmethod
    def _data_validation(data):
        """Throws ValueError if data is not list, tuple, or None"""
        if isinstance(data, (list, tuple, type(None))) is not True:
            raise ValueError(f"data must be tuple, list, or None, "
                             f"data type is '{type(data).__name__}'. "
                             f"Iterable data cannot be empty.")

    # Basic Data Attributes ###########################################

    @classmethod
    def get_n(cls, data: tuple or list) -> int:
        """Return the sample size of the dataset."""
        cls._data_validation(data)
        if isinstance(data, (type(None))):
            # Some method calculations require 0 if data is None
            return 0
        return len(data)

    @classmethod
    def get_df(cls, data: tuple or list) -> int:
        """Return the degrees of freedom for the dataset.

        .. math::
            df = n - 1
            """
        cls._data_validation(data)
        n = cls.get_n(data)
        df = n - 1
        return df

    @classmethod
    def get_min(cls, data: tuple or list) -> float:
        """Return the smallest value in the dataset."""
        cls._data_validation(data)
        return min(data)

    @classmethod
    def get_max(cls, data: tuple or list) -> float:
        """Return the largest value in the dataset."""
        cls._data_validation(data)
        return max(data)

    # Measures of Central Tendency ####################################

    @classmethod
    def get_range(cls, data: tuple or list) -> float:
        """Return the range of the data

        .. math::
            Range = x_max - x_min"""
        cls._data_validation(data)
        max_ = cls.get_max(data)
        min_ = cls.get_min(data)
        return float(max_ - min_)

    @classmethod
    def get_mean(cls, data: tuple or list) -> float:
        """Return the average value in the dataset.

        .. math::
            mean = \\frac{\sum_{i=1}^{n}x}{n}
        """
        cls._data_validation(data)
        sum_ = fsum(data)
        n = cls.get_n(data)
        try:
            return float(sum_ / n)
        except ZeroDivisionError as exc:
            # for hyp score calculation, n = 0 for empty set is useful
            return 0

    @classmethod
    def get_median(cls, data: tuple or list) -> float:
        """Return the median of the dataset.

        The median is middlemost value of the dataset, or the average
        between the two middlemost values where n % 2 = 0 (even)"""
        cls._data_validation(data)
        from math import floor
        # Sort the data
        sorted_data = sorted(list(data))
        n = len(sorted_data)
        # get the middle index
        odd_middle_index = floor(n / 2)
        upper_even_index = floor(n / 2)
        lower_even_index = floor(n / 2) - 1
        # print(f"\nodd_middle = {odd_middle_index}")
        # print(f"upper_even_middle = {upper_even_index}")
        # print(f"lower_even_middle = {lower_even_index}")
        if n % 2 == 1:
            return float(sorted_data[odd_middle_index])
        # If n is even, gets the average of the middle two values
        else:
            median_lower = sorted_data[lower_even_index]
            median_upper = sorted_data[upper_even_index]
            return_median = (median_lower + median_upper) / 2
            return float(return_median)
        
    @classmethod
    def get_quartile_data(cls, data: tuple or list) -> tuple:
        """
        Return a tuple of data's quartile information (Q1, Q2, Q3, IQR)

        If you arrange all valued in the dataset from smallest to largest,
        Q2 is the middlemost value (the median). If you divide the dataset
        in half from this median and find the middlemost value in these
        halves, Q1 is the middlemost value of the first half and Q3 is
        the middlemost value of the second half, neither half of which
        includes Q2.
        The inter-quartile range (IQR) is the number of units between
        Q1 and Q3, i.e. Q3 - Q1."""
        cls._data_validation(data)
        # Sort the data
        sorted_data = sorted(list(data))
        # Get q2, which is the median
        q2 = cls.get_median(data)
        first_half_data = list()
        second_half_data = list()
        # add to first half until median, then add to second half
        for i in range(len(sorted_data)):
            # if less than q2, first half
            if sorted_data[i] < q2:
                first_half_data.append(sorted_data[i])
            # if greather than q2, second half, skips q2
            elif sorted_data[i] > q2:
                second_half_data.append(sorted_data[i])
        # use median method on halves to get quartiles
        q1 = cls.get_median(first_half_data)
        q3 = cls.get_median(second_half_data)
        iqr = q3-q1
        return q1, q2, q3, iqr

    @classmethod
    def get_outlier_data(cls, data: tuple or list, remove_outliers=False) -> tuple:
        """
        Return a tuple of all outliers in dataset.

        Outliers are defined as data points which are not within 1.5 IQRs
        of Q1 or Q3.

        If remove_outliers=True, instead returns the data with outliers removed.

        Lower Outlier Limit = Q1 - (1.5*IQR)

        Upper Outlier Limit = Q3 +(1.5*IQR)"""
        cls._data_validation(data)
        q1, q2, q3, iqr = cls.get_quartile_data(data)
        data_without_outliers = list()
        outliers_list = list()
        lower_out_bound, upper_out_bound = q1 - 1.5*iqr, q3 + 1.5*iqr
        print(lower_out_bound, upper_out_bound)
        for i in range(len(data)):
            if lower_out_bound <= data[i] <= upper_out_bound:
                data_without_outliers.append(data[i])
            else:
                outliers_list.append(data[i])
        if remove_outliers:
            return tuple(data_without_outliers)
        else:
            return tuple(outliers_list)

    @classmethod
    def get_quartile_data(cls, data: tuple or list) -> tuple:
        """
        Return a tuple of data's quartile information (Q1, Q2, Q3, IQR)

        If you arrange all valued in the dataset from smallest to largest,
        Q2 is the middlemost value (the median). If you divide the dataset
        in half from this median and find the middlemost value in these
        halves, Q1 is the middlemost value of the first half and Q3 is
        the middlemost value of the second half, neither half of which
        includes Q2.
        The inter-quartile range (IQR) is the number of units between
        Q1 and Q3, i.e. Q3 - Q1."""
        cls._data_validation(data)
        from math import floor
        # Sort the data
        n = cls.get_n(data)
        if n == 0:
            # Empty dataset, returns zeroes
            return 0, 0, 0, 0
        sorted_data = sorted(list(data))
        n_is_odd = True if n % 2 == 1 else False

        # Get middle index
        odd_middle_index = floor(n / 2)
        even_upper_index = floor(n / 2)
        even_lower_index = floor(n / 2) - 1

        # Get q2, which is the median
        q2 = cls.get_median(data)
        first_half_data = list()
        second_half_data = list()

        # add to first half until median, then add to second half
        if n_is_odd:
            for i in range(n):
                if i < odd_middle_index:
                    first_half_data.append(sorted_data[i])
                # note how if index = middle_index, skips
                elif i > odd_middle_index:
                    second_half_data.append(sorted_data[i])
        else:
            for i in range(n):
                if i <= even_lower_index:
                    first_half_data.append(sorted_data[i])
                # note how if index = middle_index, skips
                else:
                    second_half_data.append(sorted_data[i])
        # use median method on halves to get quartiles
        q1 = cls.get_median(first_half_data)
        q3 = cls.get_median(second_half_data)
        iqr = q3 - q1
        return q1, q2, q3, iqr

    @classmethod
    def get_outlier_data(
            cls, data: tuple or list, remove_outliers=False
    ) -> tuple:
        """
        Return a tuple of all outliers in dataset.

        Outliers are defined as data points which are not within 1.5 IQRs
        of Q1 or Q3.

        If remove_outliers=True, instead returns the data with outliers removed.

        Lower Outlier Limit = Q1 - (1.5*IQR)

        Upper Outlier Limit = Q3 +(1.5*IQR)"""
        cls._data_validation(data)
        q1, _, q3, iqr = cls.get_quartile_data(data)
        if (q1, _, q3, iqr) == (0, 0, 0, 0):
            # getting outliers from empty set, return empty
            return tuple()
        data_without_outliers = list()
        outliers_list = list()
        lower_out_bound, upper_out_bound = q1 - 1.5*iqr, q3 + 1.5*iqr
        for i in range(len(data)):
            if lower_out_bound <= data[i] <= upper_out_bound:
                data_without_outliers.append(data[i])
            else:
                outliers_list.append(data[i])
        if remove_outliers:
            return tuple(data_without_outliers)
        else:
            return tuple(outliers_list)

    @classmethod
    def get_mode(cls, data: tuple or list, multimodal=False) -> float or tuple or str:
        """Return mode as float, 'none', or 'multimodal'.

        The mode of the dataset is the value which appears most
        frequently.

        >>> StatMe.get_mode((1, 2, 2)
        2.0

        Return 'none' if no modes in data.

        >>> StatMe.get_mode((2, 4, 6, 8))
        'none'

        If multiple modes, returns 'multimodal', or a tuple of modes
        if multimodal=True.

        >>> StatMe.get_mode((1, 1, 2, 2, 3))
        'multimodal'
        >>> StatMe.get_mode((1, 1, 2, 2, 3), multimodal=True)
        (1.0, 2.0)
        """
        cls._data_validation(data)
        current_highest_count = int()
        set_of_highest_items = set()
        mode_list = list()
        count_dict = dict()
        for each_item in data:
            count_dict.setdefault(each_item, 0)
            count_dict[each_item] += 1
            if count_dict[each_item] >= current_highest_count:
                set_of_highest_items.add(each_item)
                current_highest_count = count_dict[each_item]
        for each_item in set_of_highest_items:
            if count_dict[each_item] == current_highest_count:
                mode_list.append(each_item)
        # mode_list now contains all items equal to the highest
        # repetitions among data points.
        if multimodal:
            return tuple(sorted(mode_list))
        else:
            if len(mode_list) == 0:
                return 'none'
            elif len(mode_list) == 1:
                return float(mode_list[0])
            else:
                return 'multimodal'

    @classmethod

    def get_skew(cls, data: tuple or list, is_population=False) -> float:
        """Return the skewness of the data, using the skewness formula:

        .. math::
            skewness = \\frac{(1/n)\sum_{i=1}^{n}(x_{i} - mean)^{3}}{stdev^3}
            """
        cls._data_validation(data)
        mean = cls.get_mean(data)
        n = cls.get_n(data)
        stdev = cls.get_stdev(data, is_population=is_population)
        sum_of_cubed_difference = float()
        for each_item in data:
            sum_of_cubed_difference += (each_item - mean) ** 3
        skewness = (1/n) * sum_of_cubed_difference / stdev ** 3
        return float(skewness)

    # Measures of Data Variation ######################################

    @classmethod
    def get_var(cls, data: tuple or list, is_population=False) -> float:
        """Return the sample variance (s\u00b2) of each data set as a
        tuple.

        If is_population=True, returns the population variance
        (\u03c3\u00b2) instead.

        .. math::
            s^2 = \\frac{\sum_{i=1}^{n}(x_{i} - mean)^{2}}{n - 1}

            \u03c3^2 = \\frac{\sum_{i=1}^{n}(x_{i} - \u03bc)^{2}}{n}
        """
        cls._data_validation(data)
        mean = cls.get_mean(data)
        variance = float()
        n = cls.get_n(data)
        for each_item in data:
            variance += (each_item - mean) ** 2
        # Checks whether is a population or sample
        if is_population:
            variance = variance / n
        else:
            variance = variance / (n - 1)
        return float(variance)

    @classmethod
    def get_stdev(cls, data: tuple or list, is_population=False) -> float:
        """Calculates the standard deviation (s) of the data set

        .. math::
            s = \sqrt{s^2}
        """
        cls._data_validation(data)
        from math import sqrt
        return sqrt(cls.get_var(data, is_population))

    @classmethod
    def get_sterr(cls, data: tuple or list, is_population=False) -> float:
        """Calculates the standard error of the data set

        .. math::
            SE = s/\sqrt{n}
        """
        cls._data_validation(data)
        from math import sqrt
        return cls.get_stdev(data, is_population) / sqrt(cls.get_n(data))

    @classmethod
    def get_cv(cls, data: tuple or list, is_population=False) -> float:
        """Returns the coefficient of variation

        .. math::
            CV = s/mean"""
        cls._data_validation(data)
        return cls.get_stdev(data, is_population) / cls.get_mean(data)

    # Two-Population Properties #######################################

    @classmethod
    def get_data_diff(cls, data1: tuple, data2: tuple) -> tuple:
        """Return tuple of difference of two dependent data sets

        Note that this method assumes that the two data sets are
        **dependent** and of **equal sample sizes**, i.e. this method
        is meaningless when applied to two independent data sets.

        Example of dependence: weighing each participant before
        (data1) and after (data2) taking a weight-loss drug.

        .. math::
            x_{diff} = x_{1} - x_{2}
        """
        cls._data_validation(data1)
        cls._data_validation(data2)
        data1_n = StatMe.get_n(data1)
        data2_n = StatMe.get_n(data2)
        if data1_n != data2_n:
            raise ValueError(f"Samples are not of equal length.\n"
                             f"Items in 'data1' = {data1_n}\n"
                             f"Items in 'data2' = {data2_n}")
        else:
            return_list = list()
            for i in range(data1_n):
                x1 = data1[i]
                x2 = data2[i]
                return_list.append(x1 - x2)
            return tuple(return_list)

    @classmethod
    def get_var_pool(cls, data1: tuple, data2: tuple) -> float:
        """Return the pooled variance between the first and second data sets

        .. math::
            s_p^2 = \\frac{(n_x - 1)s^2_x + (n_y - 1)s^2_y)}{n_x + n_y - 2}
        """
        cls._data_validation(data1)
        cls._data_validation(data2)
        n1 = cls.get_n(data1)
        var1 = cls.get_var(data1)
        n2 = cls.get_n(data2)
        var2 = cls.get_var(data2)
        return ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)

    # Hypothesis Testing and Confidence Interval Statistics ###########

    t_table = {
        1: {0.1: 3.078, 0.05: 6.314, 0.025: 12.706, 0.01: 31.821, 0.005: 63.657},
        2: {0.1: 1.886, 0.05: 2.92, 0.025: 4.303, 0.01: 6.965, 0.005: 9.925},
        3: {0.1: 1.638, 0.05: 2.353, 0.025: 3.182, 0.01: 4.541, 0.005: 5.841},
        4: {0.1: 1.533, 0.05: 2.132, 0.025: 2.776, 0.01: 3.747, 0.005: 4.604},
        5: {0.1: 1.476, 0.05: 2.015, 0.025: 2.571, 0.01: 3.365, 0.005: 4.032},
        6: {0.1: 1.44, 0.05: 1.943, 0.025: 2.447, 0.01: 3.143, 0.005: 3.707},
        7: {0.1: 1.415, 0.05: 1.895, 0.025: 2.365, 0.01: 2.998, 0.005: 3.499},
        8: {0.1: 1.397, 0.05: 1.86, 0.025: 2.306, 0.01: 2.896, 0.005: 3.355},
        9: {0.1: 1.383, 0.05: 1.833, 0.025: 2.262, 0.01: 2.821, 0.005: 3.25},
        10: {0.1: 1.372, 0.05: 1.812, 0.025: 2.228, 0.01: 2.764, 0.005: 3.169},
        11: {0.1: 1.363, 0.05: 1.796, 0.025: 2.201, 0.01: 2.718, 0.005: 3.106},
        12: {0.1: 1.356, 0.05: 1.782, 0.025: 2.179, 0.01: 2.681, 0.005: 3.055},
        13: {0.1: 1.35, 0.05: 1.771, 0.025: 2.16, 0.01: 2.65, 0.005: 3.012},
        14: {0.1: 1.345, 0.05: 1.761, 0.025: 2.145, 0.01: 2.624, 0.005: 2.977},
        15: {0.1: 1.341, 0.05: 1.753, 0.025: 2.131, 0.01: 2.602, 0.005: 2.947},
        16: {0.1: 1.337, 0.05: 1.746, 0.025: 2.12, 0.01: 2.583, 0.005: 2.921},
        17: {0.1: 1.333, 0.05: 1.74, 0.025: 2.11, 0.01: 2.567, 0.005: 2.898},
        18: {0.1: 1.33, 0.05: 1.734, 0.025: 2.101, 0.01: 2.552, 0.005: 2.878},
        19: {0.1: 1.328, 0.05: 1.729, 0.025: 2.093, 0.01: 2.539, 0.005: 2.861},
        20: {0.1: 1.325, 0.05: 1.725, 0.025: 2.086, 0.01: 2.528, 0.005: 2.845},
        21: {0.1: 1.323, 0.05: 1.721, 0.025: 2.08, 0.01: 2.518, 0.005: 2.831},
        22: {0.1: 1.321, 0.05: 1.717, 0.025: 2.074, 0.01: 2.508, 0.005: 2.819},
        23: {0.1: 1.319, 0.05: 1.714, 0.025: 2.069, 0.01: 2.5, 0.005: 2.807},
        24: {0.1: 1.318, 0.05: 1.711, 0.025: 2.064, 0.01: 2.492, 0.005: 2.797},
        25: {0.1: 1.316, 0.05: 1.708, 0.025: 2.06, 0.01: 2.485, 0.005: 2.787},
        26: {0.1: 1.315, 0.05: 1.706, 0.025: 2.056, 0.01: 2.479, 0.005: 2.779},
        27: {0.1: 1.314, 0.05: 1.703, 0.025: 2.052, 0.01: 2.473, 0.005: 2.771},
        28: {0.1: 1.313, 0.05: 1.701, 0.025: 2.048, 0.01: 2.467, 0.005: 2.763},
        29: {0.1: 1.311, 0.05: 1.699, 0.025: 2.045, 0.01: 2.462, 0.005: 2.756},
        30: {0.1: 1.31, 0.05: 1.697, 0.025: 2.042, 0.01: 2.457, 0.005: 2.75},
        35: {0.1: 1.306, 0.05: 1.69, 0.025: 2.03, 0.01: 2.438, 0.005: 2.724},
        40: {0.1: 1.303, 0.05: 1.684, 0.025: 2.021, 0.01: 2.423, 0.005: 2.704},
        50: {0.1: 1.299, 0.05: 1.676, 0.025: 2.009, 0.01: 2.403, 0.005: 2.678},
        60: {0.1: 1.296, 0.05: 1.671, 0.025: 2, 0.01: 2.39, 0.005: 2.66},
        120: {0.1: 1.289, 0.05: 1.658, 0.025: 1.98, 0.01: 2.358, 0.005: 2.617},
        999: {0.1: 1.282, 0.05: 1.645, 0.025: 1.96, 0.01: 2.326, 0.005: 2.576}
    }

    @classmethod
    def _get_lookup_df(cls, df_data: tuple or list, df_is_population=False) -> int:
        """
        Convert actual df into t_table lookup df.

        For n > 150, returns 999 (z-score lookup value for t-table).
        """
        cls._data_validation(df_data)
        n = cls.get_n(df_data)
        df = n-1
        if df >= 150 or df_is_population:
            return 999
        elif df <= 30:
            return df
        else:
            # stores the previous key in the loop
            last_key = 0
            # all the valid df lookup values for the t-table
            list_of_lookup_dfs = sorted(cls.t_table.keys())
            for lookup_df in range(len(list_of_lookup_dfs)):
                current_key = list_of_lookup_dfs[lookup_df]
                if current_key == df:
                    return df
                elif max(current_key, df) == current_key:
                    return last_key
                else:
                    last_key = current_key

    @classmethod
    def _get_alpha(cls, cl: float, tail: str):
        """Return alpha(\u03b1), determined by CL and tailed-ness.

        \u03b1 = 1 - CL

        \u03b1 = (1 - CL) / 2 for two-tailed tests, to account for both
        possible extreme tails in the distribution."""
        alpha = (1 - cl) / 2 if tail == "two" else (1 - cl)
        return round(alpha, 3)

    @classmethod
    def get_score_critical(
            cls, data1: tuple, cl: float = 0.95,
            is_population: bool = False, tail: str = "two",
            verbose: bool = False) -> float or tuple:
        """Return a float of the appropriate critical T-score.

        This score is used by hypothesis tests and mean confidence
        intervals. The score returned is determined by several factors:

        **\u03b1** :
            alpha, determined by the confidence level (\u03b1 = 1 - CL).
            For two-tailed tests, \u03b1 = (1 - CL) / 2, in order to
            account for both extreme possible tails of the distribution.

        **df**:
            degrees of freedom in the dataset (df = n - 1).
            For multiple datasets, df = n1 + n2 - 2

        **Tail-Type**:
            whether test is one-tailed (left/right) or two-tailed (most
            common).

      * For large degrees of freedom (**df>150**), or when the
        population variance is known (**is_population=True**), the
        data is assumed to be approximately normal, and a **Z-score**
        is returned instead of a T-score.
        """
        cls._data_validation(data1)
        lookup_df = cls._get_lookup_df(data1, is_population)
        lookup_alpha = cls._get_alpha(cl=cl, tail=tail)
        test_type = "z" if lookup_df == 999 else "t"
        critical_score = cls.t_table[lookup_df][lookup_alpha]
        if verbose:
            return test_type, lookup_alpha, critical_score
        else:
            return critical_score

    @classmethod
    def get_moe(cls, data: tuple or list, cl=0.95,
                is_population=False, tail="two") -> float:
        """Return margin of error of the data.

        .. math::
            E = score_c * sterr
        """
        cls._data_validation(data)
        critical_score = cls.get_score_critical(
            data, cl=cl, is_population=is_population, tail=tail)
        sterr = cls.get_sterr(data, is_population)
        return critical_score * sterr

    @classmethod
    def get_ci(cls, data: tuple or list, cl=0.95,
               is_population=False, tail="two") -> tuple:
        """Return a tuple of lower/upper confidence interval boundaries

        Calculates the lower mean estimation and upper mean estimation
        at confidence level = cl, default 0.95 (95% confidence).

        CI = mean \u00B1 t-score * sterr
        """
        cls._data_validation(data)
        mean = cls.get_mean(data)
        e = cls.get_moe(
            data, cl=cl, is_population=is_population, tail=tail
        )
        return mean - e, mean + e

    @classmethod
    def get_score_hyp(
            cls, data1: tuple or list, data2=tuple(), h0: float = 0.0, samples_dependent=False,
            is_population=False, verbose=False) -> float or tuple:
        """
        Return the calculated T-score for the supplied data.

        Based on supplied information, will perform one of the following
        tests:
        Single-Population Z-test

        Single-Population T-test

        Two-Population Z-Test

        Two-Population Dependent T-Test

        Two-Population Independent T-Test

        Parameters:
            data1: tuple or list, first data set
            data2: optional, tuple or list, second data set
            h0: optional, float, default 0.0, the null hypothesis
            samples_dependent: optional, bool, default False, whether the samples are dependent.
            is_population: optional, bool, default False, whether the population variation is known.
            verbose: optional, bool, default False, when checked return tuple of (score, score type, test type)
        """
        cls._data_validation(data1)
        from math import sqrt

        df = cls._get_lookup_df(data1, is_population)
        return_score_type = "z" if df == 999 else "t"
        return_test_type = str()
        return_score = float()

        # The hypothesis tests ####

        def test_one_pop(data_: tuple, _is_pop: bool):
            """Return z/t score for hypothesis test

            Assumptions: single population, z/t determined by lookup.
            Note that this equation also holds true for the difference
            of two dependent populations.

            .. math::
                Z = \\frac{x^- - \\mu_0}{\\sigma/\\sqrt{n}}

                T = \\frac{x^- - \\mu_0}{s/\\sqrt{n}}"""
            x_bar = cls.get_mean(data_)
            s_x = cls.get_stdev(data_, is_population=_is_pop)
            n_x = cls.get_n(data_)
            return (x_bar - h0) / (s_x / sqrt(n_x))

        def test_two_pop_known_var_ind(data1_: tuple, data2_: tuple):
            """Return z score for hypothesis test

            Assumptions: two populations, known population variance

            .. math::
                Z = \\frac{(x^- - y^-) - \\mu_0}{\\sqrt{\\sigma^2_x/n_x + \\sigma^2_y/n_y}}"""
            x_bar = cls.get_mean(data1_)
            y_bar = cls.get_mean(data2_)
            var_x = cls.get_var(data1_, is_population=True)
            var_y = cls.get_var(data2_, is_population=True)
            n_x = cls.get_n(data1_)
            n_y = cls.get_n(data2_)
            return (x_bar - y_bar) / sqrt(var_x / n_x + var_y / n_y)

        def test_two_pop_unknown_var_ind(data1_: tuple, data2_: tuple):
            """Return t score for hypothesis test

            Assumptions: two populations, unknown population variance,
            independent data sets, variances are equal

            .. math::
                T = \\frac{(x^- - y^-) - \\mu_0}{\\sqrt{s^2_p/n_x
                + s^2_p/n_y}}"""
            x_bar = cls.get_mean(data1_)
            y_bar = cls.get_mean(data2_)
            var_pool = cls.get_var_pool(data1_, data2_)
            n_x = cls.get_n(data1_)
            n_y = cls.get_n(data2_)
            return (x_bar - y_bar) / sqrt(var_pool / n_x + var_pool / n_y)

        # Test determination
        if cls.get_n(data2) == 0:
            # if data2 is empty, treat as single pop test
            return_score = test_one_pop(data1, is_population)
            return_test_type = "single population"
        elif df == 999:
            # if df > 150 or is_population, it's a z-test
            return_score = test_two_pop_known_var_ind(data1, data2)
            return_test_type = "two pop, known var"
        elif samples_dependent:
            # if samples are dependent, e.g. before-after weigh-ins
            return_score = test_one_pop(
                cls.get_data_diff(data1, data2), _is_pop=is_population
            )
            return_test_type = "two pop, dep"
        else:
            # if two independent samples
            return_score = test_two_pop_unknown_var_ind(data1, data2)
            return_test_type = "two pop, unk var"
        if verbose:
            return return_score, return_score_type, return_test_type
        else:
            return return_score


if __name__ == "__main__":
    pass

