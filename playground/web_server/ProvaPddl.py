from pyperplan.pddl.parser import Parser
from pyperplan import grounding, planner, heuristics, search

from run_planning import run_planning, generate_pddl_file
import re
import time

initial_state=[1, 6, 2, 5, 0, 7, 4, 3, 8]

generate_pddl_file(initial_state)

# Carica il dominio e il problema PDDL
domain_file = 'puzzle_domain.pddl'
problem_file = 'puzzle_problem.pddl'

alg= "ehs" #ehs
heu= "landmark" #"hff"

start_time = time.time()
plan= run_planning(domain_file, problem_file, alg, heu)
print('perchè non')
end_time = time.time()

tempo_trascorso = end_time - start_time
print(f"Tempo di esecuzione di {alg} e heuristica {heu}", tempo_trascorso, "secondi")
act=str(plan[0])
act_str=act.split('\n')[0]
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
