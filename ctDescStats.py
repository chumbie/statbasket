"""
ctDescStats.py

Contains the DescriptiveStats class, which accepts a list or tuple 
containing data, and outputs useful descriptive statistics derived from 
that data set. Assumes data is a sample of a population, unless 
is_population=True

Classes:
    DescriptiveStats
"""


class DescriptiveStats:
    """
    Class which provides simple descriptive statistics for a supplied tuple
    dataset.

    Summary:
    __________
    For a description of the data set, print the class object as a string. Note that
    statistics in the display table are rounded to 3 decimal places. For unrounded
    statistics, use the class attributes (self.mean, etc.).

    Usage:
    ___________
    DescriptiveStats(tuple_data : tuple [, is_population : False [, data_name : str]]

    Attributes:
    __________
    data : tuple
        data supplied by user, in tuple form.
    is_population : bool
        indicates whether data is a sample or a population (default False)
    cl : float
        confidence level for confidence interval calculations, accepted
        values are 0.90, 0.95, 0.98, and 0.99 (default 0.95)
    data_name : str
        name given to the data set, appears on the display (default None)
    n : int
        Size of the sample or population, i.e. len(data).
    min : float
        The smallest value in the data set, i.e. min(data)
    max : float
        The largest value in the data set, i.e. max(data)
    range : float
        The range of the data, i.e. max - min
    mean : float
        The average value in the data set, i.e. sigma^nvi(xi)/n
    median : float
        The middlemost value in the data set.
    mode : tuple
        The value with the most repetitions in the data set. Can be either
        zero, one, two, or three modes. Zero or >3 modes results in "N/A".
    variance : float
        The variance of the data, i.e. sigma^nvi((x-mean)^2)/n
    stdev : float
        The standard deviation of the data set, i.e. sqrt(variance)
    sterr : float
        The standard error of the data set, i.e. stdev/sqrt(n)
    cov : float
        The coefficient of variation of the data set, i.e. stdev/mean
    skew : float
        The skewness of the dataset from 0 to positive infinity, i.e.
        sigma^nvi((xi - mean)^3)/((n-1)(sigma)^3)

    Methods:
    __________
    mean_calculate() -> float
        Calculates the mean of the data set, i.e. sigma^nvi(xi)/n
    median_calculate() -> float
        Calculates the middlemost value in the data set.
    mode_calculate() -> tuple
        Calculates the value with the most repetitions in the data set. Can be either
        zero, one, two, or three modes. Zero or >3 modes results in "N/A".
    variance_calculate() float
        Calculates the variance of the data, i.e. sigma^nvi((x-mean)^2)/n
    standard_deviation_calculate() -> float
        Calculates the standard deviation of the data set, i.e. sqrt(variance)
    standard_error_calculate() -> float
        Calculates the standard error of the data set, i.e. stdev/sqrt(n)
    coefficient_of_variation_calculate() -> float
        Calculates the coefficient of variation of the data set, i.e. stdev/mean
    skewness_calculate -> float
        Calculates the skewness of the dataset from 0 to positive infinity, i.e.
        sigma^nvi((xi - mean)^3)/((n-1)(sigma)^3)
    """

    def __init__(self, data: tuple, is_population=False, cl=0.95, data_name="data"):
        """
        Parameters
        __________
        data : tuple
            Data supplied by user, in tuple form.
        is_population : bool, optional
            Default False, indicates whether data is a sample (False) or a
            population (True).
         cl : float
            confidence level for confidence interval calculations, accepted
             values are 0.90, 0.95, 0.98, and 0.99 (default 0.95)
        data_name : str, optional
            Default none, name given to the data set, appears on the display.
        """

        self.data = data
        self.is_population = is_population
        self.cl = cl
        self.data_name = data_name

        # # Data validation # #
        assert isinstance(data, tuple or list), \
            f"Data is of type '{type(data).__name__}'. Acceptable types: 'tuple', 'list'"
        assert isinstance(is_population, bool), \
            f"is_population is of type '{type(is_population).__name__}', must be type 'bool' (True or False)."
        assert cl in (0.90, 0.95, 0.98, 0.99), \
            f"Provided confidence level (cl={str(cl)}) is not 0.90, 0.95, 0.98, or 0.99."
        assert isinstance(data_name, str), f"data_name {str(data_name)} is not a string."

        # # Calculated attributes # #
        self.n = len(self.data)
        self.df = self.n - 1
        self.t_score = self.t_score_calculate()

        # Measures of central tendency
        self.min = min(data)
        self.max = max(data)
        self.range = self.max - self.min
        self.mean = self.mean_calculate()
        self.median = self.median_calculate()
        self.mode = self.mode_calculate()

        # Measures of data variation
        self.variance = self.variance_calculate()
        self.stdev = self.standard_deviation_calculate()
        self.sterr = self.standard_error_calculate()
        self.cov = self.coefficient_of_variation_calculate()
        self.skew = self.skewness_calculate()

        # Confidence interval of mean
        self.ci = self.confidence_interval_calculate()

    def t_score_calculate(self) -> float:
        """Return the t-score applicable to the data's degrees of freedom
        and confidence level. See studentT.py for full t-table."""
        # nested tuple of student t-scores
        from studentT import t_table
        # first index to get t-score
        t_score_df_index = 0
        if self.df <= 30:
            t_score_df_index = self.df
        elif 30 < self.df <= 35:
            t_score_df_index = 30
        elif 35 < self.df <= 40:
            t_score_df_index = 31
        elif 40 < self.df <= 50:
            t_score_df_index = 32
        else:
            t_score_df_index = 35
        # If population, use z-score (infinity) index
        if self.is_population:
            print("True")
            t_score_df_index = 35
        print(f"df = {self.df}")
        print(f"t_score_df_index = {t_score_df_index}")
        t_score_cl_dict = {0.90: 1, 0.95: 2, 0.98: 3, 0.99: 4}
        # second index, uses above dict to get index
        t_score_cl_index = t_score_cl_dict[self.cl]
        # t-score comes from two indices, pulls from t-table
        return t_table[t_score_df_index][t_score_cl_index]

    def mean_calculate(self) -> float:
        """Return the average of the dataset."""
        return sum(self.data) / self.n

    def confidence_interval_calculate(self) -> tuple:
        """Return the upper and lower mean estimations of population, give
        the confidence interval (self.cl, default 0.95).
        CI = mean +- t-score * sterr"""
        margin_of_error = self.t_score * self.sterr  # moe = t-score * sterr
        lower_mean = self.mean - margin_of_error
        upper_mean = self.mean + margin_of_error
        ci = (lower_mean, upper_mean)
        return ci

    def median_calculate(self) -> float:
        """Calculate the median of the dataset"""
        # Sort the data
        sorted_data = sorted(list(self.data))
        # Checks if n is odd, if so return middle value
        if len(sorted_data) % 2 == 1:
            return float(sorted_data[int(len(sorted_data) / 2)])
        # If n is even, gets the average of the middle two values
        else:
            median_left = sorted_data[int(len(sorted_data) / 2)]
            median_right = sorted_data[int(len(sorted_data) / 2 - 1)]
            median = (median_left + median_right) / 2
            return median

    def mode_calculate(self) -> tuple:
        """Accept data tuple, return tuple with one, two or three modes,
        or 'N/A' if number of modes exceeds three or less than one."""
        highest_count = 0
        highest_count_items = set()
        mode_list = list()
        count_dict = dict()
        for each_item in self.data:
            count_dict.setdefault(each_item, 0)
            count_dict[each_item] += 1
            if count_dict[each_item] >= highest_count:
                highest_count_items.add(each_item)
                highest_count = count_dict[each_item]
        for each_item in highest_count_items:
            if count_dict[each_item] == highest_count:
                mode_list.append(each_item)
        # mode_list now contains all items equal to the highest
        # repetitions among data points.
        if len(mode_list) > 3 or len(mode_list) == 0:
            return tuple("N/A", )
        else:
            return tuple(mode_list)

    def variance_calculate(self) -> float:
        """Calculates the variance of the data set, which is the sum of the squares of the difference
        between each data point and the mean, divided by the sample size minus one."""
        variance = float()
        for each_item in self.data:
            variance += (each_item - self.mean) ** 2
        # Checks whether is a population or sample
        if self.is_population:
            variance = variance / len(self.data)
        else:
            variance = variance / (len(self.data) - 1)
        return round(variance, 3)

    def standard_deviation_calculate(self) -> float:
        """Calculates the standard deviation of the data set, which is the
        square root of the variance."""
        from math import sqrt
        return round(float(sqrt(self.variance_calculate())), 3)

    def standard_error_calculate(self) -> float:
        """Calculates the standard error of the data set, i.e. stdev/sqrt(n)"""
        from math import sqrt
        return self.standard_deviation_calculate() / sqrt(self.n)

    def coefficient_of_variation_calculate(self) -> float:
        """Calculates the coefficient of variation, which is the
        standard deviation divided by the mean."""
        return round(float(self.stdev / self.mean), 3)

    def skewness_calculate(self) -> float:
        """Measures the skewness of the data, using the skewness formula:
        Skewness = ((1/n)Sigma^Nvi(Xi - Xbar)^3)/(sigma)^3)"""
        skewness = 0.0
        for each_item in self.data:
            skewness += (each_item - self.mean)**3
        skewness = (skewness*1/self.n)/(self.stdev**3)
        return skewness

    def __repr__(self):
        n_type = ""
        n_letter = ""
        if self.is_population:
            n_type = "Population"
            n_letter = "N"
        else:
            n_type = "Sample"
            n_letter = "n"
        if self.data_name:
            desc = f' Description of {self.data_name} '
        else:
            desc = f" Description of {n_type} "
        general_stats = f" General {n_type} Statistics "
        size = f"Size of {n_type} ({n_letter})"
        print_n = "{:,}".format(self.n)
        print_min = "{:,}".format(self.min)
        print_max = "{:,}".format(self.max)
        print_mean = "{:,}".format(round(self.mean, 3))
        print_ci_desc = f"CI ({self.cl:.0%}, t={self.t_score}, df={self.df})"
        print_ci = "[{:,}".format(round(self.ci[0], 3)) + ", {:,}]".format(round(self.ci[1], 3))
        print_median = "{:,}".format(round(self.median, 3))
        if type(self.mode[0]) == str:
            print_mode = "N/A"
        else:
            mode_list = list()
            for i in range(len(self.mode)):
                mode_list.append("{:,}".format(round(self.mode[i])))
            print_mode = ", ".join(mode_list)
        print_range = "{:,}".format(round(self.range, 3))
        print_var = "{:,}".format(round(self.variance, 3))
        print_stdev = "{:,}".format(round(self.stdev, 3))
        print_sterr = "{:,}".format(round(self.sterr, 3))
        print_cov = "{:,}".format(round(self.cov, 3))
        print_skew = "{:,}".format(round(self.skew, 3))
        L_WIDTH = max(len(print_ci_desc), len(print_cov))
        R_WIDTH = max(len(str(print_var)) + 1, len(str(self.data_name)), len(str(print_ci_desc)))
        TOTAL_WIDTH = L_WIDTH + R_WIDTH + 4

        return \
f""" {"_" * TOTAL_WIDTH}
|{"=" * TOTAL_WIDTH}|
|{desc.center(TOTAL_WIDTH, "=")}|
|{"=" * TOTAL_WIDTH}|
|{" " * TOTAL_WIDTH}|
|{general_stats.center(TOTAL_WIDTH, "-")}|
|{" " * TOTAL_WIDTH}|
| {size.center(L_WIDTH) + " : " + print_n.center(R_WIDTH)}|
|{" " * TOTAL_WIDTH}|
| {"Minimum Value (min)".center(L_WIDTH) + " : " + print_min.center(R_WIDTH)}|
|{" " * TOTAL_WIDTH}|
| {"Maximum Value (max)".center(L_WIDTH) + " : " + print_max.center(R_WIDTH)}|
|{" " * TOTAL_WIDTH}|
|{" Central Tendency ".center(TOTAL_WIDTH, "-")}|
|{" " * TOTAL_WIDTH}|
| {"Mean".center(L_WIDTH) + " : " + print_mean.center(R_WIDTH)}|
|{" " * TOTAL_WIDTH}|
| {print_ci_desc.center(L_WIDTH) + " : " + print_ci.center(R_WIDTH)}|
|{" " * TOTAL_WIDTH}|
| {"Median".center(L_WIDTH) + " : " + print_median.center(R_WIDTH)}|
|{" " * TOTAL_WIDTH}|
| {"Mode".center(L_WIDTH) + " : " + print_mode.center(R_WIDTH)}|
|{" " * TOTAL_WIDTH}|
| {"Range".center(L_WIDTH) + " : " + print_range.center(R_WIDTH)}|
|{" " * TOTAL_WIDTH}|
|{" Level of Variation ".center(TOTAL_WIDTH, "-")}|
|{" " * TOTAL_WIDTH}|
| {"Variance".center(L_WIDTH) + " : " + print_var.center(R_WIDTH)}|
|{" " * TOTAL_WIDTH}|
| {"Standard Deviation".center(L_WIDTH) + " : " + print_stdev.center(R_WIDTH)}|
|{" " * TOTAL_WIDTH}|
| {"Standard Error".center(L_WIDTH) + " : " + print_sterr.center(R_WIDTH)}|
|{" " * TOTAL_WIDTH}|
| {"Coefficient of Variation".center(L_WIDTH) + " : " + print_cov.center(R_WIDTH)}|
|{" " * TOTAL_WIDTH}|
| {"Skewness".center(L_WIDTH) + " : " + print_skew.center(R_WIDTH)}|
{"|" + "_" * (TOTAL_WIDTH) + "|"}
"""


if __name__ == "__main__":
    data = (1, 1, 1, 2, 3, 4, 5, 6, 7)
    # DescriptiveStats(data).t_score_calculate()
    print(DescriptiveStats(data))
