import numpy as np
import pandas as pd
from numpy.random import choice
from schedule import Schedule


def grab_csvs():
    """ gets the csvs for objective evaluation

    Returns:
        df_ta (Pandas DataFrame): table of TA data
        df_section (Pandas DataFrame): table of section data
    """

    # reading csvs
    df_ta = pd.read_csv('tas.csv')
    df_section = pd.read_csv('sections_easy.csv')

    return df_ta, df_section


def overallocation(array):
    """ evaluates overallocation objective

    Args:
        array (NumPy Array): array to be evaluated

    Returns:
        penalty_sum (int): penalty for this objective
    """

    # getting csv data
    df_ta, df_sections = grab_csvs()

    # rotates array to look at TAs
    array = np.rot90(array)

    # finds all of the assignments that puts the TA over max allocation
    penalty_sum = 0
    for i in range(len(array)):
        if sum(array[i]) > df_ta.iloc[i, 2]:
            penalty_sum += sum(array[i]) - df_ta.iloc[i, 2]

    return penalty_sum


def conflicts(array):

    df_ta, df_sections = grab_csvs()

    penalty_sum = 0
    for i in range(len(array)):
        time_list = []
        for j in range(len(array[i])):
            if array[i][j] == 1:
                time_list.append(df_sections.iloc[j, 2])

        if time_list != set(time_list):
            penalty_sum += len(time_list) - len(set(time_list))

    return penalty_sum


def undersupport(array):

    df_ta, df_sections = grab_csvs()

    array = np.rot90(array)

    penalty_sum = 0
    for i in range(len(array)):
        if sum(array[i]) < df_sections.iloc[i, -2]:
            penalty_sum += df_sections.iloc[i, -2] - sum(array[i])

    return penalty_sum


def unwilling(array):

    df_ta, df_section = grab_csvs()

    pref_matrix = df_ta.iloc[:, 3:].to_numpy()

    penalty_sum = 0
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == 1 and pref_matrix[i][j] == 'U':
                penalty_sum += 1

    return penalty_sum


def unprefered(array):

    df_ta, df_section = grab_csvs()

    pref_matrix = df_ta.iloc[:, 3:].to_numpy()

    penalty_sum = 0
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == 1 and pref_matrix[i][j] != 'P':
                penalty_sum += 1

    return penalty_sum

