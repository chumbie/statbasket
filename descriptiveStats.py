"""
ctDescStats.py

Contains the DescriptiveStats class, which accepts a list or tuple 
containing data, and outputs useful descriptive statistics derived from 
that data set. Assumes data is a sample of a population, unless 
is_population=True

Classes:
    DescriptiveStats
"""

from sys import exit as sys_exit


class DescriptiveStats:
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
    DescriptiveStats(data: tuple [, is_population: False [, data_name: str]]

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
        data_name = str()
        if self.data_name != "data":
            data_name = f" Name of data = {self.data_name}"
        return f"A DescriptiveStats object.{data_name}"
    # Score tables
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
    z_table = {
        -99: 0.0001,
        0.0: 0.5, 0.01: 0.504, 0.02: 0.508, 0.03: 0.512, 0.04: 0.516, 0.05: 0.5199, 0.06: 0.5239, 0.07: 0.5279,
        0.08: 0.5319, 0.09: 0.5359,
        0.1: 0.5398, 0.11: 0.5438, 0.12: 0.5478, 0.13: 0.5517, 0.14: 0.5557, 0.15: 0.5596, 0.16: 0.5636, 0.17: 0.5675,
        0.18: 0.5714, 0.19: 0.5753,
        0.2: 0.5793, 0.21: 0.5832, 0.22: 0.5871, 0.23: 0.591, 0.24: 0.5948, 0.25: 0.5987, 0.26: 0.6026, 0.27: 0.6064,
        0.28: 0.6103, 0.29: 0.6141,
        0.3: 0.6179, 0.31: 0.6217, 0.32: 0.6255, 0.33: 0.6293, 0.34: 0.6331, 0.35: 0.6368, 0.36: 0.6406, 0.37: 0.6443,
        0.38: 0.648, 0.39: 0.6517,
        0.4: 0.6554, 0.41: 0.6591, 0.42: 0.6628, 0.43: 0.6664, 0.44: 0.67, 0.45: 0.6736, 0.46: 0.6772, 0.47: 0.6808,
        0.48: 0.6844, 0.49: 0.6879,
        0.5: 0.6915, 0.51: 0.695, 0.52: 0.6985, 0.53: 0.7019, 0.54: 0.7054, 0.55: 0.7088, 0.56: 0.7123, 0.57: 0.7157,
        0.58: 0.719, 0.59: 0.7224,
        0.6: 0.7257, 0.61: 0.7291, 0.62: 0.7324, 0.63: 0.7357, 0.64: 0.7389, 0.65: 0.7422, 0.66: 0.7454, 0.67: 0.7486,
        0.68: 0.7517, 0.69: 0.7549,
        0.7: 0.758, 0.71: 0.7611, 0.72: 0.7642, 0.73: 0.7673, 0.74: 0.7704, 0.75: 0.7734, 0.76: 0.7764, 0.77: 0.7794,
        0.78: 0.7823, 0.79: 0.7852,
        0.8: 0.7881, 0.81: 0.791, 0.82: 0.7939, 0.83: 0.7967, 0.84: 0.7995, 0.85: 0.8023, 0.86: 0.8051, 0.87: 0.8078,
        0.88: 0.8106, 0.89: 0.8133,
        0.9: 0.8159, 0.91: 0.8186, 0.92: 0.8212, 0.93: 0.8238, 0.94: 0.8264, 0.95: 0.8289, 0.96: 0.8315, 0.97: 0.834,
        0.98: 0.8365, 0.99: 0.8389,
        1.0: 0.8413, 1.01: 0.8438, 1.02: 0.8461, 1.03: 0.8485, 1.04: 0.8508, 1.05: 0.8531, 1.06: 0.8554, 1.07: 0.8577,
        1.08: 0.8599, 1.09: 0.8621,
        1.1: 0.8643, 1.11: 0.8665, 1.12: 0.8686, 1.13: 0.8708, 1.14: 0.8729, 1.15: 0.8749, 1.16: 0.877, 1.17: 0.879,
        1.18: 0.881, 1.19: 0.883,
        1.2: 0.8849, 1.21: 0.8869, 1.22: 0.8888, 1.23: 0.8907, 1.24: 0.8925, 1.25: 0.8944, 1.26: 0.8962, 1.27: 0.898,
        1.28: 0.8997, 1.29: 0.9015,
        1.3: 0.9032, 1.31: 0.9049, 1.32: 0.9066, 1.33: 0.9082, 1.34: 0.9099, 1.35: 0.9115, 1.36: 0.9131, 1.37: 0.9147,
        1.38: 0.9162, 1.39: 0.9177,
        1.4: 0.9192, 1.41: 0.9207, 1.42: 0.9222, 1.43: 0.9236, 1.44: 0.9251, 1.45: 0.9265, 1.46: 0.9279, 1.47: 0.9292,
        1.48: 0.9306, 1.49: 0.9319,
        1.5: 0.9332, 1.51: 0.9345, 1.52: 0.9357, 1.53: 0.937, 1.54: 0.9382, 1.55: 0.9394, 1.56: 0.9406, 1.57: 0.9418,
        1.58: 0.9429, 1.59: 0.9441,
        1.6: 0.9452, 1.61: 0.9463, 1.62: 0.9474, 1.63: 0.9484, 1.64: 0.9495, 1.65: 0.9505, 1.66: 0.9515, 1.67: 0.9525,
        1.68: 0.9535, 1.69: 0.9545,
        1.7: 0.9554, 1.71: 0.9564, 1.72: 0.9573, 1.73: 0.9582, 1.74: 0.9591, 1.75: 0.9599, 1.76: 0.9608, 1.77: 0.9616,
        1.78: 0.9625, 1.79: 0.9633,
        1.8: 0.9641, 1.81: 0.9649, 1.82: 0.9656, 1.83: 0.9664, 1.84: 0.9671, 1.85: 0.9678, 1.86: 0.9686, 1.87: 0.9693,
        1.88: 0.9699, 1.89: 0.9706,
        1.9: 0.9713, 1.91: 0.9719, 1.92: 0.9726, 1.93: 0.9732, 1.94: 0.9738, 1.95: 0.9744, 1.96: 0.975, 1.97: 0.9756,
        1.98: 0.9761, 1.99: 0.9767,
        2.0: 0.9772, 2.01: 0.9778, 2.02: 0.9783, 2.03: 0.9788, 2.04: 0.9793, 2.05: 0.9798, 2.06: 0.9803, 2.07: 0.9808,
        2.08: 0.9812, 2.09: 0.9817,
        2.1: 0.9821, 2.11: 0.9826, 2.12: 0.983, 2.13: 0.9834, 2.14: 0.9838, 2.15: 0.9842, 2.16: 0.9846, 2.17: 0.985,
        2.18: 0.9854, 2.19: 0.9857,
        2.2: 0.9861, 2.21: 0.9864, 2.22: 0.9868, 2.23: 0.9871, 2.24: 0.9875, 2.25: 0.9878, 2.26: 0.9881, 2.27: 0.9884,
        2.28: 0.9887, 2.29: 0.989,
        2.3: 0.9893, 2.31: 0.9896, 2.32: 0.9898, 2.33: 0.9901, 2.34: 0.9904, 2.35: 0.9906, 2.36: 0.9909, 2.37: 0.9911,
        2.38: 0.9913, 2.39: 0.9916,
        2.4: 0.9918, 2.41: 0.992, 2.42: 0.9922, 2.43: 0.9925, 2.44: 0.9927, 2.45: 0.9929, 2.46: 0.9931, 2.47: 0.9932,
        2.48: 0.9934, 2.49: 0.9936,
        2.5: 0.9938, 2.51: 0.994, 2.52: 0.9941, 2.53: 0.9943, 2.54: 0.9945, 2.55: 0.9946, 2.56: 0.9948, 2.57: 0.9949,
        2.58: 0.9951, 2.59: 0.9952,
        2.6: 0.9953, 2.61: 0.9955, 2.62: 0.9956, 2.63: 0.9957, 2.64: 0.9959, 2.65: 0.996, 2.66: 0.9961, 2.67: 0.9962,
        2.68: 0.9963, 2.69: 0.9964,
        2.7: 0.9965, 2.71: 0.9966, 2.72: 0.9967, 2.73: 0.9968, 2.74: 0.9969, 2.75: 0.997, 2.76: 0.9971, 2.77: 0.9972,
        2.78: 0.9973, 2.79: 0.9974,
        2.8: 0.9974, 2.81: 0.9975, 2.82: 0.9976, 2.83: 0.9977, 2.84: 0.9977, 2.85: 0.9978, 2.86: 0.9979, 2.87: 0.9979,
        2.88: 0.998, 2.89: 0.9981,
        2.9: 0.9981, 2.91: 0.9982, 2.92: 0.9982, 2.93: 0.9983, 2.94: 0.9984, 2.95: 0.9984, 2.96: 0.9985, 2.97: 0.9985,
        2.98: 0.9986, 2.99: 0.9986,
        3.0: 0.9987, 3.01: 0.9987, 3.02: 0.9987, 3.03: 0.9988, 3.04: 0.9988, 3.05: 0.9989, 3.06: 0.9989, 3.07: 0.9989,
        3.08: 0.999, 3.09: 0.999,
        3.1: 0.999, 3.11: 0.9991, 3.12: 0.9991, 3.13: 0.9991, 3.14: 0.9992, 3.15: 0.9992, 3.16: 0.9992, 3.17: 0.9992,
        3.18: 0.9993, 3.19: 0.9993,
        3.2: 0.9993, 3.21: 0.9993, 3.22: 0.9994, 3.23: 0.9994, 3.24: 0.9994, 3.25: 0.9994, 3.26: 0.9994, 3.27: 0.9995,
        3.28: 0.9995, 3.29: 0.9995,
        3.3: 0.9995, 3.31: 0.9995, 3.32: 0.9995, 3.33: 0.9996, 3.34: 0.9996, 3.35: 0.9996, 3.36: 0.9996, 3.37: 0.9996,
        3.38: 0.9996, 3.39: 0.9997,
        3.4: 0.9997, 3.41: 0.9997, 3.42: 0.9997, 3.43: 0.9997, 3.44: 0.9997, 3.45: 0.9997, 3.46: 0.9997, 3.47: 0.9997,
        3.48: 0.9997, 3.49: 0.9998,
        99: 0.9999
    }

    def __init__(self,
                 data1: tuple,
                 data2=None,
                 is_population=False,
                 cl=0.95,
                 tail=None,
                 data1_name="data",
                 data2_name="data"):
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
             values are 0.90, 0.95, and 0.99 (default 0.95)
        tails : str
            Default "two", indicates what type of tail in hypothesis testing,
            accepted values are "two", "left", or "right", for two-tailed,
            left-tailed, or right-tailed hypothesis testing, respectively.
        data_name : str, optional
            Default "data", name given to the data set, appears on the display.
        """

        # #################### #
        # Primary Attributes and Validation
        # #################### #

        assert isinstance(data1, tuple or list), \
            f"Data is of type '{type(data1).__name__}'. Acceptable types: 'tuple', 'list'"
        if data2:
            assert isinstance(data2, tuple or list or None), \
                f"Data is of type '{type(data1).__name__}'. Acceptable types: 'tuple', 'list'"
        data_type_error_list = []
        for i in range(len(data1)):
            if not isinstance(data1[i], int or float):
                data_type_error_list.append((i, data1[i]))
        assert len(data_type_error_list) == 0, \
            f"One or more values in dataset are non-numeric (index, value): {data_type_error_list}"
        assert isinstance(is_population, bool), \
            f"is_population is of type '{type(is_population).__name__}', must be type 'bool' (True or False)."
        assert cl in (0.90, 0.95, 0.99), \
            f"Confidence level (cl={str(cl)}) is not 0.90, 0.95, or 0.99."
        assert tail in (None, "two", "left", "right"), \
            f"Tail attribute value (tail={str(cl)}) is not 'two', 'left', or 'right'."
        assert isinstance(data1_name, str), f"data_name {str(data1_name)} is not a string."
        if not data2:
            data2 = tuple()
        if not tail:
            tail = "two"
        self.data = data1, data2
        self.is_population = is_population
        self.cl = cl
        self.tail = tail
        self.data_name = data1_name

    # #################### #
    # Calculated Data Properties
    # #################### #

    @property
    def n(self) -> tuple:
        """Return a tuple containing the length of each dataset.
        return = (n_data1, n_data2)."""
        return_list = list()
        for each in self.data:
            if each == ():
                break
            return_list.append(len(each))
        return tuple(return_list)

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

    # #################### #
    # Measures of Central Tendency
    # #################### #

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

    # #################### #
    # Measures of Data Variation
    # #################### #

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

    # #################### #
    # Statistics Score Functions
    # #################### #

    @property
    def _score_type(self) -> tuple:
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
    def ci_score(self) -> tuple:
        """Return the score for self.score_type from the appropriate table.

        Acceptable score types:

        * "z" = z-score
        * "t" = Student t-score"""
        return_list = list()
        for i in range(len(self._dflookup)):
            if self._score_type[i] in ("z", "t"):
                try:
                    return_list.append(self.t_table[self._dflookup[i]][self.alpha])
                except KeyError as exc:
                    raise KeyError(f"t_table lookup cannot interpret "
                          f"df_lookup or alpha (exc={exc}). "
                          f"self.df_lookup = {self._dflookup}, "
                          f"self.alpha = {self.alpha}")
            else:
                raise ValueError(f"Score calculation not implemented for "
                                 f"self.score_type={self._score_type}")
        return tuple(return_list)

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
            return_list.append(self.ci_score[i] * self.sterr[i])
        return tuple(return_list)

    @property
    def ci(self) -> tuple:
        """
        Return (ci_lower, ci_upper), i.e. a tuple containing the
        lower mean estimation, upper mean estimation at confidence
        level = cl, default 0.95 (95% confidence).

        * CI = mean +- t-score * sterr
        """
        return_list = list()
        for i in range(len(self.data)):
            if self.data[i] == ():
                break
            return_list.append((self.mean[i] - self.moe[i], self.mean[i] + self.moe[i]))
        return tuple(return_list)

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
            (f"{self._score_type}-score", "{:,}".format(round(self.ci_score[0], 3))),
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

    def hypothesis_test(self,
                        h0_mu_equals: float,
                        first_data_set=0,
                        second_data_set=None,
                        samples_dependent=False,
                        verbose=False) -> tuple or str:
        """Takes data and null hypothesis, returns a tuple with test score,
        p-value, alpha, and interpretation ("Reject null", "Can't reject null")"""
        from math import sqrt
        return_test_score = float()
        return_p_value = float()
        return_interpretation = str()

        def p_value(z_score: float, tail: str = "two") -> float:
            """Returns the cumulative normal distribution at a z of z_score, two-tailed
            by default.

            :param float z_score: Z-score lookup value used in the table, from -inf to +inf
            :param str tail: Whether the test is "left" tailed, "right" tailed, or "two"-tailed (default)
            """
            # Data validation
            assert isinstance(z_score, float) or isinstance(z_score, int), \
                "z_score must be of type 'float' or 'int'"
            assert tail in ("left", "right", "two"), \
                "Acceptable tail values: 'left', 'right', 'two'"

            # Scores less than -3.49 have approx. cumulative area = 0.0001
            # Scores greater than 3.49 are approx. cumulative area = 0.9999
            z_score = round(z_score, 2)

            if z_score < -3.49:
                if tail == "right":
                    return 0.9999
                else:
                    return 0.0001
            elif z_score > 3.49:
                if tail == "left":
                    return 0.9999
                else:
                    return 0.0001

            # For negative scores, subtract the area represented by the absolute
            # value of the negative score from 1
            # print(f"z_score = {z_score}")
            cumulative_left_area = 0.0
            return_p_value = 0.0
            if z_score < 0:
                # print("z_score < 0")
                cumulative_left_area = 1 - self.z_table[abs(z_score)]
            else:
                # print("z_score > 0")
                cumulative_left_area = self.z_table[abs(z_score)]
            # print(f"cla = {cumulative_left_area}")
            if tail == "two":
                # print("tail = 'two'")
                if cumulative_left_area > 0.5:
                    cumulative_left_area = round(1 - cumulative_left_area, 4)
                if cumulative_left_area == 0.0001:
                    return_p_value = cumulative_left_area
                else:
                    return_p_value = 2 * cumulative_left_area
            elif tail == "right":
                # print("tail = 'right'")
                return_p_value = 1 - cumulative_left_area
            else:
                # print("tail = 'left'")
                return_p_value = cumulative_left_area

            return round(return_p_value, 4)

        def interpret_p_value(p_value: float, alpha: float):
            fail_to_reject = "fail to reject the null hypothesis"
            reject = "reject the null hypothesis"

            if p_value >= alpha:
                return fail_to_reject
            else:
                return reject

        def verbose_explanation(score_type, cl, tail, alpha, score, p_value, interpretation) -> str:
            tail_dict = {"left": "<", "right": ">", "two": "!="}
            equal_dict = {"left": ">=", "right": "<=", "two": "="}
            p_value_with_comparator = f"<{p_value}" if p_value == 0.0001 else p_value
            return f"The resulting {'z' if 'z' in score_type else 't'}-score for this hypothesis test " \
                   f"is {round(score, 3)}, which provides a p-value of {p_value_with_comparator}. " \
                   f"If we compare this p-value to our alpha (cl={cl}, tail={tail}, " \
                   f"\N{GREEK SMALL LETTER ALPHA}{'/2' if tail == 'two' else ''}={alpha}), " \
                   f"we can see that {p_value} " \
                   f"{'>=' if p_value >= alpha else '<'} {alpha}. Therefore, we " \
                   f"{interpretation} (h0: \N{GREEK SMALL LETTER MU} {equal_dict[tail]} {h0_mu_equals}) " \
                   f"in favor of the alternative hypothesis (h1: \N{GREEK SMALL LETTER MU} {tail_dict[tail]} {h0_mu_equals})"

        # For single populations
        if second_data_set is None:
            return_test_score = (self.mean[first_data_set] - h0_mu_equals) \
                                / (self.stdev[first_data_set] / sqrt(self.n[first_data_set]))
            return_p_value = p_value(return_test_score, self.tail)
            return_interpretation = interpret_p_value(return_p_value, self.alpha)
        # For two populations
        else:
            if "z" in self._score_type:
                # Two populations, population variance is known, test for true mean difference
                return_test_score = ((self.mean[first_data_set] - self.mean[second_data_set]) - h0_mu_equals) \
                                    / sqrt((self.var[first_data_set]/self.n[first_data_set])
                                           + (self.var[second_data_set]/self.n[second_data_set]))
                return_p_value = p_value(return_test_score, self.tail)
                return_interpretation = interpret_p_value(return_p_value, self.alpha)
            # Student t-tests
            else:
                if samples_dependent:

                    print("Not implemented")







        if verbose:
            return verbose_explanation(self._score_type, self.cl, self.tail, self.alpha,
                                       round(return_test_score, 3), return_p_value, return_interpretation)
        else:
            return round(return_test_score, 3), return_p_value, self.alpha, return_interpretation


if __name__ == "__main__":
    dsObject = DescriptiveStats(
        (0, 0, 0, 0, 0, 1, 2, 3, 4, 4, 5, 6, 10),
        # data2=(38, 34, 19, 56, 41, 48, 15),
        # is_population=True,
        # cl=0.99,
        tail="left")
    # print(dsObject.mean)
    print(dsObject.hypothesis_test(5, verbose=True))
    # print(dsObject.tail)
    # print(dsObject.describe())
