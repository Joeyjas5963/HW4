import numpy as np
from schedule import Schedule
import random

def max_pref(picks):

    sol = picks[0]

    # sum each TAs preference values
    pref_vec = np.sum(sol.w_sol, axis=1)

    # find TAs with lowest preference values
    ta_idx_0, ta_idx_1 = np.argsort(pref_vec)[:2]

    # isolate a random section that they were assigned to
    ta_0, ta_1 = sol.sch_sol[ta_idx_0], sol.sch_sol[ta_idx_1]
    sects_0, sects_1 = np.where(ta_0 == 1), np.where(ta_1 == 1)

    sect_0 = random.choice(sects_0[0])
    sect_1 = random.choice(sects_1[0])

    # swap the two sections between the TAs
    sol.sch_sol[ta_idx_0, sect_0] = 0
    sol.sch_sol[ta_idx_0, sect_1] = 1
    sol.sch_sol[ta_idx_1, sect_0] = 1
    sol.sch_sol[ta_idx_1, sect_1] = 0

    return sol.sch_sol
