import numpy as np
import pandas as pd
import random as rnd
from copy import copy
from evo import Evo


class TA:

    def __init__(self, row):

        self.id = row[0]
        self.max = row[2]
        self.pref = row[3:]
        self.sections = []


class Section:

    def __init__(self, row):

        self.id = row[0]
        self.inst = row[1]
        self.time = row[2]
        self.location = row[3]
        self.topic = row[5]
        self.min = row[6]
        self.max = row[7]
        self.tas = []


def assign(section, ta):

    section.tas.append(ta)
    ta.sections.append(section)


def get_array(sections, tas):

    array = np.loadtxt('test_cases/test1.csv', delimiter=',', dtype=int) * 0

    for ta in tas:
        for section in ta.sections:
            array[ta.id, section.id] = 1

    print(array)

def setup():

    df_sections = pd.read_csv('sections_easy.csv')
    df_ta = pd.read_csv('tas.csv')

    sections = []
    for i in range(len(df_sections)):
        s = Section(df_sections.loc[i, :])
        sections.append(s)

    tas = []
    for i in range(len(df_ta)):
        t = TA(df_ta.loc[i, :])
        tas.append(t)

    return sections, tas


def random_start(sections, tas):

    for ta in tas:
        random_sections = rnd.sample(sections, rnd.randint(1, len(sections)))
        for section in random_sections:
            assign(section, ta)

    for section in sections:
        print(section.tas)


def overallocation(tas):

    penalty_sum = 0
    for ta in tas:
        if len(ta.sections) > ta.max:
            penalty = len(ta.sections) - ta.max
            penalty_sum += penalty

    print(penalty_sum)

    return penalty_sum


def conflicts(tas):

    penalty_sum = 0
    for ta in tas:
        times = []
        for section in ta.sections:
            times.append(section.time)

        times_set = set(times)

        if len(times_set) < len(times):
            penalty = len(times) - len(times_set)
            penalty_sum += penalty

    print(penalty_sum)

    return penalty_sum


def undersupport(sections):

    penalty_sum = 0
    for section in sections:
        if len(section.tas) < section.min:
            penalty = section.min - len(section.tas)
            penalty_sum += penalty

    print(penalty_sum)

    return penalty_sum


def unwilling(tas):

    penalty_sum = 0
    for ta in tas:
        for section in ta.sections:
            opinion = ta.pref[section.id]
            if opinion == 'U':
                penalty_sum += 1

    print(penalty_sum)

    return penalty_sum


def unprefered(tas):

    penalty_sum = 0
    for ta in tas:
        for section in ta.sections:
            opinion = ta.pref[section.id]
            if opinion != 'P':
                penalty_sum += 1

    print(penalty_sum)

    return penalty_sum


def main():


    sections, tas = setup()


    random_start(sections, tas)

    get_array(sections, tas)

    """
    overallocation(tas)
    conflicts(tas)
    undersupport(sections)
    unwilling(tas)
    unprefered(tas)
    """

main()



