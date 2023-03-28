from agents import allocator, time_fix
from schedule import Schedule


def main():
    Schedule.load_tas('tas.csv')
    Schedule.load_sections('sections_easy.csv')
    sol = Schedule('test_cases/test1.csv')

    print(sol.sch_sol)
    n_sol = time_fix(sol)

    print(n_sol.sch_sol)
    #print(sol.sch_sol)
    s = sol.sch_sol.sum(axis=1)
    print(s > sol.tas_max)
    n_sol = allocator(sol)
    n = n_sol.sch_sol.sum(axis=1)
    print(n > sol.tas_max)


if __name__ == '__main__':
    main()
