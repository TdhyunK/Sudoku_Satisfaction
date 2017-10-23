class SAT:

	def __init__(self, cnf_path):
		self.file_path = cnf_path
		self.variable_to_index_dict = self.init_variable_to_index_dict()
		print(self.variable_to_index_dict)
		self.clause_constraint_list = self.init_clause_constraint_set()
		print(self.clause_constraint_list)

	def gst(self):	
		pass

	def walksat(self):
		pass

	def write_solution(self, file_path):
		pass

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
						variable_index_dict[variable] = negative_index
						negative_index -= 1

				#If considering a positive variable		
				else:
					if variable not in variable_index_dict:
						variable_index_dict[variable] = positive_index
						positive_index += 1
		file.close()
		return variable_index_dict


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
