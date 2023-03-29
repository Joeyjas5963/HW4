import random as rnd
import copy
from functools import reduce
from schedule import Schedule
import matplotlib.pyplot as plt
from collections import defaultdict
import time


class Evo:

    # initializing the penalty history list
    penalty_trend = [(('overallocation', 0),
                      ('conflicts', 0),
                      ('undersupport', 0),
                      ('unwilling', 0),
                      ('unprefered', 0))]

    # connecting penalty types to agents
    pen_to_agent = {'overallocation': 'allocator',
                    'conflicts': 'time_fix',
                    'undersupport': 'support',
                    'unwilling': 'max_pref',
                    'unprefered': 'max_pref'}

    # starting clock
    start = time.time()

    def __init__(self):
        self.pop = {}   # ((ob1, eval1), (obj2, eval2), ...) ==> solution
        self.fitness = {}  # name -> objective func
        self.agents = {}   # name -> (agent operator, # input solutions)

    def size(self):
        """ The size of the solution population """
        return len(self.pop)

    def add_fitness_criteria(self, name, f):
        """ Registering an objective with the Evo framework
        name - The name of the objective (string)
        f    - The objective function:   f(solution)--> a number """
        self.fitness[name] = f

    def add_agent(self, name, op, k=1):
        """ Registering an agent with the Evo framework
        name - The name of the agent
        op   - The operator - the function carried out by the agent  op(*solutions)-> new solution
        k    - the number of input solutions (usually 1) """
        self.agents[name] = (op, k)

    def get_random_solutions(self, k=1):
        """ Pick k random solutions from the population as a list of solutions
            We are returning DEEP copies of these solutions as a list """
        if self.size() == 0: # No solutions in the populations
            return []
        else:
            popvals = tuple(self.pop.values())
            return [copy.deepcopy(rnd.choice(popvals)) for _ in range(k)]

    def add_solution(self, sol):
        """Add a new solution to the population """
        eval = tuple([(name, f(sol)) for name, f in self.fitness.items()])
        Evo.penalty_trend.append(eval)
        self.pop[eval] = sol

    def run_agent(self, name):
        """ Invoke an agent against the current population """
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)

        for i in range(len(picks)):
            picks[i] = Schedule(sol_array=picks[i])

        new_solution = op(picks)
        self.add_solution(new_solution)

    def evolve(self, n=1, dom=100, status=100):
        """ To run n random agents against the population
        n - # of agent invocations
        dom - # of iterations between discarding the dominated solutions """

        agent_names = list(self.agents.keys())
        for i in range(n):

            # picks the first agent for the first algorithm
            if i == 0:
                pick = agent_names[0]

            else:

                # picks agent based upon which of the last penalties was highest
                last = {}
                for j in range(len(Evo.penalty_trend[-1])):
                    last[Evo.penalty_trend[-1][j][1]] = Evo.penalty_trend[-1][j][0]

                pick = Evo.pen_to_agent[last[min(last.keys())]]

            self.run_agent(pick)

            if i % dom == 0:
                self.remove_dominated()

            end = time.time()

            if i % status == 0 or (end - Evo.start) > 600: # print the population
                self.remove_dominated()
                print("Iteration: ", i)
                print("Population Size: ", self.size())
                print(self)
                print(f'Seconds: {end - Evo.start:.0f}')

                # stops the evolution after ten minutes
                if (end - Evo.start) > 600:
                    break

        # Clean up population
        self.remove_dominated()

    @staticmethod
    def _dominates(p, q):
        pscores = [score for _, score in p]
        qscores = [score for _, score in q]
        score_diffs = list(map(lambda x, y: y - x, pscores, qscores))
        min_diff = min(score_diffs)
        max_diff = max(score_diffs)
        return min_diff >= 0.0 and max_diff > 0.0

    @staticmethod
    def _reduce_nds(S, p):
        return S - {q for q in S if Evo._dominates(p, q)}

    def remove_dominated(self):
        nds = reduce(Evo._reduce_nds, self.pop.keys(), self.pop.keys())
        self.pop = {k:self.pop[k] for k in nds}

    def __str__(self):
        """ Output the solutions in the population """
        rslt = ""
        for eval,sol in self.pop.items():
            rslt += str(dict(eval))+"\n"+str(sol)+"\n"

        return rslt

    @staticmethod
    def plot_trend():

        pen_dict = defaultdict(lambda: [])

        for i in range(len(Evo.penalty_trend)):
            for j in range(len(Evo.penalty_trend[i])):
                pen_dict[Evo.penalty_trend[i][j][0]].append(Evo.penalty_trend[i][j][1])

        pen_dict = dict(pen_dict)

        for key, value in pen_dict.items():
            plt.plot(range(len(value[1:])), value[1:], label=key)

        plt.legend()
        plt.show()



