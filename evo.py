import random as rnd
import copy
from functools import reduce


class Evo:

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
        self.pop[eval] = sol

    def run_agent(self, name):
        """ Invoke an agent against the current population """
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_solution = op(picks)
        self.add_solution(new_solution)

    def evolve(self, n=1, dom=100, status=100):
        """ To run n random agents against the population
        n - # of agent invocations
        dom - # of iterations between discarding the dominated solutions """

        agent_names = list(self.agents.keys())
        for i in range(n):
            pick = rnd.choice(agent_names) # pick an agent to run
            self.run_agent(pick)
            if i % dom == 0:
                self.remove_dominated()

            if i % status == 0: # print the population
                self.remove_dominated()
                print("Iteration: ", i)
                print("Population Size: ", self.size())
                print(self)

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
            rslt += str(dict(eval))+":\t"+str(sol)+"\n"
        return rslt