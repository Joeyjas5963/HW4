from evo import Evo
from objectives import *
from agents import *
from agents_2 import *
from schedule import Schedule


def random_start():
    """ Creates a random starting position for the model

    Args:
        None

    Returns:
        start (np array): Array of a starting schedule
    """

    # creates an array the size of the schedule
    start = np.zeros((43, 17), dtype=int)
    options = [0, 1]

    # puts ones and zeroes into the array
    for i in range(len(start)):
        for j in range(len(start[i])):
            start[i][j] = choice(options, 1, p=[.8, .2])

    return start

def main():
    """ Runs the evolution class

    """

    # creating the evolution object
    E = Evo()

    # adding all of the fitness objectives
    E.add_fitness_criteria('overallocation', overallocation)
    E.add_fitness_criteria('conflicts', conflicts)
    E.add_fitness_criteria('undersupport', undersupport)
    E.add_fitness_criteria('unwilling', unwilling)
    E.add_fitness_criteria('unprefered', unprefered)

    # adding all of the agents
    E.add_agent('allocator', allocator)
    E.add_agent('time_fix', time_fix)
    E.add_agent('support', support)
    E.add_agent('max_pref', max_pref)

    # adding a solution for the first random instance
    E.add_solution(random_start())

    # loading csvs into the schedule object for agent reference
    Schedule.load_tas('tas.csv')
    Schedule.load_sections('sections.csv')

    # running the evolution algorithm
    E.evolve(1000000, 100, 100)


if __name__ == '__main__':
    main()
    print('DONE')