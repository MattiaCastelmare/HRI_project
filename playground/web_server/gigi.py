from kstar_planner import planners
from pathlib import Path

domain_file = Path("puzzle_domain.pddl")
problem_file = Path("puzzle_problem.pddl")
print("CIAO ANTONIO")
plans = planners.plan_topk(domain_file=domain_file, problem_file=problem_file, number_of_plans_bound=100, timeout=30)
print(plans)
print("Ciao Mattia")
