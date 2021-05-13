"""
ctDescStats.py

Contains the DescriptiveStats class, which accepts a list or tuple 
containing data, and outputs useful descriptive statistics derived from 
that data set. Assumes data is a sample of a population, unless 
is_population=True

Classes:
    DescriptiveStats
"""
# Standard Python Imports
import functools  # for decorator wrapper functions i.e. @functools.wraps

# Third-Party Imports
from statMethods import StatMe

# TODO: Clean up statBasket.py, remove duplicate methods
#  (everything now in statMethods.py)
# TODO: refactor StatBasket so that it can create object which has
#  attributes for each of the class methods in statMethods. The idea is
#  for large datasets, can create everything all at once, so can refer
#  to attributes without having to continuously recalculate.
class StatBasket:
    """
    Class which provides simple descriptive statistics for a supplied tuple
    dataset.

    Summary:
    __________
    For a description of the data set, print the class object as a string.
    Note that statistics in the display table are rounded to 3 decimal
    places. For unrounded statistics, use the class attributes
    (self.mean, etc.).

    Usage:
    ___________
    StatBasket(data: tuple [, is_population: False [, data_name: str]]

    Attributes:
    __________
    data : tuple
        data supplied by user, in tuple form.
    is_population : bool
        indicates whether data is a sample or a population (default False)
    cl : float
        confidence level for confidence interval calculations, accepted
        values are 0.90, 0.95, and 0.99 (default 0.95)
    tail : str
        default "two", the tailed nature of the test. Options are "two",
        "left", or "right".
    data_name : str
        name given to the data set, appears on the display (default None)

    Properties:
    ___________
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
    """

    def __repr__(self):
        return f"a StatBasket object."

    def __init__(self,
                 data1: tuple,
                 data2=tuple(),
                 is_population=False,
                 samples_dependent=False,
                 cl=0.95,
                 tail="two",
                 first_name="data",
                 second_name="data"):
        """
        Parameters
        __________
        data : tuple
            Data supplied by user, in tuple form. To supply multiple data
            sets, supply a tuple of tuples ((1, 2, 3),(4, 5, 6)).
        is_population : bool, optional
            Default False, indicates whether data is a sample (False) or a
            population (True).
        cl : float
            confidence level for confidence interval calculations, accepted
             values are 0.90, 0.95, and 0.99 (default 0.95)
        tails : str
            Default "two", indicates what type of tail in hypothesis testing,
            accepted values are "two", "left", or "right", for two-tailed,
            left-tailed, or right-tailed hypothesis testing, respectively.
        data_name : str, optional
            Default "data", name given to the data set, appears on the display.
        """

        # Data Validation #############################################

        def data_validation():
            # Validate data in tuple form
            if not isinstance(data1, tuple):
                raise ValueError(
                       f"Data is of type '{type(data1).__name__}'. "
                       f"Acceptable types: 'tuple'")

            # Validate, only int or float data in data tuples
            data_type_error_list = []
            error_help = str()
            for i in range(len(data1)):
                if isinstance(data1[i], tuple):
                    # print("Detected tuple")
                    error_help = f"data_index, value_index, value"
                    for j in range(len(data1[i])):
                        # print("inside nested tuple")
                        if not isinstance(data1[i][j], (int, float)):
                            data_type_error_list.append((i, j, data1[i][j]))
                elif not isinstance(data1[i], (int, float)):
                    # print("Non-nested tuple")
                    error_help = f"value_index, value"
                    data_type_error_list.append((i, data1[i]))
            # Any non-int, non-float members will be added to error
            if len(data_type_error_list) != 0:
                raise ValueError(f"One or more values in dataset are non-numeric \n"
                                 f"({error_help}): {tuple(data_type_error_list)}")

            if not isinstance(is_population, bool):
                raise ValueError(
                    f"is_population is of type '{type(is_population).__name__}', must be of type 'bool'.")
            if cl not in (0.90, 0.95, 0.99):
                raise ValueError(f"Confidence level (cl={str(cl)}) is not 0.90, 0.95, or 0.99.")
            if tail not in ("two", "left", "right"):
                raise ValueError(f"Tail attribute value (tail={str(tail)}) is not 'two', 'left', or 'right'.")
            wrong_name = str()
            if not isinstance(first_name, str):
                wrong_name = first_name
            if not isinstance(second_name, str):
                wrong_name = second_name
            if wrong_name != '':
                raise ValueError(f"data_name {str(wrong_name)} is not a string.")

        data_validation()
        # Primary Attributes ##########################################

        self.data = data1, data2
        self.is_population = is_population
        self.samples_dependent = samples_dependent
        self.cl = cl
        self.tail = tail
        # self.first_index = first_index
        # self.second_index = second_index
        self.data_name = first_name

    # Nested Tuple Detection Decorator (experimental) ################################

    # # @staticmethod
    # def nested_tuple_detector(func):
    #     """This function only runs if it detects that data is nested tuples."""
    #     def inner(self):
    #         if isinstance(self.data[0], tuple):
    #             return_list = list()
    #             for each in self.data:
    #                 return_list.append(func(each))
    #             return tuple(return_list)
    #         else:
    #             return func(self.data)
    #     return inner

    # @staticmethod
    # def n_calc(dataset: tuple):
    #     """Return the number of elements in the dataset"""
    #     return len(dataset)
    """"""
    def overwrapper_to_pass_stat_function(stat_function):
        """Passes the appropriate stat function to the property function."""
        def actual_decorator(func):
            """If one dataset, return single float/int, else return tuple"""
            @functools.wraps(func)  # lets functions keep their docs, etc.
            def inner(self):
                # checks if un-nested tuple
                if isinstance(self.data[0], (float, int)):
                    return (stat_function(self.data))
                else:
                    # performs function to each nested tuple
                    return_list = list()
                    for each in self.data:
                        if each == ():
                            break
                        return_list.append(stat_function(each))
                    return tuple(return_list)
                    func_return = func(self)
                    if func_return[1] == ():
                        return func(self, stat_function)[0]
            return inner
        return actual_decorator

        # Calculated Data Properties ######################################

    class TestClass:
        @staticmethod
        def get_n(data):
            return len(data)

    @property
    @overwrapper_to_pass_stat_function(TestClass.get_n)
    def n(self, stat_function):
        return stat_function(self.data)

    @property
    def df(self) -> tuple:
        return_list = list()
        for each in self.n:
            if each == ():
                break
            return_list.append(each - 1)
        return tuple(return_list)

    @property
    def _dflookup(self) -> tuple:
        """Return self.df converted into an acceptable df lookup value
        for t-table dictionary."""
        return_df_lookup = list()
        for i in range(len(self.df)):
            if self.df[i] > 150 or self.is_population:
                return_df_lookup.append(999)
            elif self.df[i] <= 30:
                return_df_lookup.append(self.df[i])
            else:
                # stores the previous key in the loop
                last_key = 0
                # all the valid df lookup values for the t-table
                list_of_lookup_dfs = list(self.t_table.keys())
                for score in range(len(list_of_lookup_dfs)):
                    current_key = list_of_lookup_dfs[score]
                    if current_key == self.df[i]:
                        return_df_lookup.append(self.df[i])
                        break
                    elif max(current_key, self.df[i]) == current_key:
                        return_df_lookup.append(last_key)
                        break
                    else:
                        last_key = current_key
        return tuple(return_df_lookup)

    @property
    def alpha(self) -> float:
        """Returns the alpha value for the datasets rounded to three
        decimal places, based on self.cl"""
        return_alpha = (1 - self.cl) / 2 if self.tail == "two" else 1 - self.cl
        return round(return_alpha, 3)

    # Measures of Central Tendency ####################################

    @property
    def min(self) -> tuple:
        """Return the smallest value in the dataset."""
        return_list = list()
        for data in self.data:
            if data == ():
                break
            return_list.append(min(data))
        return tuple(return_list)

    @property
    def max(self) -> tuple:
        """Return the largest value in the dataset."""
        return_list = list()
        for data in self.data:
            if data == ():
                break
            return_list.append(max(data))
        return tuple(return_list)

    @property
    def range(self) -> tuple:
        """Return the range of the data

        * range = max - min"""
        return_list = list()
        for i in range(len(self.data)):
            if self.data[i] == ():
                break
            return_list.append(self.max[i] - self.min[i])
        return tuple(return_list)

    @property
    def mean(self) -> tuple:
        """Return the average value in the dataset,

        .. math::
            mean = \\frac{\sum_{i=1}^{n}data}{n}
        """
        return_list = list()
        for i in range(len(self.data)):
            if self.data[i] == ():
                break
            return_list.append(sum(self.data[i]) / self.n[i])
        return tuple(return_list)

    @property
    def median(self) -> tuple:
        """Return the median (middlemost value) of the dataset, or
        returns the average between the two middlemost values where
        n % 2 = 0 (even)"""
        return_list = list()
        for i in range(len(self.data)):
            if self.data[i] == ():
                break
            # Sort the data
            sorted_data = sorted(list(self.data[i]))
            # Checks if n is odd, if so return middle value
            if len(sorted_data) % 2 == 1:
                return_list.append(float(sorted_data[int(len(sorted_data) / 2)]))
            # If n is even, gets the average of the middle two values
            else:
                median_left = sorted_data[int(len(sorted_data) / 2)]
                median_right = sorted_data[int(len(sorted_data) / 2 - 1)]
                return_median = (median_left + median_right) / 2
                return_list.append(return_median)
        return tuple(return_list)

    @property
    def mode(self) -> tuple:
        """Return tuple of tuples, each which contains one, two or three modes,
        or 'None' if number of modes exceeds three or fewer than one.

        The mode of the dataset is the value which appears most frequently,
        e.g. the mode of (1, 2, 2, 3) = 2"""
        return_list = list()
        for i in range(len(self.data)):
            if self.data[i] == ():
                break
            current_highest_count = int()
            set_of_highest_items = set()
            mode_list = list()
            count_dict = dict()
            for each_item in self.data[i]:
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
                return_list.append(("None",))
            else:
                return_list.append(tuple(mode_list))
        return tuple(return_list)

    @property
    def skew(self) -> tuple:
        """Measures the skewness of the data, using the skewness formula:

        .. math::
            skewness = \\frac{(1/n)\sum_{i=1}^{n}(x_{i} - mean)^{3}}{stdev^3}
            """
        return_list = list()
        for i in range(len(self.data)):
            if self.data[i] == ():
                break
            skewness = 0.0
            for each_item in self.data[i]:
                skewness += (each_item - self.mean[i]) ** 3
            skewness = (skewness * 1 / self.n[i]) / (self.stdev[i] ** 3)
            return_list.append(skewness)
        return tuple(return_list)

    # Measures of Data Variation ######################################

    @property
    def var(self) -> tuple:
        """Return the variance (s\u00b2) of each data set as a tuple.

        .. math::
            s^2 = \\frac{\sum_{i=1}^{n}(x_{i} - mean)^{2}}{n}
        """
        return_list = list()
        for i in range(len(self.data)):
            if self.data[i] == ():
                break
            variance = 0.0
            for each_item in self.data[i]:
                variance += (each_item - self.mean[i]) ** 2
            # Checks whether is a population or sample
            if self.is_population:
                variance = variance / len(self.data[i])
            else:
                variance = variance / (len(self.data[i]) - 1)
            return_list.append(variance)
        return tuple(return_list)

    @property
    def stdev(self) -> tuple:
        """Calculates the standard deviation (s) of the data set

        .. math::
            s = \sqrt{s^2}
        """
        from math import sqrt
        return_list = list()
        for i in range(len(self.data)):
            if self.data[i] == ():
                break
            return_list.append(sqrt(self.var[i]))
        return tuple(return_list)

    @property
    def sterr(self) -> tuple:
        """Calculates the standard error of the data set

        .. math::
            SE = s/\sqrt{n}
        """
        from math import sqrt
        from math import sqrt
        return_list = list()
        for i in range(len(self.data)):
            if self.data[i] == ():
                break
            return_list.append(self.stdev[i] / sqrt(self.n[i]))
        return tuple(return_list)

    @property
    def cv(self) -> tuple:
        """Returns the coefficient of variation

        CV = s/mean"""
        return_list = list()
        for i in range(len(self.data)):
            if self.data[i] == ():
                break
            return_list.append(self.stdev[i] / self.mean[i])
        return tuple(return_list)

    # Z/T-score Properties ############################################

    @property
    def score_type(self) -> tuple:
        """Returns a string representation of the test being performed, based on the provided data.

        Possible return values include:

        * z-score = "z"
        * t-score = "t"
        """
        return_list = list()
        for i in range(len(self._dflookup)):
            if self._dflookup[i] == 999 or self.is_population:
                return_list.append("z")
            else:
                return_list.append("t")
        return tuple(return_list)

    @property
    def score_critical(self) -> tuple:
        """Return the critical score from the t-table for the given confidence level (cl).

        In confidence intervals, this score is called the 'reliability factor'."""
        return_list = list()
        for i in range(len(self._dflookup)):
            try:
                return_list.append(self.t_table[self._dflookup[i]][self.alpha])
            except KeyError as exc:
                raise KeyError(f"t_table lookup cannot interpret df_lookup or alpha (exc={exc}). "
                               f"self.df_lookup = {self._dflookup}, "
                               f"self.alpha = {self.alpha}")
        return tuple(return_list)

    # Two-Population Properties #######################################

    @property
    def data_diff(self) -> tuple:
        """Return tuple of differences between the two dependent data sets

        .. math::
            x_{diff,i} = x_{1,i} - x_{2,i}
        """
        if self.samples_dependent is not True:
            raise ValueError("Samples not dependent. Did you declare samples_dependent=True?")
        else:
            return_list = list()
            for i in range(len(self.data[0])):
                x1 = self.data[self.first_index][i]
                x2 = self.data[self.second_index][i]
                return_list.append(x1 - x2)
            return tuple(return_list)

    @property
    def n_diff(self) -> float:
        """Return the number of datapoints in difference dataset"""
        return len(self.data_diff)

    @property
    def mean_diff(self) -> float:
        """Return the average of the difference between the two dependent data sets"""
        mean_difference = sum(self.data_diff) / self.n_diff
        return mean_difference

    @property
    def var_diff(self) -> float:
        """Return the variance of the differences between the first and second data sets

        .. math::
            s_diff^2 = \\frac{\sum_{i=1}^{n}(x_{i,diff} - mean_diff)^{2}}{n}
        """
        variance_of_difference = 0.0
        for each_item in self.data_diff:
            variance_of_difference += (each_item - self.mean_diff) ** 2
        variance_of_difference = variance_of_difference / (len(self.data_diff) - 1)
        return variance_of_difference

    @property
    def stdev_diff(self) -> float:
        """Return the standard deviation of the differences between the
        first and second data sets

        .. math::
            s_diff = \sqrt{s^2_diff}
        """
        from math import sqrt
        return sqrt(self.var_diff)

    @property
    def sterr_diff(self) -> float:
        """Calculates the standard error of the data set

        .. math::
            SE = s/\sqrt{n}
        """
        from math import sqrt
        return self.stdev_diff / sqrt(self.n[self.first_index])

    @property
    def var_pool(self) -> float:
        """Return the pooled variance between the first and second data sets

        .. math::
            s_p^2 = \\frac{(n_x - 1)s^2_x + (n_y - 1)s^2_y)}{n_x + n_y - 2}
        """
        a = self.n[self.first_index] * self.var[self.first_index]
        b = self.n[self.second_index] * self.var[self.second_index]
        c = self.n[self.first_index] + self.n[self.second_index] - 2
        return (a + b) / c

    # Confidence Interval Properties ##################################

    @property
    def moe(self) -> tuple:
        """
        Return margin of error of the population, used for confidence
        interval calculation.

        E = z-/t-score * sterr
        """
        return_list = list()
        for i in range(len(self.data)):
            if self.data[i] == ():
                break
            return_list.append(self.score_critical[i] * self.sterr[i])
        return tuple(return_list)

    @property
    def moe_diff(self) -> float:
        """
        Return margin of error of the population difference, used for confidence
        interval calculation.

        E = z-/t-score * sterr
        """
        return self.score_critical[0] * self.sterr_diff

    @property
    def ci(self) -> tuple:
        """
        Return (ci_lower, ci_upper)

        Calculates the lower mean estimation and upper mean estimation at
        confidence level = cl, default 0.95 (95% confidence).

        * CI = mean +- t-score * sterr
        """
        return_list = list()
        for i in range(len(self.data)):
            if self.data[i] == ():
                break
            return_list.append((self.mean[i] - self.moe[i], self.mean[i] + self.moe[i]))
        return tuple(return_list)

    @property
    def ci_diff(self) -> tuple:
        """
        Return (ci_lower, ci_upper)

        Calculates the lower mean estimation and upper mean estimation
        at confidence level = cl, default 0.95 (95% confidence).

        .. math::
            CI_diff = mean_diff \\pm t_{\\alpha/2} * SE
        """
        return self.mean_diff - self.moe_diff, self.mean_diff + self.moe_diff

    # Hypothesis Testing Properties and Functions #####################

    def score_hyp_calc(self, h0_mu=0) -> tuple or str:
        """Takes data and null hypothesis, returns a tuple with test score,
        p-value, alpha, and interpretation ("reject null" or "fail to reject null")"""
        # Check that both samples are same length
        if self.samples_dependent:
            assert len(self.data[self.first_index]) == len(self.data[self.second_index]), \
                "Samples flagged 'dependent' but not of equal length.\n" \
                f"len(data1) = {len(self.data[self.first_index])}\n" \
                f"len(data2) = {len(self.data[self.second_index])}"

        from math import sqrt
        return_test_score = float()
        return_score_type = str()
        return_test_type = str()

        def test_one_pop():
            """Return z/t score for hypothesis test
            Assumptions: single population, z/t determined by _dflookup.

            .. math::
                Z = \\frac{x^- - \\mu_0}{\\sigma/\\sqrt{n}}

                T = \\frac{x^- - \\mu_0}{s/\\sqrt{n}}"""
            x_bar = self.mean[self.first_index]
            s = self.stdev[self.first_index]
            n = self.n[self.first_index]
            return (x_bar - h0_mu) / (s / sqrt(n))

        def test_two_pop_known_var_ind():
            """Return z score for hypothesis test

            Assumptions: two populations, known population variance

            .. math::
                Z = \\frac{(x^- - y^-) - \\mu_0}{\\sqrt{\\sigma^2_x/n_x + \\sigma^2_y/n_y}}"""
            x_bar = self.mean[self.first_index]
            y_bar = self.mean[self.second_index]
            var_x = self.var[self.first_index]
            var_y = self.var[self.second_index]
            n_x = self.n[self.first_index]
            n_y = self.n[self.second_index]
            return (x_bar - y_bar) / sqrt(var_x/n_x + var_y/n_y)

        def test_two_pop_unknown_var_dep():
            """Return t score for hypothesis test

            Assumptions: two populations, unknown population variance, dependent data sets

            .. math::
                T = \\frac{d^- - \\mu_0}{s_d / \\sqrt{n}}"""
            d_bar = self.mean_diff
            stdev_d = self.stdev_diff
            n = self.n[self.first_index]
            return (d_bar - h0_mu) / (stdev_d / sqrt(n))

        def test_two_pop_unknown_var_ind():
            """Return t score for hypothesis test

            Assumptions: two populations, unknown population variance, independent data sets, variances are equal

            .. math::
                T = \\frac{(x^- - y^-) - \\mu_0}{\\sqrt{s^2_p/n_x + s^2_p/n_y}}"""

            x_bar = self.mean[self.first_index]
            y_bar = self.mean[self.second_index]
            var_pool = self.var_pool
            n_x = self.n[self.first_index]
            n_y = self.n[self.second_index]
            return (x_bar - y_bar) / sqrt(var_pool / n_x + var_pool / n_y)

        # Set the score type (z or t)
        if "z" in self.score_type:
            return_score_type = "z"
        else:
            return_score_type = "t"

        # For single populations
        if self.second_index is None:
            if "z" in self.score_type:
                return_test_type = "one population, known variance"
            else:
                return_test_type = "one population, unknown variance"
            return_test_score = test_one_pop()

        # For two populations
        else:
            # Z-test
            # Two populations, population variance is known, test for true mean difference
            if "z" in self.score_type:
                return_test_type = "two populations, known variance"
                return_test_score = test_two_pop_known_var_ind()
            # Student t-tests
            else:
                # Samples dependent on one another, e.g. before-after weights
                if self.samples_dependent:
                    return_test_type = "two populations, unknown variance, dependent samples"
                    return_test_score = test_two_pop_unknown_var_dep()
                # Samples independent, population variance assumed equal
                else:
                    return_test_type = "two populations, unknown variance, independent samples"
                    return_test_score = test_two_pop_unknown_var_ind()

        return return_test_score, self.score_critical, return_score_type, return_test_type

    # Other Functions #################################################

    def describe(self, data_set_index=0):
        """Return a string of composition 'top' + 'title' + 'data_table'
        + 'bottom'"""
        n_type = str()
        n_letter = str()
        if self.is_population:
            n_type = "Population"
            n_letter = "N"
        else:
            n_type = "Sample"
            n_letter = "n"

        print_sections = (
            f"General {n_type} Statistics",
            f"Measures of Central Tendency",
            f"Measures of Variation",
            f"Confidence Interval Statistics"
        )
        title = f"DESCRIPTION OF {'DATA' if self.data_name == 'data' else self.data_name}"
        print_dict = dict()
        # Key = section: (Subkey = stat name, Value: stat value)
        print_dict[f"General {n_type} Statistics"] = (
            (f"Size of {n_type} ({n_letter})", "{:,}".format(round(self.n[data_set_index], 3))),
            ("Minimum Value (min)", "{:,}".format(round(self.min[data_set_index], 3))),
            ("Maximum Value (max)", "{:,}".format(round(self.max[data_set_index], 3)))
        )
        # Transform mode tuple into string
        print_mode = str()
        for each in self.mode[data_set_index]:
            if each == "None":
                print_mode = "None"
            else:
                print_mode = "{:,}".format(round(each, 3)) + ", "
                print_mode = print_mode[:-2]
        print_dict["Measures of Central Tendency"] = (
            ("Mean", "{:,}".format(round(self.mean[data_set_index], 3))),
            ("Median", "{:,}".format(round(self.median[data_set_index], 3))),
            ("Mode", print_mode),
            ("Range", "{:,}".format(round(self.range[data_set_index], 3)))
        )
        print_dict["Measures of Variation"] = (
            ("Variance", "{:,}".format(round(self.var[data_set_index], 3))),
            ("Standard Deviation", "{:,}".format(round(self.stdev[data_set_index], 3))),
            ("Standard Error", "{:,}".format(round(self.sterr[data_set_index], 3))),
            ("Coeff. of Variation", "{:,}".format(round(self.cv[data_set_index], 3))),
            ("Skewness", "{:,}".format(round(self.skew[data_set_index], 3)))
        )
        print_dict["Confidence Interval Statistics"] = (
            ("Confidence Level", "{:,}".format(round(self.cl, 3))),
            (f"\N{GREEK SMALL LETTER ALPHA} ({self.tail}-tailed test)", "{:,}".format(round(self.alpha, 3))),
            (f"{self.score_type}-score", "{:,}".format(round(self.score_critical[0], 3))),
            (f"Margin of Error (E)", "{:,}".format(round(self.moe[data_set_index], 3))),
            (f"CI (mean \u00B1 E)", "[{:,}".format(round(self.ci[data_set_index][0], 3)) + ", " + "{:,}]".format(round(self.ci[data_set_index][1], 3)))
        )

        # gets the maximum length of left and right columns
        L_WIDTH = 0
        R_WIDTH = 0
        TOTAL_WIDTH = 0
        DIVIDER = " : "
        for section in print_sections:
            TOTAL_WIDTH = max(len(section), TOTAL_WIDTH)
            for stat_tuple in print_dict[section]:
                L_WIDTH = max(len(stat_tuple[0]), L_WIDTH)
                R_WIDTH = max(len(stat_tuple[1]), R_WIDTH)
        TOTAL_WIDTH = max(L_WIDTH + R_WIDTH + len(DIVIDER), len(title), TOTAL_WIDTH)
        LINE_BREAK = f"|{'='*(TOTAL_WIDTH+2)}|\n"
        # create the central data in the table
        data_string = str()
        for section in print_sections:
            data_string += LINE_BREAK + f"|-{section.center(TOTAL_WIDTH, '-')}-|\n" + LINE_BREAK
            for stat_tuple in print_dict[section]:
                data_string += f"| {stat_tuple[0].center(L_WIDTH)}{DIVIDER}{stat_tuple[1].center(R_WIDTH)} |\n"
        # create the top, title, and bottom of the table
        top = f"{''.center(TOTAL_WIDTH + 4, '_')}\n"
        title = LINE_BREAK + f"| {title.center(TOTAL_WIDTH)} |\n"
        bottom = f"{''.center(TOTAL_WIDTH + 4, '-')}\n"

        return top + title + data_string + bottom


if __name__ == "__main__":
    data = (
        (1.0, 2, 3)
      , (4, 5.0, 6)
    )
    dsObject = StatBasket(data)
    print(dsObject.n)



# def p_value(z_score: float, tail: str = "two") -> float:
#     """Returns the cumulative normal distribution at a z of z_score, two-tailed
#     by default.
#
#     :param float z_score: Z-score lookup value used in the table, from -inf to +inf
#     :param str tail: Whether the test is "left" tailed, "right" tailed, or "two"-tailed (default)
#     """
#     # Data validation
#     assert isinstance(z_score, float) or isinstance(z_score, int), \
#         "z_score must be of type 'float' or 'int'"
#     assert tail in ("left", "right", "two"), \
#         "Acceptable tail values: 'left', 'right', 'two'"
#
#     # Scores less than -3.49 have approx. cumulative area = 0.0001
#     # Scores greater than 3.49 are approx. cumulative area = 0.9999
#     z_score = round(z_score, 2)
#
#     if z_score < -3.49:
#         if tail == "right":
#             return 0.9999
#         else:
#             return 0.0001
#     elif z_score > 3.49:
#         if tail == "left":
#             return 0.9999
#         else:
#             return 0.0001
#
#     # For negative scores, subtract the area represented by the absolute
#     # value of the negative score from 1
#     # print(f"z_score = {z_score}")
#     cumulative_left_area = 0.0
#     return_p_value = 0.0
#     if z_score < 0:
#         # print("z_score < 0")
#         cumulative_left_area = 1 - self.z_table[abs(z_score)]
#     else:
#         # print("z_score > 0")
#         cumulative_left_area = self.z_table[abs(z_score)]
#     # print(f"cla = {cumulative_left_area}")
#     if tail == "two":
#         # print("tail = 'two'")
#         if cumulative_left_area > 0.5:
#             cumulative_left_area = round(1 - cumulative_left_area, 4)
#         if cumulative_left_area == 0.0001:
#             return_p_value = cumulative_left_area
#         else:
#             return_p_value = 2 * cumulative_left_area
#     elif tail == "right":
#         # print("tail = 'right'")
#         return_p_value = 1 - cumulative_left_area
#     else:
#         # print("tail = 'left'")
#         return_p_value = cumulative_left_area
#
#     return round(return_p_value, 4)
#
#
# def interpret_p_value(p_value: float, alpha: float):
#     fail_to_reject = "fail to reject the null hypothesis"
#     reject = "reject the null hypothesis"
#
#     if p_value >= alpha:
#         return fail_to_reject
#     else:
#         return reject

# def verbose_explanation(score_type, cl, tail, alpha, score, p_value, interpretation) -> str:
#     tail_dict = {"left": "<", "right": ">", "two": "!="}
#     equal_dict = {"left": ">=", "right": "<=", "two": "="}
#     p_value_with_comparator = f"<{p_value}" if p_value == 0.0001 else p_value
#     return f"The resulting {'z' if 'z' in score_type else 't'}-score for this hypothesis test " \
#            f"is {round(score, 3)}, which provides a p-value of {p_value_with_comparator}. " \
#            f"If we compare this p-value to our alpha (cl={cl}, tail={tail}, " \
#            f"\N{GREEK SMALL LETTER ALPHA}{'/2' if tail == 'two' else ''}={alpha}), " \
#            f"we can see that {p_value} " \
#            f"{'>=' if p_value >= alpha else '<'} {alpha}. Therefore, we " \
#            f"{interpretation} (h0: \N{GREEK SMALL LETTER MU} {equal_dict[tail]} {h0_mu}) " \
#            f"in favor of the alternative hypothesis (h1: \N{GREEK SMALL LETTER MU} {tail_dict[tail]} {h0_mu})"
