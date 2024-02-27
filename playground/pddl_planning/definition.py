from utils import*
from pyperplan.pddl.parser import Parser
from pyperplan import grounding, planner
from pddl.logic import Predicate, variables, constants
from pddl.core import Domain, Problem
from pddl.action import Action
from pddl.formatter import domain_to_string, problem_to_string
from pddl.requirements import Requirements
from pddl.logic.base import And

def generation_constants(num_const, path_str):
    dictionary = dict()
    cos_list = []
    num = 0
    for x in range(0, num_const):
        st = path_str + str(num)
        dictionary[path_str + '%d' % x] = constants(st)
        cos_list.extend(dictionary[path_str + '%d' % x])
        num += 1
    return cos_list

def define_predicates(x, p):
    position_pred = Predicate("POSITION", p)
    piece_pred = Predicate("PIECE", x)
    at_pred = Predicate("at", p, x)
    return position_pred, piece_pred, at_pred

def define_actions(px, x, py, y, position_pred, piece_pred, at_pred):
    return Action(
        "swap",
        parameters=[px, x, py, y],
        precondition=position_pred(px) & position_pred(py) & piece_pred(x) & piece_pred(y) & at_pred(px, x) & at_pred(py, y),
        effect=at_pred(px, y) & at_pred(py, x) & ~at_pred(px, x) & ~at_pred(py, y)
    )

def define_domain(requirements, predicates, actions):
    return Domain("puzzle", requirements=requirements, predicates=predicates, actions=actions)

def define_initial_state(pos_list, piece_list, index_list, position_pred, piece_pred, at_pred):
    initial_state = [position_pred(elem) for elem in pos_list]
    initial_state.extend([piece_pred(elem) for elem in piece_list])
    index = 0
    for elem in index_list:
        puzz_piece = piece_list[elem]
        initial_state.append(at_pred(pos_list[index], puzz_piece))
        index += 1 
    return initial_state

def define_goal_state(pos_list, piece_list, at_pred):
    goal_state = [at_pred(pos_list[i], piece_list[i]) for i in range(len(piece_list))]
    return goal_state

def write_domain_and_problem_to_files(domain, prob_string):
    with open("puzzle_domain.pddl", "w") as domain_file:
        domain_file.write(domain_to_string(domain))
    with open("puzzle_problem.pddl", "w") as problem_file:
        problem_file.write(prob_string)

def generate_pddl_file(index_list):
    # Define the requirements, variables, and predicates
    requirements = [Requirements.STRIPS]
    x, px, y, py, p = variables("x px y py p")
    position_pred, piece_pred, at_pred = define_predicates(x, p)
    # Generate the constant depending on the initial_position
    number_constants = len(index_list)
    piece_list = generation_constants(number_constants, 'c')
    pos_list = generation_constants(number_constants, 'p')
    # Create the list of the object for the problem.pddl file
    obj = piece_list + pos_list
    # Define actions
    swap_action = define_actions(px, x, py, y, position_pred, piece_pred, at_pred)
    # Define the domain 
    domain = define_domain(requirements, [position_pred, piece_pred, at_pred], [swap_action])
    # Define initial state
    initial_state = define_initial_state(pos_list, piece_list, index_list, position_pred, piece_pred, at_pred)
    # Define goal state
    goal_state = define_goal_state(pos_list, piece_list, at_pred)
    # Define the problem
    problem = Problem(
        "puzzle_problem", 
        domain=domain,
        objects=obj,
        requirements=None,
        init=initial_state,
        goal=And(*goal_state)
    )
    prob_string = problem_to_string(problem).replace("(:requirements :strips)", '')
    # Write domain and problem to files
    write_domain_and_problem_to_files(domain, prob_string)
