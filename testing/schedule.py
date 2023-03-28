import pandas as pd
import numpy as np


class Schedule:
    tas_max = None
    tas_pref = None
    min_tas = None
    sec_len = None
    num_tas = None
    times = None

    def __init__(self, sol_csv):
        self.sch_sol = np.loadtxt(sol_csv, delimiter=",", dtype=int)
        self.w_sol = np.multiply(self.sch_sol, Schedule.tas_pref)


    @staticmethod
    def load_sections(csv):
        # load tas
        df = pd.read_csv(csv)

        # filter df
        df_min = df['min_ta']

        Schedule.min_tas = df_min.to_numpy()

        # converting time to int representation
        df_time = df['daytime']
        s_int, s_categories = df_time.factorize()
        s_int[s_int == 0] = s_int.max() + 1
        Schedule.times = s_int

    @staticmethod
    def load_tas(csv):
        df = pd.read_csv(csv)
        Schedule.tas_max = df['max_assigned'].to_numpy()

        df_p = df.iloc[:, 3:]
        p_map = {'U': -1, 'W': 1, 'P': 2}
        df_p.replace(p_map, inplace=True)
        Schedule.tas_pref = df_p.to_numpy()
        Schedule.num_tas = len(df_p)
        Schedule.sec_len = len(df_p.columns)
