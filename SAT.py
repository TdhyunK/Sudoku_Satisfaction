from random import randint, uniform, choice

class SAT:

	def __init__(self, cnf_path):
		self.file_path = cnf_path
		self.solution_attempts = 0
		self.variable_to_index_dict = self.init_variable_to_index_dict()
		self.index_to_variable_dict = self.init_index_to_variable_dict()
		self.assignment_dict = {}
		# print(self.variable_to_index_dict)
		# print(self.index_to_variable_dict)
		self.clause_constraint_list = self.init_clause_constraint_set()
		# print(self.clause_constraint_list)
		# self.random_assignment()
		# print("assignment dict: " + str(self.assignment_dict))

	def GSAT(self):	
		self.random_assignment()
		threshold = 0.5
		self.solution_attempts += 1
		while not self.satisfy_clauses():
			self.solution_attempts += 1			
			# print(self.assignment_dict)
			random_flip = uniform(0, 1)

			if random_flip > threshold:
				random_key = choice(list(self.assignment_dict))
				random_key_complement = random_key * -1
				self.assignment_dict[random_key] = not self.assignment_dict[random_key]
				self.assignment_dict[random_key_complement] = not self.assignment_dict[random_key_complement]

			else:

				max_variable_list = self.gen_max_var_list()

				random_var = choice(max_variable_list)
				random_var_complement = random_var * -1
				# print("Actual max clauses: " + str(max_clauses_satisfied))
				# print("Variable: " + str(rand) + " max_clause_satisfied: " + str(max_clauses_satisfied))

				self.assignment_dict[random_var] = not self.assignment_dict[random_var]
				self.assignment_dict[random_var_complement] = not self.assignment_dict[random_var_complement]

	def gen_max_var_list(self, clause_set = None):
		max_variable_list = []
		num_clauses_to_variable = []
		max_variable_list = []
		visited_set = set()
		max_clauses_satisfied = 0
		variable_list = self.index_to_variable_dict if clause_set == None else clause_set

		#First loop to get max # clauses satisfied
		for variable in variable_list:
			variable_complement = variable * -1
			if variable not in visited_set and variable_complement not in visited_set:
				(current_variable, satisfied_clauses) = self.satisfy_clauses(variable_arg=variable)
				num_clauses_to_variable.append((current_variable, satisfied_clauses))
				if satisfied_clauses > max_clauses_satisfied:
					max_clauses_satisfied = satisfied_clauses
				visited_set.add(variable)	
				visited_set.add(variable_complement)

		print("max clauses satisfied: " + str(max_clauses_satisfied))
		# print("num clauses to variable: " + str(num_clauses_to_variable))
		# print("visited set: " + str(visited_set))
		#Second loop to get all variables with max # clauses satisfied
		for variable_clause_tuple in num_clauses_to_variable:
			if variable_clause_tuple[1] == max_clauses_satisfied:
				max_variable_list.append(variable_clause_tuple[0])

		# print("max variable list: " + str(max_variable_list))
		return max_variable_list

	def random_assignment(self):
		for variable in self.variable_to_index_dict:
			if(int(variable) > 0):
				rand_int = randint(0, 1)
				variable_complement = '-' + str(variable)
				self.assignment_dict[self.variable_to_index_dict[variable]] = (False if rand_int == 0 else True)
				self.assignment_dict[self.variable_to_index_dict[variable_complement]] = (False if rand_int == 0 else True)

	def flip_var(self, var):
		complement_var = var * -1
		self.assignment_dict[var] = not self.assignment_dict[var]
		self.assignment_dict[complement_var] = not self.assignment_dict[complement_var]

	#if len(args) == 0, just return boolean
	def satisfy_clauses(self, variable_arg=None, walksat=False):

		valid_assignment = True  
		#Used for walkset
		unsatisfied_constraint_variable_list = []

		#Used to check # clauses satisfied by a variable
		#variable is passed in, flip the value
		if variable_arg != None:
				self.flip_var(variable_arg)

		#Check for clause satisfaction
		satisfied_clauses = 0
		for clause_set in self.clause_constraint_list:
			is_positive_clause = False
			positive_true_count = 0
			negative_false_count = 0
			for variable in clause_set:
				# print("variable: " + str(variable))
				if variable > 0:
					is_positive_clause = True
					if self.assignment_dict[variable] == True:
						positive_true_count += 1
				elif variable < 0:
					if self.assignment_dict[variable] == False:
						negative_false_count += 1

			#If clause is not valid
			if (is_positive_clause and positive_true_count == 0) or (not is_positive_clause and negative_false_count == 0):
				valid_assignment = False

				#Add unsatisfied clause to set
				unsatisfied_constraint_variable_list.append(clause_set)
				if(variable_arg == None and walksat == False):
					return False

			#If the clause is successful, increment satisfied_clauses		
			else:
				satisfied_clauses += 1

		#Used to check num clauses satisfied by a variable
		#If variable was passed in, unflip the value to return to original value
		if variable_arg != None:
				self.flip_var(variable_arg)

		#If no variable passed and not for walksat, just return whether 
		#clauses are satisfied or not
		if variable_arg == None and walksat == False:
			return True

		#If used in walksat, pass whether clauses are satisfied and 
		#a randomly chosen invalid clause set
		elif walksat == True:
			if (valid_assignment):
				return valid_assignment, None
			else:
				return valid_assignment, choice(unsatisfied_constraint_variable_list)

		#If variable is passed in, return tuple (variable, number clauses satisfied)
		elif variable_arg != None:
			return variable_arg, satisfied_clauses

	def walksat(self):
		self.random_assignment()
		threshold = 0.7
		self.solution_attempts += 1
		satisfy_clauses_tuple = self.satisfy_clauses(walksat = True)
		is_satisfied = satisfy_clauses_tuple[0]
		clause_set = satisfy_clauses_tuple[1]
		# print("is satisfied: " + str(is_satisfied))
		# print("CLAUSE SET: " + str(clause_set))
		while not is_satisfied:
			self.solution_attempts += 1			
			# print(self.assignment_dict)
			random_flip = uniform(0, 1)

			if random_flip > threshold:
				random_key = choice(list(self.assignment_dict))
				random_key_complement = random_key * -1
				self.assignment_dict[random_key] = not self.assignment_dict[random_key]
				self.assignment_dict[random_key_complement] = not self.assignment_dict[random_key_complement]

			else:
				max_variable_list = self.gen_max_var_list(clause_set)

				random_var = choice(max_variable_list)
				random_var_complement = random_var * -1
				# print("Actual max clauses: " + str(max_clauses_satisfied))
				# print("Variable: " + str(rand) + " max_clause_satisfied: " + str(max_clauses_satisfied))

				self.assignment_dict[random_var] = not self.assignment_dict[random_var]
				self.assignment_dict[random_var_complement] = not self.assignment_dict[random_var_complement]

			(is_satisfied, clause_set) = self.satisfy_clauses(walksat = True)
		return self.assignment_dict
					

	
	def write_solution(self, file_path):
		print("Number of solution attempts: " + str(self.solution_attempts))
		file = open(file_path, "w")
		visited_set = set()
		for var in self.assignment_dict:
			var_complement = var * -1
			if var not in visited_set and var_complement not in visited_set:

				positive_var = max(var_complement, var)

				#If value of var is False				
				if not self.assignment_dict[positive_var]:
					negated_val = "-" + self.index_to_variable_dict[positive_var]
					file.write(negated_val + "\n")

				#If value of var is True
				else:
					positive_val = self.index_to_variable_dict[positive_var]
					file.write(positive_val + "\n")

				visited_set.add(var)
				visited_set.add(var_complement)
		file.close()


	def init_variable_to_index_dict(self):
		file = open(self.file_path, "r")
		positive_index = 1
		negative_index = -1
		variable_index_dict = {}
		for line in file:
			for variable in line.strip().split(' '):

				#If considering a negative variable
				if variable[0] == '-': 
					if variable not in variable_index_dict:
						variable_complement = variable[1:]
						variable_index_dict[variable] = negative_index
						variable_index_dict[variable_complement] = positive_index
						negative_index -= 1
						positive_index += 1

				#If considering a positive variable		
				else:
					if variable not in variable_index_dict:
						variable_complement = '-' + variable
						variable_index_dict[variable] = positive_index
						variable_index_dict[variable_complement] = negative_index
						positive_index += 1
						negative_index -= 1
		file.close()
		return variable_index_dict

	def init_index_to_variable_dict(self):
		index_to_variable_dict = {}
		for key in self.variable_to_index_dict:
			value = self.variable_to_index_dict[key]
			index_to_variable_dict[value] = key
		return index_to_variable_dict


	def init_clause_constraint_set(self):
		file = open(self.file_path, "r")
		clause_list = []
		for line in file:
			clause_dict = set()
			for variable in line.strip().split(' '):
				clause_dict.add(self.variable_to_index_dict[variable])
			clause_list.append(clause_dict)
		return clause_list
			


test = SAT("./one_cell.cnf")
# test.GSAT()
test.walksat()
print("SOLUTION ATTEMPTS: " + str(test.solution_attempts))
print(test.assignment_dict)
test.write_solution("./test.sol")
