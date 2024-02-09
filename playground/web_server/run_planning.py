from pyperplan.pddl.parser import Parser
from pyperplan import grounding, planner
import numpy as np

from pddl.logic import Predicate, variables, constants
from pddl.core import Domain, Problem
from pddl.action import Action
from pddl.formatter import domain_to_string, problem_to_string
from pddl.requirements import Requirements

from pddl.logic.base import And

def generation_constants(num_const, pathStr):
  dictionary=dict()
  cos_list = []
  num=1
  for x in range(1, num_const+1 ):
      st= pathStr+str(num)
      dictionary[pathStr+'%d' %x] = constants(st)
      cos_list.extend(dictionary[pathStr+'%d' % x])
      num+=1

  return cos_list

def generate_pddl_file(initial_positions):
    #Define the requirements
    requirements = [Requirements.STRIPS]
    
    # set up variables 
    x, px, y, py, p= variables("x px y py p")
    
    # generate the constant depending on the initial_position
    number_constants= len(initial_positions)
    piece_list=generation_constants(number_constants,'c')
    pos_list=generation_constants(number_constants,'p')
    
    #create the list of the object for the problem.pddl file
    obj= piece_list + pos_list

    # Define predicates
    position_pred = Predicate("POSITION", p)
    piece_pred = Predicate("PIECE", x)
    at_pred = Predicate("at", p, x)

    # Define actions
    swap_action = Action(
        "swap",
        parameters=[px, x, py, y],
        precondition= position_pred(px) & position_pred(py) & piece_pred(x) & piece_pred(y) & at_pred(px, x) & at_pred(py, y),
        effect= at_pred(px, y) & at_pred(py, x) & ~at_pred (px, x) & ~at_pred(py, y)
    )
    
    #Define the domain 
    domain = Domain("puzzle2",
                requirements=requirements,
                predicates=[position_pred, piece_pred, at_pred],
                actions=[swap_action])
    
    
    # Define initial state
    initial_state = [position_pred(elem) for elem in pos_list]
    initial_state.extend([piece_pred(elem) for elem in piece_list])
    
    index=0
    for elem in initial_positions:
        puzz_piece=piece_list[elem-1]
        initial_state.append(at_pred(pos_list[index], puzz_piece))
        index+=1
        
    goal_state = []
    for i in range(0,number_constants):
        puzz_piece=piece_list[elem-1]
        goal_state.append(at_pred(pos_list[i], piece_list[i]))
    
    
    # Define the problem
    problem = Problem(
            "puzzle_problem", 
            domain=domain,
            objects= obj,
            requirements= None,
            init= initial_state,
            goal= And(*goal_state
                      )
            )
    
    prob_string=problem_to_string(problem).replace("(:requirements :strips)", '')
    # Write domain and problem to files
    with open("puzzle_domain.pddl", "w") as domain_file:
        domain_file.write(domain_to_string(domain))

    with open("puzzle_problem.pddl", "w") as problem_file:
        problem_file.write(prob_string)
        


def run_planning(domain_pddl, problem_pddl, search_alg_name,
                 heuristic_name=None):
  """Plan a sequence of actions to solve the given PDDL problem.

  This function is a lightweight wrapper around pyperplan.

  Args:
    domain_pddl_str: A str, the contents of a domain.pddl file.
    problem_pddl_str: A str, the contents of a problem.pddl file.
    search_alg_name: A str, the name of a search algorithm in
      pyperplan. Options: astar, wastar, gbf, bfs, ehs, ids, sat.
    heuristic_name: A str, the name of a heuristic in pyperplan.
      Options: blind, hadd, hmax, hsa, hff, lmcut, landmark.

  Returns:
    plan: A list of actions; each action is a pyperplan Operator.
  """
  # Parsing the PDDDL
  parser = Parser(domain_pddl, problem_pddl)
  domain = parser.parse_domain()
  problem = parser.parse_problem(domain)
  print('ecco')
  # Ground the PDDL
  task = grounding.ground(problem)
  print('ah boh')
  # Get the search alg
  search_alg = planner.SEARCHES[search_alg_name]
  print('bella ciao')
  if heuristic_name is None:
    print('so entrato')
    plan=search_alg(task)
    print('sto uscendo')
    return plan
  
  # Get the heuristic
  heuristic = planner.HEURISTICS[heuristic_name](task)
  print('ma perchè ci metto così tanto?')
  plan=search_alg(task, heuristic)
  print('almeno è andato')
  # Run planning
  return plan

'''
def alternativa(domain_pddl, problem_pddl):
  # Crea un'istanza del pianificatore
  planner = Planner("path/to/domain.pddl", "path/to/problem.pddl")

  # Risolvi il problema PDDL
  solution = planner.solve()

  # Stampa la prima azione
  print(solution[0])
'''