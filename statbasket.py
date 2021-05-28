"""
ctDescStats.py

Contains the StatBasket class, which accepts a list or tuple 
containing data and calculates a 'basket' of useful statistics
describing that data. See class documentation for more
details.

Classes:
    StatBasket
"""
# Standard Library Imports
import sys

# Local Imports
sys.path.append("..")  # so path can see the project
from statmethods import StatMe as sm


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
<<<<<<< HEAD:statbasket/statbasket.py
    >>> basket = StatBasket(my_data)
=======
    
    >>> basket = StatBasket(my_data)
    
>>>>>>> 9b139656718d8deddbe47c473991cd01b6ca7ef4:statbasket/statBasket.py
    >>> basket.describe()

    Parameters:
    ___________
    first_data_set : tuple
        Single numeric data tuple
    second_data_set : tuple, optional
        Optional, default empty tuple, single numeric data tuple, for
        comparison or hypothesis testing.
    is_population : bool, optional
        Default False, indicates whether data is a sample (False) or
        a population, i.e. population variance is known (True).
    samples_dependent: bool, optional
        Default False, indicates whether the datasets are dependent.
    cl : float, optional
        Default 0.95, confidence level for critical score
        calculation. Valid inputs are 0.90, 0.95, or 0.99
    tail : str, optional
        Default "two", indicates what type of tail in hypothesis
        testing, accepted values are "two", "left", or "right",
        for two-tailed, left-tailed, or right-tailed hypothesis
        testing, respectively.
    first_data_name : str, optional
        Name given to the data set, appears on the describe() method.
    second_data_name : str, optional
        Name given to the data set, appears when using describe() method.

    Attributes:
    __________
    When multiple datasets are used (second_data_set is not None), attributes are
<<<<<<< HEAD:statbasket/statbasket.py
    sub-categorized by suffix.
=======
    subcategorized by number.
>>>>>>> 9b139656718d8deddbe47c473991cd01b6ca7ef4:statbasket/statBasket.py
    
    >>> data_x, data_y = (1, 2, 3), (6, 7, 8, 9)
    >>> sbObj = StatBasket(data_x, data_y)
    >>> print(n_data_x, ', ', n_data_y)
    '3, 4'

    If samples_dependent=True, attributes are saved with '_diff' suffix.

    >>> data_x, data_y = (1, 2, 3), (4, 5, 6)
    >>> sbObj = StatBasket(data_x, data_y, samples_dependent=True)
    >>> print(sbObj.mean_diff)
    -3.0

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
    data_name : str, optional
        Name given to the data set, appears in describe().
    n : float
        Sample size of datasets, ie. len(data).
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
<<<<<<< HEAD:statbasket/statbasket.py
    quartiles : tuple
        Tuple of quartile information, i.e. (Q1, Q2, Q3, IQR)
=======
>>>>>>> 9b139656718d8deddbe47c473991cd01b6ca7ef4:statbasket/statBasket.py
    mode : tuple
        The value with the most repetitions in the data set. Can be either
        zero, one, two, or three modes. Zero or >3 modes results in "N/A".
    var : float
        The variance of the data, i.e. sigma^nvi((x-mean)^2)/n
    stdev : float
        The standard deviation (s) of the data set, i.e. sqrt(variance)
    sterr : float
        The standard error of the data set, i.e. stdev/sqrt(n)
    cv : float
        The coefficient of variation of the data set, i.e. stdev/mean
    skew : float
        The skewness of the dataset from negative to positive infinity, i.e.
        sigma^nvi((xi - mean)^3)/((n-1)(sigma)^3)
    score_critical : float
        The critical z- or t-score used for confidence interval calculation
    alpha : float
        The alpha of the dataset, used for critical score calculation
    score_critical_type : str
        Whether the critical score is a 'z' or 't' score

    Methods:
    _____________
    calculate_test_score
        Return the hypothesis test score for the dataset(s)
    describe
        Creates a printout of statistics describing the data
    """

    def __init__(self, first_data_set: tuple or list,
                 second_data_set: tuple or list = None,
                 remove_outliers=False,
                 is_population=False,
                 samples_dependent=False,
                 cl=0.95,
                 tail="two",
                 first_data_name: str = None,
                 second_data_name: str = None):
        """
        Parameters
        __________
        *first_data_set : tuple or list*
            One dimensional data set
        *second_data_set: tuple or list, optional*
            Optional, one-dimensional data set, for comparison to first
            data set, or hypothesis testing
        *remove_outliers: bool, optional
            Default False, if True identifies and removes outliers from
            calculations
        *is_population : bool, optional*
            Default False, indicates whether data is a sample (False) or
            a population, i.e. population variance is known (True).
        *cl : float, optional*
            Default 0.95, confidence level for critical score
            calculation. Valid inputs are 0.90, 0.95, or 0.99 only
        *tail : str, optional*
            Default "two", indicates the 'tailed-ness' of the confidence
            level or hypothesis test. Acceptable values are "two",
            "left", or "right", for two-tailed, left-tailed, or
            right-tailed hypothesis testing, respectively.
        *first_data_name: str, optional*
            Default "data", name given to the first data set, appears
            when the describe() method is called.
        *second_data_name: str, optional*
            Default "data", name given to the second data set, appears
            when the describe() method is called.
        """

        # Data Validation and Primary Attributes ######################

        def data_validation():
            """Raises error if data types are incorrect, or other problems"""
            # Validate data in tuple form
            if not isinstance(first_data_set, (tuple, list)):
                raise ValueError(
                       f"Data is of type '{type(first_data_set).__name__}'. "
                       f"Acceptable types: 'tuple', 'list'")

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
            if type(first_data_name) not in (type(str()), type(None)):
                wrong_name = first_data_name
            if type(second_data_name) not in (type(str()), type(None)):
                wrong_name = first_data_name
            if wrong_name != '':
                raise ValueError(f"data_name {str(wrong_name)} is not a string.")
            if samples_dependent:
                if isinstance(second_data_set, type(None)):
                    raise ValueError(f"'samples_dependent' is True but only one sample set provided.")
                elif len(first_data_set) != len(second_data_set):
                    raise ValueError(f"'Samples dependent' is True, but samples are not the same length.\n"
                                     f"First data set length = {len(first_data_set)}\n"
                                     f"Second data set length = {len(second_data_set)}")

        data_validation()

        # Set default names if not supplied ##
        default_name = "DATA"
        default_name_x = "DATA_X"
        default_name_y = "DATA_Y"
        default_name_diff = "DATA_DIFF"

        # Check used to determine if second data set supplied
        self.data_y_empty = True if second_data_set is None else False

        if self.data_y_empty:
            self.data_y_empty = True
            if first_data_name is None:
                # No data_y, no name given, set to default
                self.data_name = default_name
            else:
                # Set to user-supplied name
                self.data_name = first_data_name
        else:
            self.data_y_empty = False
            if samples_dependent:
                self.samples_dependent = True
                self.data_name = default_name_diff
            else:
                self.samples_dependent = False
                if first_data_name is None:
                    # Yes data_y, no name given, set to default
                    self.data_x_name = default_name_x
                else:
                    # Set to user-supplied name
                    self.data_x_name = first_data_name

                if second_data_name is None:
                    # No name for data_y, default
                    self.data_y_name = default_name_y
                else:
                    self.data_y_name = second_data_name

        # Primary Attributes ##########################################

        if remove_outliers:
            first_data_set = sm.get_outlier_data(first_data_set, remove_outliers=True)
            second_data_set = sm.get_outlier_data(second_data_set, remove_outliers=True)
        # Only one data set, standard names (no _x, _y, etc)
        if samples_dependent:
            # If dependent, _diff stats are of the difference of datasets
            self.data_diff = sm.get_data_diff(first_data_set, second_data_set)
            self.samples_dependent = True
        if self.data_y_empty:
            self.data = first_data_set
        else:
            self.data_x = first_data_set
            self.data_y = second_data_set
        self.is_population = is_population
        self.samples_dependent = samples_dependent
        self.cl = cl
        self.tail = tail

        # Calculated Attributes #######################################

        def get_calculated_attributes(self, suffix=str()) -> None:
            """Execute calculated attributes declarations with suffix.

            suffix : str, optional
                Default '', determines the suffix of each attribute

            #>>> get_calculated_attributes(suffix='x')

            Output: exec(self.n_x = sm.get_n(self.data_x))"""

            if suffix is not str():
                suffix = "_" + suffix
            exec(f"""self.ci{suffix} = sm.get_ci(self.data{suffix},
            cl=self.cl, is_population=self.is_population, tail=self.tail)""")
            exec(f"""self.cv{suffix} = sm.get_cv(self.data{suffix}, is_population=self.is_population)""")
            exec(f"""self.df{suffix} = sm.get_df(self.data{suffix})""")
            exec(f"""self.max{suffix} = sm.get_max(self.data{suffix})""")
            exec(f"""self.mean{suffix} = sm.get_mean(self.data{suffix})""")
            exec(f"""self.median{suffix} = sm.get_median(self.data{suffix})""")
            exec(f"""self.min{suffix} = sm.get_min(self.data{suffix})""")
            exec(f"""self.mode{suffix} = sm.get_mode(self.data{suffix})""")
            exec(f"""self.moe{suffix} = sm.get_moe(self.data{suffix},
            cl=self.cl, is_population=self.is_population, tail=self.tail)""")
            exec(f"""self.n{suffix} = sm.get_n(self.data{suffix})""")
            exec(f"""self.range{suffix} = sm.get_range(self.data{suffix})""")
            exec(f"""type, alpha, score = sm.get_score_critical(self.data{suffix},
            cl=self.cl, is_population=self.is_population, tail=self.tail,verbose=True)""")
            exec(f"""self.score_critical_type{suffix} = type""")
            exec(f"""self.alpha{suffix} = alpha""")
            exec(f"""self.score_critical{suffix} = score """)
            exec(f"""self.skew{suffix} = sm.get_skew(self.data{suffix}, is_population=self.is_population)""")
            exec(f"""self.stdev{suffix} = sm.get_stdev(self.data{suffix}, is_population=self.is_population)""")
            exec(f"""self.sterr{suffix} = sm.get_sterr(self.data{suffix}, is_population=self.is_population)""")
            exec(f"""self.var{suffix} = sm.get_var(self.data{suffix}, is_population=self.is_population)""")
            exec(f"""self.quartiles{suffix} = sm.get_quartile_data(self.data{suffix})""")

        # if samples dependent, data = difference (i.e. data_x - data_y)
        if samples_dependent:
            get_calculated_attributes(self, 'diff')
        if self.data_y_empty:
            get_calculated_attributes(self)
        else:
            get_calculated_attributes(self, 'x')
            get_calculated_attributes(self, 'y')
            self.var_pool = sm.get_var_pool(self.data_x, self.data_y)

    def calculate_test_score(self, h0: float = 0.0, verbose=False):
        """Return the hypothesis test score for the dataset(s)"""
        test_data = tuple()
        test_data2 = None
        if self.samples_dependent:
            test_data = self.data_diff
        elif self.data_y_empty:
            test_data = self.data
        else:
            test_data = self.data_x
            test_data2 = self.data_y
        return sm.get_score_hyp(
            data1=test_data, data2=test_data2, h0=h0,
            samples_dependent=self.samples_dependent,
            is_population=self.is_population,
            verbose=verbose)

    def describe(self, round_places=3, h0=None):
        """
        Return a string table containing statistics about the supplied data

        Data is rounded to round_places number of decimal places

        If h0 is supplied, returns hypothesis test data as well
        """

        # Initializes the title of the return table
        title = str()
        if self.samples_dependent:
            title = "DATA DIFFERENCE"
        elif self.data_y_empty:
            title = self.data_name
        else:
            title = f"{self.data_x_name} and {self.data_y_name}"
        title = f"DESCRIPTION OF {title}"

        # Set whether data is pop or sample data, names used for labels
        n_type = str()
        n_letter = str()
        if self.is_population:
            n_type = "Population"
            n_letter = "N"
        else:
            n_type = "Sample"
            n_letter = "n"

        print_sections = [
            f"General {n_type} Statistics",
            f"Measures of Central Tendency",
            f"Measures of Variation",
            f"Confidence Interval Statistics"
        ]
        if h0 is not None:
            print_sections.append(f"Hypothesis Test Results")

        def create_data_dict(print_sections: list,
                             round_places: int,
                             n_type: str,
                             n_letter: str,
                             h0: float = None,
                             data_suffix: str = str()) -> dict:
            """
            Return a dictionary containing section data

            If two independent datasets, returns two values for
            every subkey (data_x and data_y)
            """
            def create_single_dict(print_sections: list,
                             round_places: int,
                             n_type: str,
                             n_letter: str,
                             h0: float = None,
                             data_suffix: str = str()) -> dict:
                # Key = section: (Subkey = stat name, Value: stat value)
                return_data_dict = dict()

                # Sets the values to their appropriate attributes based on type of data:
                # data, data_x, data_y, or data_diff
                if data_suffix is not str():
                    data_suffix = "_" + data_suffix

                exec(f"""return_data_dict['General {n_type} Statistics'] = (
                    ('Size of {n_type} ({n_letter})', "{{:,}}".format(round(self.n{data_suffix}, round_places))),
                    ('Minimum Value (min)', "{{:,}}".format(round(self.min{data_suffix}, round_places))),
                    ('Maximum Value (max)', "{{:,}}".format(round(self.max{data_suffix}, round_places))))""")

                exec(f"""return_data_dict['Measures of Central Tendency'] = (
                    ('Mean', "{{:,}}".format(round(self.mean{data_suffix}, round_places))),
                    ('Median', "{{:,}}".format(round(self.median{data_suffix}, round_places))),
                    ('Mode', self.mode{data_suffix} if isinstance(self.mode{data_suffix}, str) else "{{:,}}".format(round(self.mode{data_suffix}, round_places))),
                    ('Range', "{{:,}}".format(round(self.range{data_suffix}, round_places))),
                    ('Skewness', "{{:,}}".format(round(self.skew{data_suffix}, round_places))))""")

                exec(f"""return_data_dict['Measures of Variation'] = (
                    ('Variance', "{{:,}}".format(round(self.var{data_suffix}, round_places))),
                    ('Standard Deviation', "{{:,}}".format(round(self.stdev{data_suffix}, round_places))),
                    ('Standard Error', "{{:,}}".format(round(self.sterr{data_suffix}, round_places))),
                    ('Coeff. of Variation', "{{:,}}".format(round(self.cv{data_suffix}, round_places))))""")

                exec(f"""return_data_dict['Confidence Interval Statistics'] = (
                    ('Confidence Level', '{{:,}}'.format(round(self.cl, round_places))),
                    (f'\N{GREEK SMALL LETTER ALPHA} ({self.tail}-tailed)', '{{:,}}'.format(round(self.alpha{data_suffix}, round_places))),
                    (f'{{self.score_critical_type{data_suffix}}}-score', '{{:,}}'.format(round(self.score_critical{data_suffix}, round_places))),
                    (f'Margin of Error (E)', '{{:,}}'.format(round(self.moe{data_suffix}, round_places))),
                    (f'CI (mean \u00B1 E)',
                     '[{{:,}}'.format(round(self.ci{data_suffix}[0], round_places)) + ', ' + '{{:,}}]'.format(round(self.ci{data_suffix}[1], round_places))))""")

                if h0 is not None:
                    # Get appropriate operators, based on h0 and tail of test
                    h0_op = '='
                    h1_op = '\u2260'
                    if self.tail == 'left':
                        h0_op = '\u2265'
                        h1_op = '<'
                    elif self.tail == 'right':
                        h0_op = '\u2265'
                        h1_op = '>'

                    mu_type = (f"\N{GREEK SMALL LETTER MU}x "
                               f"- \N{GREEK SMALL LETTER MU}y")
                    if self.data_y_empty:
                        mu_type = f"\N{GREEK SMALL LETTER MU}"

                    exec(f"""score, score_type, test_type = """
                         + f"""self.calculate_test_score(h0=h0, verbose=True)""")
                    exec(f"""return_data_dict['Hypothesis Test Results'] = (
                        ('Test Type', test_type),
                        ('Null Hypothesis', 'h0: {mu_type} {h0_op} {h0}'),
                        ('Alternative Hypothesis', 'h1: {mu_type} {h1_op} {h0}'),
                        (f'Score Type', score_type),
                        (f'Score', '{{:.3f}}'.format(score)))""")
                return return_data_dict

            # Return different dict depending on type of data provided
            data_dict = dict()
            data_dict_x = dict()
            data_dict_y = dict()
            if self.data_y_empty:
                data_dict = create_single_dict(
                    print_sections, round_places, n_type, n_letter, h0
                )
            elif self.samples_dependent:
                data_dict = create_single_dict(
                    print_sections, round_places, n_type, n_letter, h0, data_suffix="diff"
                )
            else:
                data_dict_x = create_single_dict(
                    print_sections, round_places, n_type, n_letter, h0, data_suffix="x"
                )
                data_dict_y = create_single_dict(
                    print_sections, round_places, n_type, n_letter, h0, data_suffix="y"
                )

                # Combine the two dictionaries into one
                for section in print_sections:
                    temp_list = list()
                    # Iterate over each stat per section
                    for i in range(len(data_dict_x[section])):
                        stat_name = data_dict_x[section][i][0]
                        x_value = data_dict_x[section][i][1]
                        y_value = data_dict_y[section][i][1]
                        temp_list.append((stat_name, x_value, y_value))
                    data_dict[section] = tuple(temp_list)
            return data_dict

        data_dict = create_data_dict(print_sections, round_places, n_type, n_letter, h0)
        # Check, if two independent samples, pop var unknown
        stat_divider = "  "
        sample_divider = "  "
        is_two_ind = True
        if self.samples_dependent or self.data_y_empty:
            is_two_ind = False
            sample_divider = ''

        def get_column_widths():
            """Return tuple of l_width, r_width, r_width_mult, and total_width"""
            l_width = 0
            r_width = 0
            r_width_mult = 2 if is_two_ind else 1
            total_width = 0

            for section in print_sections:
                total_width = max(len(section), total_width)
                for stat_tuple in data_dict[section]:
                    l_width = max(len(stat_tuple[0]), l_width)
                    r_width = max(len(stat_tuple[1]), r_width)
                    if is_two_ind:
                        r_width = max(len(stat_tuple[2]), r_width)
            total_width = max(
                l_width + (r_width * r_width_mult) + len(stat_divider) + len(sample_divider),
                len(title),
                total_width
            )
            return l_width, r_width, r_width_mult, total_width

        l_width, r_width, r_width_mult, total_width = get_column_widths()

        def get_line_break(filler: str) -> str:
            return f"|{filler*(total_width+2)}|\n"
        line_break = get_line_break("=")

        def create_central_data_table():
            data_string = str()
            for section in print_sections:
                # Since hyp testing is single, special rules if hypothesis section
                hyp_sec = True if section == 'Hypothesis Test Results' else False
                # r_length is adjusted to account for sample divider in other sections
                sample_adjust = len(sample_divider) if hyp_sec else 0

                # Begin
                data_string += line_break + f"|-{section.center(total_width, '-')}-|\n" + line_break
                for stat_tuple in data_dict[section]:
                    two_data_and_not_hyp = True if not hyp_sec and is_two_ind else False
                    hyp_mult = 2 if hyp_sec and is_two_ind else 1
                    data_string += (f"| {stat_tuple[0].center(l_width)}"
                                    f"{stat_divider}"
                                    f"{stat_tuple[1].center(r_width * hyp_mult + sample_adjust)}"
                                    f"{sample_divider + stat_tuple[2].center(r_width) if two_data_and_not_hyp else ''} |\n")
            return data_string

        # create the top, title, data_middle, and bottom of the table
        top = f"{''.center(total_width + 4, '_')}\n"
        title = line_break + f"| {title.center(total_width)} |\n"
        data_middle = create_central_data_table()
        bottom = f"{''.center(total_width + 4, '-')}\n"

        return (
                top
                + title
                + data_middle
                + bottom
        )

    def __repr__(self):
        return (
            f"a StatBasket object, "
            f"data = ({self.data_name if self.data_y_empty else self.data_x_name}"
            f"{'EMPTY' if self.data_y_empty else ', ' + self.data_y_name})"
        )


if __name__ == "__main__":
    pass
    data1 = (1, 2, 3, 4, 4, 5, 6, 10)
    # data2 = (-1.0, -2.0, -3.0, -4.0, -4.0, -5.0, -6.0, -10.0)
    sbObj = StatBasket(data1)
    print(sbObj.quartiles)
