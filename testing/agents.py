from copy import copy
import numpy as np


def allocator(picks):

    # grabs first solution
    sol = picks[0]

    s = sol.sch_sol.sum(axis=1)
    mask = s > sol.tas_max

    def r_array(m_as, len):
        pr = m_as / len
        return np.random.choice([0, 1], len, p=[1 - pr, pr])

    n_sol = copy(sol)

    for i, b in enumerate(mask):
        if b:
            n_arr = r_array(n_sol.tas_max[i], n_sol.sec_len)
            n_sol.sch_sol[i] = n_arr

    return n_sol.sch_sol


def time_fix(picks):

    sol = picks[0]

    n_sol = copy(sol)

    for i, row, in enumerate(n_sol.sch_sol):
        h_arr = np.multiply(n_sol.times, row)
        # Get the unique values and their indices in the original array
        unique_vals, unique_idx = np.unique(h_arr, return_index=True)

        # Create a new array with the same shape as the original array,
        # filled with zeros
        new_arr = np.zeros_like(h_arr)

        # Put the unique values back into the new array at their
        # original indices
        np.put(new_arr, unique_idx, unique_vals)

        # Replace duplicate nonzero values with zero randomly
        nonzero_vals = new_arr[new_arr != 0]
        unique_nonzero_vals = np.unique(nonzero_vals)
        for val in unique_nonzero_vals:
            indices = np.where(new_arr == val)[0]
            if len(indices) > 1:
                replace_idx = np.random.choice(indices, size=len(indices) - 1,
                                               replace=False)
                new_arr[replace_idx] = 0

        n_sol.sch_sol[i] = np.where(new_arr != 0, 1, 0)

    return n_sol.sch_sol


def support(picks):

    sol = picks[0]

    sec_tas = sol.sch_sol.sum(axis=0)
    mask = sec_tas < sol.min_tas

    def r_array(m_as, len):
        pr = m_as / len
        return np.random.choice([0, 1], len, p=[1 - pr, pr])

    n_sol = copy(sol)

    for i, b in enumerate(mask):
        if b:
            n_arr = r_array(n_sol.min_tas[i] + 2, n_sol.num_tas)
            n_sol.sch_sol[:, i] = n_arr

    return n_sol.sch_sol
