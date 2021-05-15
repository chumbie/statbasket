"""
ctDescStats.py

Contains the StatBasket class, which accepts a list or tuple 
containing data and calculates a 'basket' of useful statistics
describing that data. See the class documentation for more
details.

Classes:
    StatBasket
"""
# Standard Library Imports
import sys

# Local Imports
sys.path.append("..")  # so path can see the project
from src.statMethods import StatMe as sm


class StatBasket:
    """
    Class which provides simple statistics for a supplied tuple
    dataset.

    Summary:
    __________
    This class is used in conjunction with statMethods.py to statically
    create descriptive and testing statistics for one or two datasets.
    This class is useful for creating a quick comparison between two
    data sets, or if consistently re-using the statistics for a large
    set of data.

    For a description of the data set(s), use the describe() method:
    >>> my_data = (1, 2, 3, 4, 5)
    >>> basket = StatBasket(my_data)
    >>> basket.describe()
    (Note: statistics in this display table are rounded to 5 decimal
    places.

    Usage:
    ___________
    StatBasket(data: tuple [, is_population: False [, data_name: str]]

    Parameters:
    ___________
    *data : tuple*
        Single numeric data tuple
    *data2 : tuple, optional*
        Optional, default empty tuple, single numeric data tuple, for
        comparison or hypothesis testing.
    *is_population : bool, optional*
        Default False, indicates whether data is a sample (False) or
        a population, i.e. population variance is known (True).
    *cl : float, optional*
        Default 0.95, confidence level for critical score
        calculation. Valid inputs are 0.90, 0.95, or 0.99
    *tail : str, optional*
        Default "two", indicates what type of tail in hypothesis
        testing, accepted values are "two", "left", or "right",
        for two-tailed, left-tailed, or right-tailed hypothesis
        testing, respectively.
    *data_name1 : str, optional*
        Default "data", name given to the data set, appears on the display.
    *data_name2 : str, optional*
        Default "data", name given to the data set, appears on the display.

    Attributes:
    __________
    When multiple datasets are used (data2 is not empty), attributes are
    subcategorized by number.
    >>> data_x = (1, 2, 3)
    >>> data_y = (6, 7, 8, 9)
    >>> sbObj = StatBasket(data_x, data_y)
    >>> print(f"n_data_x = {sbObj.n_x}, n_data_y = {sbObj.n_y})
    >>> 'n_data_x = 3, n_data_y = 4'

    data : tuple
        Single numeric data tuple
    data2 : tuple, optional
        Optional, default empty tuple, single numeric data tuple, for
        comparison or hypothesis testing.
    is_population : bool, optional
        Default False, indicates whether data is a sample (False) or
        a population, i.e. population variance is known (True).
    cl : float, optional
        Default 0.95, confidence level for critical score
        calculation. Valid inputs are 0.90, 0.95, or 0.99
    tail : str, optional
        Default "two", indicates what type of tail in hypothesis
        testing, accepted values are "two", "left", or "right",
        for two-tailed, left-tailed, or right-tailed hypothesis
        testing, respectively.
    data_name1 : str, optional
        Default "data", name given to the data set, appears in describe().
    data_name2 : str, optional*
        Default "data", name given to the data set, appears in describe().
    n, n1, n2 : float
        Sample size of datasets, ie. len(data).
    min, min1, min2 : float
        The smallest value in the data set, i.e. min(data)
    max, max1, max2 : float
        The largest value in the data set, i.e. max(data)
    range, range1, range2 : float
        The range of the data, i.e. max - min
    mean, mean1, mean2 : float
        The average value in the data set, i.e. sigma^nvi(xi)/n
    median, median1, median2 : float
        The middlemost value in the data set.
    mode, mode1, mode2 : tuple
        The value with the most repetitions in the data set. Can be either
        zero, one, two, or three modes. Zero or >3 modes results in "N/A".
    var, var1, var2 : float
        The variance of the data, i.e. sigma^nvi((x-mean)^2)/n
    stdev, stdev1, stdev2 : float
        The standard deviation (s) of the data set, i.e. sqrt(variance)
    sterr, sterr1, sterr2 : float
        The standard error of the data set, i.e. stdev/sqrt(n)
    cv, cv1, cv2 : float
        The coefficient of variation of the data set, i.e. stdev/mean
    skew, skew1, skew2 : float
        The skewness of the dataset from negative to positive infinity, i.e.
        sigma^nvi((xi - mean)^3)/((n-1)(sigma)^3)
    """

    def __init__(self, first_data_set: tuple, second_data_set: tuple = None, is_population=False,
                 samples_dependent=False, cl=0.95, tail="two",
                 data_name: str = None, second_data_name: str = None):
        """
        Parameters
        __________
        *data_x : tuple*
            Single numeric data tuple
        *data_y : tuple, optional*
            Optional, single numeric data tuple, for comparison or
            hypothesis testing
        *is_population : bool, optional*
            Default False, indicates whether data is a sample (False) or
            a population, i.e. population variance is known (True).
        *cl : float, optional*
            Default 0.95, confidence level for critical score
            calculation. Valid inputs are 0.90, 0.95, or 0.99
        *tail : str, optional*
            Default "two", indicates what type of tail in hypothesis
            testing, accepted values are "two", "left", or "right",
            for two-tailed, left-tailed, or right-tailed hypothesis
            testing, respectively.
        *data_name : str, optional*
            Default "data", name given to the first data set, appears on the display.
        *data_y_name : str, optional*
            Default "data", name given to the second data set, appears on the display.
        """

        # Data Validation #############################################

        def data_validation():
            # Validate data in tuple form
            if not isinstance(first_data_set, tuple):
                raise ValueError(
                       f"Data is of type '{type(first_data_set).__name__}'. "
                       f"Acceptable types: 'tuple'")

            # Validate, only int or float data in data tuples
            data_type_error_list = []
            error_help = str()
            for i in range(len(first_data_set)):
                if isinstance(first_data_set[i], tuple):
                    error_help = f"data_index, value_index, value"
                    for j in range(len(first_data_set[i])):
                        if not isinstance(first_data_set[i][j], (int, float)):
                            data_type_error_list.append((i, j, first_data_set[i][j]))
                elif not isinstance(first_data_set[i], (int, float)):
                    error_help = f"value_index, value"
                    data_type_error_list.append((i, first_data_set[i]))
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
            if type(data_name) not in (type(str()), type(None)):
                wrong_name = data_name
            if type(second_data_name) not in (type(str()), type(None)):
                wrong_name = data_name
            if wrong_name != '':
                raise ValueError(f"data_name {str(wrong_name)} is not a string.")

        data_validation()

        # Check Number of Sets, Dependence ############################

        # Set default names if not supplied ##
        default_name = "data"
        default_name_x = "data_x"
        default_name_y = "data_y"
        default_name_diff = "data_diff"

        data_y_empty = True if second_data_set is None else False

        if data_y_empty:
            self.data_y_empty = True
            if data_name is None:
                # No data_y, no name given, set to default
                self.data_name = default_name
            else:
                # Set to user-supplied name
                self.data_name = data_name
        else:
            self.data_y_empty = False
            if samples_dependent:
                self.dep = True
                self.data_name = default_name_diff
            else:
                self.dep = False
                if data_name is None:
                    # Yes data_y, no name given, set to default
                    self.data_x_name = default_name_x
                else:
                    # Set to user-supplied name
                    self.data_x_name = data_name

                if second_data_name is None:
                    # No name for data_y, default
                    self.data_y_name = default_name_y
                else:
                    self.data_y_name = second_data_name

        # Primary Attributes ##########################################

        if data_y_empty:
            self.data = first_data_set
        elif samples_dependent:
            self.data = sm.get_data_diff(first_data_set, second_data_set)
            self.dep = True
        else:
            self.data_x = first_data_set
        self.data_y = second_data_set
        self.is_population = is_population
        self.samples_dependent = samples_dependent
        self.dep = self.samples_dependent  # shorter name
        self.cl = cl
        self.tail = tail

        # Calculated Attributes #######################################

        # if samples dependent, data = difference (i.e. data_x - data_y)
        if data_y_empty or samples_dependent:
            # Stats for single data set
            self.ci = sm.get_ci(
                self.data, self.cl, self.is_population, self.tail
            )
            self.cv = sm.get_cv(self.data)
            self.df = sm.get_df(self.data)
            self.max = sm.get_max(self.data)
            self.mean = sm.get_mean(self.data)
            self.median = sm.get_median(self.data)
            self.min = sm.get_min(self.data)
            self.mode = sm.get_mode(self.data)
            self.moe = sm.get_moe(
                self.data,
                cl=self.cl,
                pop_var_known=self.is_population,
                tail=self.tail
            )
            self.n = sm.get_n(self.data)
            self.range = sm.get_range(self.data)
            self.score_critical = sm.get_score_critical(
                self.data,
                cl=self.cl,
                pop_var_known=self.is_population,
                tail=self.tail
            )
            self.skew = sm.get_skew(self.data)
            self.stdev = sm.get_stdev(self.data)
            self.sterr = sm.get_sterr(self.data)
            self.var = sm.get_var(self.data, self.is_population)

        else:
            # Two data stats
            # First Data set
            self.ci_x = sm.get_ci(
                self.data_x,
                cl=self.cl,
                pop_var_known=self.is_population,
                tail=self.tail
            )
            self.cv_x = sm.get_cv(self.data_x)
            self.df_x = sm.get_df(self.data_x)
            self.max_x = sm.get_max(self.data_x)
            self.mean_x = sm.get_mean(self.data_x)
            self.median_x = sm.get_median(self.data_x)
            self.min_x = sm.get_min(self.data_x)
            self.mode_x = sm.get_mode(self.data_x)
            self.moe_x = sm.get_moe(
                self.data_x,
                cl=self.cl,
                pop_var_known=self.is_population,
                tail=self.tail
            )
            self.n_x = sm.get_n(self.data_x)
            self.range_x = sm.get_range(self.data_x)
            self.score_critical_x = sm.get_score_critical(
                self.data_x,
                cl=self.cl,
                pop_var_known=self.is_population,
                tail=self.tail
            )
            self.skew_x = sm.get_skew(self.data_x)
            self.stdev_x = sm.get_stdev(self.data_x)
            self.sterr_x = sm.get_sterr(self.data_x)
            self.var_x = sm.get_var(self.data_x, self.is_population)

            # Second Data Set
            self.ci_y = sm.get_ci(
                self.data_y,
                cl=self.cl,
                pop_var_known=self.is_population,
                tail=self.tail
            )
            self.cv_y = sm.get_cv(self.data_y)
            self.df_y = sm.get_df(self.data_y)
            self.max_y = sm.get_max(self.data_y)
            self.mean_y = sm.get_mean(self.data_y)
            self.median_y = sm.get_median(self.data_y)
            self.min_y = sm.get_min(self.data_y)
            self.mode_y = sm.get_mode(self.data_y)
            self.moe_y = sm.get_moe(
                self.data_y,
                cl=self.cl,
                pop_var_known=self.is_population,
                tail=self.tail
            )
            self.n_y = sm.get_n(self.data_y)
            self.range_y = sm.get_range(self.data_y)
            self.score_critical_y = sm.get_score_critical(
                self.data_y,
                cl=self.cl,
                pop_var_known=self.is_population,
                tail=self.tail
            )
            self.skew_y = sm.get_skew(self.data_y)
            self.stdev_y = sm.get_stdev(self.data_y)
            self.sterr_y = sm.get_sterr(self.data_y)
            self.var_y = sm.get_var(self.data_y, self.is_population)

            # Pooled Variation
            self.var_pool = sm.get_var_pool(self.data_x, self.data_y)

    def calculate_test_score(self, h0=0):
        test_data = tuple()
        test_data2 = None
        if self.data_y_empty or self.dep:
            test_data = self.data
        else:
            test_data = self.data_x
            test_data2 = self.data_y
        return sm.get_score_hyp(
            data1=test_data, data2=test_data2, h0=h0,
            samples_dependent=self.dep,
            pop_var_known=self.is_population)

    def __repr__(self):
        return (
            f"a StatBasket object, "
            f"data = ({self.data_name if self.data_y_empty else self.data_x_name}"
            f"{'EMPTY' if self.data_y_empty else ', ' + self.data_y_name})"
        )

    def describe(self) -> str:
        """Return a string table containing statistics about the supplied data."""
        # n_type = str()
        # n_letter = str()
        return "This message indicates that .describe() is currently under construction. Sorry about that."
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
        name_list = [self.data_x_name]
        if self.data_y_empty is not True:
            name_list.append(self.data_y_name)
        title = f"DESCRIPTION OF {'DATA' if self.data_x_name == 'data' else self.data_x_name}"
        print_dict = dict()
        # # Key = section: (Subkey = stat name, Value: stat value)
        # print_dict[f"General {n_type} Statistics"] = (
        #     (f"Size of {n_type} ({n_letter})", "{:,}".format(round(self.n, 3))),
        #     ("Minimum Value (min)", "{:,}".format(round(self.min, 3))),
        #     ("Maximum Value (max)", "{:,}".format(round(self.max, 3)))
        # )
        # # Transform mode tuple into string
        # print_mode = str()
        # for each in self.mode[data_set_index]:
        #     if each == "None":
        #         print_mode = "None"
        #     else:
        #         print_mode = "{:,}".format(round(each, 3)) + ", "
        #         print_mode = print_mode[:-2]
        # print_dict["Measures of Central Tendency"] = (
        #     ("Mean", "{:,}".format(round(self.mean[data_set_index], 3))),
        #     ("Median", "{:,}".format(round(self.median[data_set_index], 3))),
        #     ("Mode", print_mode),
        #     ("Range", "{:,}".format(round(self.range[data_set_index], 3)))
        # )
        # print_dict["Measures of Variation"] = (
        #     ("Variance", "{:,}".format(round(self.var[data_set_index], 3))),
        #     ("Standard Deviation", "{:,}".format(round(self.stdev[data_set_index], 3))),
        #     ("Standard Error", "{:,}".format(round(self.sterr[data_set_index], 3))),
        #     ("Coeff. of Variation", "{:,}".format(round(self.cv[data_set_index], 3))),
        #     ("Skewness", "{:,}".format(round(self.skew[data_set_index], 3)))
        # )
        # print_dict["Confidence Interval Statistics"] = (
        #     ("Confidence Level", "{:,}".format(round(self.cl, 3))),
        #     (f"\N{GREEK SMALL LETTER ALPHA} ({self.tail}-tailed test)", "{:,}".format(round(self.alpha, 3))),
        #     (f"{self.score_type}-score", "{:,}".format(round(self.score_critical[0], 3))),
        #     (f"Margin of Error (E)", "{:,}".format(round(self.moe[data_set_index], 3))),
        #     (f"CI (mean \u00B1 E)", "[{:,}".format(round(self.ci[data_set_index][0], 3)) + ", " + "{:,}]".format(round(self.ci[data_set_index][1], 3)))
        # )
        #
        # # gets the maximum length of left and right columns
        # L_WIDTH = 0
        # R_WIDTH = 0
        # TOTAL_WIDTH = 0
        # DIVIDER = " : "
        # for section in print_sections:
        #     TOTAL_WIDTH = max(len(section), TOTAL_WIDTH)
        #     for stat_tuple in print_dict[section]:
        #         L_WIDTH = max(len(stat_tuple[0]), L_WIDTH)
        #         R_WIDTH = max(len(stat_tuple[1]), R_WIDTH)
        # TOTAL_WIDTH = max(L_WIDTH + R_WIDTH + len(DIVIDER), len(title), TOTAL_WIDTH)
        # LINE_BREAK = f"|{'='*(TOTAL_WIDTH+2)}|\n"
        # # create the central data in the table
        # data_string = str()
        # for section in print_sections:
        #     data_string += LINE_BREAK + f"|-{section.center(TOTAL_WIDTH, '-')}-|\n" + LINE_BREAK
        #     for stat_tuple in print_dict[section]:
        #         data_string += f"| {stat_tuple[0].center(L_WIDTH)}{DIVIDER}{stat_tuple[1].center(R_WIDTH)} |\n"
        # # create the top, title, and bottom of the table
        # top = f"{''.center(TOTAL_WIDTH + 4, '_')}\n"
        # title = LINE_BREAK + f"| {title.center(TOTAL_WIDTH)} |\n"
        # bottom = f"{''.center(TOTAL_WIDTH + 4, '-')}\n"
        #
        # return (
        #         top
        #         + title
        #         + data_string
        #         + bottom
        # )


if __name__ == "__main__":
    data = (1, 2, 3)
    print(StatBasket(data).mean)
