from pddl_planning.definition import *
# Import the PDDLReader and PDDLWriter classes 
import unified_planning
from unified_planning.shortcuts import *
from unified_planning.io.pddl_reader import PDDLReader

class Planning():
    def __init__(self, algorithm_name, heuristic_name):
        self.domain_file = user_dir + "/pddl_planning/puzzle_domain.pddl"
        self.problem_file = user_dir + "/pddl_planning/puzzle_problem.pddl"
        self.algorithm_name = algorithm_name
        self.heuristic_name = heuristic_name
        self.oldPlan_len = 1000000
        self.num_error = 0

    def solve(self, index_list):
            swaps = []
            # Generate the new pddl files and execute the new pddl
            generate_pddl_file(index_list)
            # DIFFFICULTY EASY OR MEDIUM ONLY 9 PIECES
            if len(index_list) == 9:
                plan = self.generate_plan()
            # DIFFFICULTY HARD 16 PIECES
            if len(index_list)== 16:
                plan = self.generate_plan16()
            if self.check_empty_plan(plan):
                return None, None
            print("The plan is: ", plan + "with len:" + str(len(plan)))
            # Compute the number of action need to resolve the puzzle
            num_action = len(plan)
            play_well = self.count_errors(num_actions=num_action)
            swaps.append(self.generate_swap(action=plan[0]))
            if self.num_error == 3:
                swaps.append(self.generate_swap(action=plan[1]))
                # Reset counter 
                self.num_error = 0
            self.oldPlan_len = num_action
            return swaps, play_well
    
    def generate_plan16(self):
        plan = []
        reader = PDDLReader()
        pddl_problem = reader.parse_problem(self.domain_file, self.problem_file)
        #pddl_problem.environment.factory.add_engine(name = "lpg", module_name = "up_lpg.lpg_planner", class_name = "LPGEngine")
        with OneshotPlanner(name='fast-downward') as planner: 
                result = planner.solve(pddl_problem, timeout=30)        
        # Itera attraverso le azioni nel piano 
        for action in result.plan.actions: 
            # Aggiungi la rappresentazione stringa dell'azione alla lista 
            plan.append(str(action))
        return plan

    def generate_plan(self):
        # Define Parser
        parser = Parser(self.domain_file, self.problem_file)
        domain = parser.parse_domain()
        problem = parser.parse_problem(domain)
        # Ground the PDDL
        task = grounding.ground(problem)
        # Get the search alg
        search_alg = planner.SEARCHES[self.algorithm_name]
        # Get the heuristic
        heuristic = planner.HEURISTICS[self.heuristic_name](task)
        # Generate new plan
        plan = search_alg(task, heuristic)
        return plan
    
    def generate_swap(self, action):
        swap = str(action).split('\n')[0]
        # Extract the two position to switch
        matches = re.findall(r"p(\d+)", swap)
        if len(matches) >= 2:
            puzzlePos1 = matches[0]
            puzzlePos2 = matches[1]
        return (puzzlePos1, puzzlePos2)

    def check_empty_plan(self, plan):
        if len(plan) == 0:
            self.oldPlan_len = 100000
            self.num_error = 0
            return True 
        else:
            return False

    def count_errors(self, num_actions):
        if num_actions >= self.oldPlan_len:
            print("\nONE ERROR MADE")
            self.num_error += 1
            print("\nNUM ERRORS:", self.num_error)
            return False
        print("\nNUM ERRORS:", self.num_error)
        return True