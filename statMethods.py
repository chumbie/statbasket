
class StatMe:

    # Basic Data Attributes ####################################

    @classmethod
    def get_n(cls, data: tuple) -> int:
        """Return the sample size of the dataset."""
        return len(data)

    @classmethod
    def get_df(cls, data: tuple) -> int:
        """Return the degrees of freedom for the dataset.

        .. math::
            df = n - 1
            """
        n = cls.get_n(data)
        df = n - 1
        return df

    @classmethod
    def get_min(cls, data: tuple) -> float:
        """Return the smallest value in the dataset."""
        return min(data)

    @classmethod
    def get_max(cls, data: tuple) -> float:
        """Return the largest value in the dataset."""
        return max(data)

    # Measures of Central Tendency ####################################

    @classmethod
    def get_range(cls, data: tuple) -> float:
        """Return the range of the data

        .. math::
            Range = x_max - x_min"""
        return cls.get_max(data) - cls.get_min(data)

    @classmethod
    def get_mean(cls, data: tuple) -> float:
        """Return the average value in the dataset to 5 decimal places.

        .. math::
            mean = \\frac{\sum_{i=1}^{n}data}{n}
        """
        try:
            return round(sum(data) / cls.get_n(data), 5)
        except ZeroDivisionError as exc:
            # if empty set
            return 0

    @classmethod
    def get_median(cls, data: tuple) -> float:
        """Return the median of the dataset.

        The median is middlemost value of the dataset, or the average
         between the two middlemost values where n % 2 = 0 (even)"""
        # Sort the data
        sorted_data = sorted(list(data))
        # Checks if n is odd, if so return middle value
        if len(sorted_data) % 2 == 1:
            from math import ceil
            return float(sorted_data[ceil(len(sorted_data) / 2)])
        # If n is even, gets the average of the middle two values
        else:
            median_left = sorted_data[int(len(sorted_data) / 2)]
            median_right = sorted_data[int(len(sorted_data) / 2 - 1)]
            return_median = (median_left + median_right) / 2
            return round(return_median, 5)

    @classmethod
    def get_mode(cls, data: tuple) -> tuple or str:
        """Return 'None' or tuple of one, two or three modes.
        
        The mode of the dataset is the value which appears most frequently, 
        e.g. the mode of (1, 2, 2, 3) = 2. Method returns 'None' if number 
        of modes is either greater than three or fewer than one.
        """
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
        if len(mode_list) > 3 or len(mode_list) == 0:
            return "None"
        else:
            return tuple(mode_list)

    @classmethod
    def get_skew(cls, data: tuple) -> float:
        """Return the skewness of the data, using the skewness formula:

        .. math::
            skewness = \\frac{(1/n)\sum_{i=1}^{n}(x_{i} - mean)^{3}}{stdev^3}
            """
        skewness = 0.0
        for each_item in data:
            skewness += (each_item - cls.get_mean(data)) ** 3
        skewness = (skewness * 1 / cls.get_n(data)) / cls.get_stdev(data) ** 3
        return round(skewness, 5)

    # Measures of Data Variation ######################################

    @classmethod
    def get_var(cls, data: tuple, is_population=False) -> float:
        """Return the variance (s\u00b2) of each data set as a tuple.

        .. math::
            s^2 = \\frac{\sum_{i=1}^{n}(x_{i} - mean)^{2}}{n}
        """
        variance = 0.0
        for each_item in data:
            variance += (each_item - cls.get_mean(data)) ** 2
        # Checks whether is a population or sample
        if is_population:
            variance = variance / len(data)
        else:
            variance = variance / (len(data) - 1)
        return round(variance, 5)

    @classmethod
    def get_stdev(cls, data: tuple) -> float:
        """Calculates the standard deviation (s) of the data set

        .. math::
            s = \sqrt{s^2}
        """
        from math import sqrt
        return round(sqrt(cls.get_var(data)), 5)

    @classmethod
    def get_sterr(cls, data: tuple) -> float:
        """Calculates the standard error of the data set

        .. math::
            SE = s/\sqrt{n}
        """
        from math import sqrt
        return round(cls.get_stdev(data) / sqrt(cls.get_n(data)), 5)

    @classmethod
    def get_cv(cls, data: tuple) -> float:
        """Returns the coefficient of variation

        .. math::
            CV = s/mean"""
        return round(cls.get_stdev(data) / cls.get_mean(data), 5)

    # Two-Population Properties #######################################

    @classmethod
    def get_data_diff(cls, data1: tuple, data2: tuple) -> tuple:
        """Return tuple of differences between the values of two dependent data sets

        Note that this method assumes that the two data sets are
        **dependent** and of **equal length**. This method is meaningless
        when applied to two independent data sets.

        .. math::
            x_{diff,i} = x_{1,i} - x_{2,i}
        """
        data1_len = len(data1)
        data2_len = len(data2)
        if data1_len != data2_len:
            raise ValueError(f"Samples are not of equal length.\n"
                             f"Items in 'data1' = {data1_len}\n"
                             f"Items in 'data2' = {data2_len}")
        else:
            return_list = list()
            for i in range(data1_len):
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
        n1 = cls.get_n(data1)
        var1 = cls.get_var(data1)
        n2 = cls.get_n(data2)
        var2 = cls.get_var(data2)
        return round(((n1 - 1) * var1 + (n2 - 2) * var2) / (n1 + n2 - 2), 5)

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
    def _get_lookup_df(cls, df_data1, df_data2, df_pop_var_known) -> int:
        """Convert actual df into t_table lookup df."""
        n1 = cls.get_n(df_data1)
        n2 = cls.get_n(df_data2)
        subtractor = 1 if n2 == 0 else 2
        df = n1 + n2 - subtractor
        if df > 150 or df_pop_var_known:
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
    def get_score_critical(
            cls, data1: tuple, cl=0.95,
            data2=tuple(), pop_var_known=False, tail="two") -> float:
        """Return a float of the appropriate critical T-score.
        
        This score is used by hypothesis tests and mean confidence intervals.
        The score returned is determined by several factors:

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

            * For large degrees of freedom (**df>150**), or when the population
              variance is known (**pop_var_known=True**), the data is assumed to 
              be approximately normal, and a **Z-score** is returned instead of a 
              T-score.
        """

        lookup_df = cls._get_lookup_df(data1, data2, pop_var_known)
        lookup_alpha = (1 - cl) / 2 if tail == "two" else (1 - cl)
        return cls.t_table[lookup_df][lookup_alpha]

    @classmethod
    def get_moe(cls, data: tuple, cl=0.95, pop_var_known=False, tail="two") -> float:
        """Return margin of error of the data.

        .. math::
            E = score_c * sterr
        """
        critical_score = cls.get_score_critical(
            data, cl=cl, pop_var_known=pop_var_known, tail=tail)
        sterr = cls.get_sterr(data)
        return critical_score * sterr

    @classmethod
    def get_ci(cls, data: tuple, cl=0.95, pop_var_known=False, tail="two"):
        """Return a tuple with the lower and upper bound of the confidence interval

        Calculates the lower mean estimation and upper mean estimation at
        confidence level = cl, default 0.95 (95% confidence).

        CI = mean \u00B1 t-score * sterr
        """
        mean = cls.get_mean(data)
        e = cls.get_moe(data, cl=cl, pop_var_known=pop_var_known, tail=tail)
        return mean - e, mean + e

    @classmethod
    def get_score_hyp(
            cls, data1, data2=tuple(), h0=0, samples_dependent=False,
            pop_var_known=False, more_info=False) -> float or tuple:
        """Return the calculated T-score for the supplied data."""
        from math import sqrt

        def validate_data():
            if samples_dependent:
                if cls.get_n != cls.get_n(data2):
                    raise ValueError("Dependent data sets must have the same number of items.")

        validate_data()

        df = cls._get_lookup_df(data1, data2, pop_var_known)

        # The hypothesis tests
        def test_one_pop():
            """Return z/t score for hypothesis test

            Assumptions: single population, z/t determined by lookup.

            .. math::
                Z = \\frac{x^- - \\mu_0}{\\sigma/\\sqrt{n}}

                T = \\frac{x^- - \\mu_0}{s/\\sqrt{n}}"""
            x_bar = cls.get_mean(data1)
            s_x = cls.get_stdev(data1)
            n_x = cls.get_n(data1)
            return (x_bar - h0) / (s_x / sqrt(n_x))

        def test_two_pop_known_var_ind():
            """Return z score for hypothesis test

            Assumptions: two populations, known population variance

            .. math::
                Z = \\frac{(x^- - y^-) - \\mu_0}{\\sqrt{\\sigma^2_x/n_x + \\sigma^2_y/n_y}}"""
            x_bar = cls.get_mean(data1)
            y_bar = cls.get_mean(data2)
            var_x = cls.get_var(data1)
            var_y = cls.get_var(data2)
            n_x = cls.get_n(data1)
            n_y = cls.get_n(data2)
            return (x_bar - y_bar) / sqrt(var_x / n_x + var_y / n_y)

        def test_two_pop_unknown_var_dep():
            """Return t score for hypothesis test

            Assumptions: two populations, unknown population variance, dependent data sets

            .. math::
                T = \\frac{d^- - \\mu_0}{s_d / \\sqrt{n}}"""
            data_d = cls.get_data_diff(data1, data2)
            d_bar = cls.get_mean(data_d)
            s_d = cls.get_stdev(data_d)
            n_d = cls.get_n(data_d)
            return (d_bar - h0) / (s_d / sqrt(n_d))

        def test_two_pop_unknown_var_ind():
            """Return t score for hypothesis test

            Assumptions: two populations, unknown population variance,
            independent data sets, variances are equal

            .. math::
                T = \\frac{(x^- - y^-) - \\mu_0}{\\sqrt{s^2_p/n_x
                + s^2_p/n_y}}"""
            x_bar = cls.get_mean(data1)
            y_bar = cls.get_mean(data2)
            var_pool = cls.get_var_pool(data1, data2)
            n_x = cls.get_n(data1)
            n_y = cls.get_n(data2)
            return (x_bar - y_bar) / sqrt(var_pool / n_x + var_pool / n_y)

        # Test determination
        if len(data2) == 0:
            # if data2 is empty, treat as single pop test
            return test_one_pop()
        elif df == 999:
            # if df > 150 or pop_var_known, it's a z-test
            return test_two_pop_known_var_ind()
        elif samples_dependent:
            # if samples are dependent, e.g. before-after weigh-ins
            return test_two_pop_unknown_var_dep()
        else:
            # if two independent samples
            return test_two_pop_unknown_var_ind()
