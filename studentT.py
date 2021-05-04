"""studentT.py
Contains the Student-T score table used in ctDescStats.py

first index is df - 1 (df is n - 1), except as follows:
30 : 30 < df <= 35
31: 35 < df <= 40
32: 40 < df <= 45
33: 45 < df <= 50
34: 50 < df

second index is as follows:
0 : 80% confidence
1 : 90% confidence
2 : 95% confidence
3 : 98% confidence
4 : 99% confidence
"""


class ScoreFinder:

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
        99: 0.9999,
    }

    def __init__(self, df: int, alpha: float):

        # Primary initializations
        self.df = df
        self.alpha = alpha
        # Calculated attributes
        # degrees of freedom actually used in score lookup
        self.lookup_df = self.get_lookup_df()
        # determine which score function to use
        self.score_type = self.get_score_type()
        # calculate statistics score
        self.score = self.score_calculate()

    def get_lookup_df(self):
        last_key = 0
        list_of_lookup_dfs = list(ScoreFinder.t_table.keys())
        for i in range(len(list_of_lookup_dfs)):
            current_key = list_of_lookup_dfs[i]
            if current_key == self.df:
                return self.df
            elif max(current_key, self.df) == current_key:
                return last_key
            else:
                last_key = current_key

    def get_score_type(self):
        # TODO: is it a z or t score?
        pass

    def score_calculate(self):
        # TODO: if z, get_z_score
        # TODO: if t, get_t_score
        pass

    def get_z_score(self):
        # TODO
        pass

    def get_t_score(self):
        # TODO
        pass
