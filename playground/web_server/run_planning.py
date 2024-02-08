from pyperplan.pddl.parser import Parser
from pyperplan import grounding, planner
import numpy as np

from pddl.logic import Predicate, variables, constants
from pddl.core import Domain, Problem
from pddl.action import Action
from pddl.formatter import domain_to_string, problem_to_string
from pddl.requirements import Requirements

from pddl.logic.base import And


def generate_pddl_file(initial_positions):
    #Define the requirements
    requirements = [Requirements.STRIPS]
    
    # set up variables and constants
    x, px, y, py, p= variables("x px y py p")
    p1, p2, p3, p4, p5, p6, p7, p8, p9= constants("p1 p2 p3 p4 p5 p6 p7 p8 p9")
    c1, c2, c3, c4, c5, c6, c7, c8, c9= constants("c1 c2 c3 c4 c5 c6 c7 c8 c9")
    
    goal=[c1, c2, c3, c4, c5, c6, c7, c8, c9]
    pos_puzzle=[p1, p2, p3, p4, p5, p6, p7, p8, p9]
    
    #create the list of the object for the problem.pddl file
    obj= goal + pos_puzzle

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
    initial_state = [position_pred(p1), position_pred(p2), position_pred(p3), position_pred(p4), position_pred(p5), position_pred(p6), position_pred(p7), position_pred(p8), position_pred(p9), piece_pred(c1), piece_pred(c2), piece_pred(c3), piece_pred(c4), piece_pred(c1), piece_pred(c5), piece_pred(c6), piece_pred(c7), piece_pred(c8), piece_pred(c9)]
    index=0
    for elem in initial_positions:
        puzz_piece=goal[elem-1]
        initial_state.append(at_pred(pos_puzzle[index], puzz_piece))
        index+=1
        
    # Define the problem
    problem = Problem(
            "puzzle_problem", 
            domain=domain,
            objects= obj,
            requirements= None,
            init= initial_state,
            goal= And(at_pred(p1,c1),
                      at_pred(p2,c2),
                      at_pred(p3,c3),
                      at_pred(p4,c4),
                      at_pred(p5,c5),
                      at_pred(p6,c6),
                      at_pred(p7,c7),
                      at_pred(p8,c8),
                      at_pred(p9,c9)
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

  # Ground the PDDL
  task = grounding.ground(problem)

  # Get the search alg
  search_alg = planner.SEARCHES[search_alg_name]

  if heuristic_name is None:
    return search_alg(task)

  # Get the heuristic
  heuristic = planner.HEURISTICS[heuristic_name](task)

  # Run planning
  return search_alg(task, heuristic)