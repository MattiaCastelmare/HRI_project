from pyperplan.pddl.parser import Parser
from pyperplan import grounding, planner, heuristics, search

from run_planning import run_planning, generate_pddl_file
import re

initial_state=[3, 4, 8, 5, 2, 1, 9, 6, 7]

generate_pddl_file(initial_state)

# Carica il dominio e il problema PDDL
domain_file = 'domainPuzzle.pddl'
problem_file = 'problem.pddl'

plan = run_planning(domain_file, problem_file, "gbf", "hadd")
act=str(plan[0])
act_str=act.split('\n')[0]

plan2= run_planning('puzzle_domain.pddl', 'puzzle_problem.pddl',"gbf", "hadd")

# Definisci il pattern regex per trovare i numeri preceduti da "c"
pattern = r"c(\d+)"

# Trova tutti i numeri che corrispondono al pattern nella stringa
matches = re.findall(pattern, act_str)

# Estrai i primi due numeri trovati
if len(matches) >= 2:
    cNumero1 = matches[0]
    cNumero2 = matches[1]
    
print(f'Pepper move: {cNumero1},{cNumero2}')
print(f'The first planning gives:{plan}')
print(f'the second planning gives:{plan2}')
