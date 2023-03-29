import pandas as pd
import numpy as np


class Schedule:
    """
    A solution class in our evolutionary framework that describes constraints
    and contains solution as a 2D numpy array of 1s & 0s.

    Attributes:
        tas_max (ndarray): an array describing the max assignments per TA
        tas_pref (ndarray): a 2D array describing each TA's preferences
        min_tas (ndarray): the minimum # of tas required per section
        sec_len (int): number of sections
        num_tas (int): number of TAs
        times (ndarray): daytimes represented as integers
    """
    tas_max = None
    tas_pref = None
    min_tas = None
    sec_len = None
    num_tas = None
    times = None

    def __init__(self, sol_csv=None, sol_array=None):
        # Loading solution

        self.sch_sol = sol_array

        if sol_csv:
            # Loading if given csv
            self.sch_sol = np.loadtxt(sol_csv, delimiter=",", dtype=int)
            self.w_sol = np.multiply(self.sch_sol, Schedule.tas_pref)

        else:
            # Randomly generating solution based on schedule requirements
            n_tas = Schedule.num_tas
            n_sec = Schedule.sec_len

            # Probability = average number of TAs per section
            pr = np.mean(Schedule.min_tas) / n_sec
            self.sch_sol = np.random.choice([0, 1], size=(n_tas, n_sec),
                                            p=[1-pr, pr])
            self.w_sol = np.multiply(self.sch_sol, Schedule.tas_pref)

    def __str__(self):

        return 'I AM A SOLUTION'

    @staticmethod
    def load_sections(csv):
        """
        Loads sections with csv and registers attributes to class
        """
        df = pd.read_csv(csv)

        # Filter df for minimum required TAs
        df_min = df['min_ta']

        # Register min_tas
        Schedule.min_tas = df_min.to_numpy()

        # Converting time to int representation for computation
        df_time = df['daytime']
        s_int, s_categories = df_time.factorize()
        s_int[s_int == 0] = s_int.max() + 1

        # Register times
        Schedule.times = s_int

    @staticmethod
    def load_tas(csv):
        """
        Loads TA info with csv and registers class attributes
        """
        df = pd.read_csv(csv)

        # Register tas_max
        Schedule.tas_max = df['max_assigned'].to_numpy()

        # Map preference matrix to numeric values/weights
        df_p = df.iloc[:, 3:]
        p_map = {'U': -1, 'W': 1, 'P': 2}
        df_p.replace(p_map, inplace=True)

        # Register tas_pref, num_tas, sec_len
        Schedule.tas_pref = df_p.to_numpy()
        Schedule.num_tas = len(df_p)
        Schedule.sec_len = len(df_p.columns)
