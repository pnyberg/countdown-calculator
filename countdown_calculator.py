'''
	main method
	currently takes a list of numbers and a target and prints the info about the calculation
'''
def solve_for_target(numbers, target):
	max_number_of_parenthesis = len(numbers) - 1
	result = naive_check_for_additative_solution(numbers, target, [], 0, max_number_of_parenthesis)

	result = remove_unnecessary_parenthesises(result)

	print(numbers)
	print(target)
	print(result)

def remove_unnecessary_parenthesises(result):
	starting_index = -1
	stopping_index = -1

	index = 0
	while index < len(result) - 1:
		if result[index] == '(':
			starting_index = index
		elif result[index] == ')':
			if result[starting_index-1] == '(' and result[index+1] == ')': 
				result = result[0:starting_index] + result[starting_index+1:index] + result[index+1:len(result)]
				starting_index = -1
				stopping_index = -1
				index = -1

		index += 1

	return result

def naive_check_for_additative_solution(usable_list, target, used_list, open_parenthesis, number_of_allowed_parenthesis_left):
	# calculates the value of the 
	if len(used_list) > 4 and used_list[0] == '(' and used_list[2] == '+' and used_list[4] == ')' and \
			(used_list[1] == 3 and used_list[3] == 5 or used_list[1] == 5 and used_list[3] == 3) and \
			len(usable_list) > 0:
		print(used_list)
		print("Usable list: " + str(usable_list))
	sum = calculate_sum(used_list)

	if sum == target:
		return used_list

	for i in range(len(usable_list)):
		active_number = usable_list[i]
		copied_usable_list = usable_list[0:i] + usable_list[i+1:len(usable_list)]

		if has_last_element(used_list) and (last_element_was_digit(used_list) or last_element_was_ending_parenthesis(used_list)):
			#print(str(used_list[-1]) + " ----- adding/subtracting/multiplying/dividing ----- " + str(used_list))

			# check when adding
			res_when_adding = naive_check_for_additative_solution(usable_list, target, used_list + ["+"], open_parenthesis, number_of_allowed_parenthesis_left)
			if res_when_adding != []:
				return res_when_adding
			# check when subtracting
			res_when_subtracting = naive_check_for_additative_solution(usable_list, target, used_list + ["-"], open_parenthesis, number_of_allowed_parenthesis_left)
			if res_when_subtracting != []:
				return res_when_subtracting
			# check when multiplying
			res_when_multiplying = naive_check_for_additative_solution(usable_list, target, used_list + ["*"], open_parenthesis, number_of_allowed_parenthesis_left)
			if res_when_multiplying != []:
				return res_when_multiplying
			# check when diving
			res_when_dividing = naive_check_for_additative_solution(usable_list, target, used_list + ["/"], open_parenthesis, number_of_allowed_parenthesis_left)
			if res_when_dividing != []:
				return res_when_dividing

		if not has_last_element(used_list) or last_element_was_operator(used_list) or last_element_was_starting_parenthesis(used_list):
			#print(str(used_list[-1]) + " ----- start-parenthesis / number / nothing ----- " + str(used_list))

			# check when starting parenthesis
			if number_of_allowed_parenthesis_left > 0:
				res_with_start_parenthesis = naive_check_for_additative_solution(usable_list, target, used_list + ["("], open_parenthesis+1, number_of_allowed_parenthesis_left-1)
				if res_with_start_parenthesis != []:
					return res_with_start_parenthesis

			# check when using a number
			res_with_number = naive_check_for_additative_solution(copied_usable_list, target, used_list + [active_number], open_parenthesis, number_of_allowed_parenthesis_left-1)
			if res_with_number != []:
				return res_with_number

		if has_last_element(used_list) and (last_element_was_digit(used_list) or last_element_was_ending_parenthesis(used_list)):
			#print(str(used_list[-1]) + " ----- end-parenthesis ----- " + str(used_list))

			# check when ending parenthesis
			if open_parenthesis > 0:
				res_with_end_parenthesis = naive_check_for_additative_solution(usable_list, target, used_list + [")"], open_parenthesis-1, number_of_allowed_parenthesis_left)
				if res_with_end_parenthesis != []:
					return res_with_end_parenthesis

			# check when not used at all
			res_with_nothing = naive_check_for_additative_solution(copied_usable_list, target, used_list, open_parenthesis, number_of_allowed_parenthesis_left-1)
			if res_with_nothing != []:
				return res_with_nothing

	return []

def has_last_element(used_list):
	return len(used_list) > 0

def last_element_was_digit(used_list):
	last_element = str(used_list[-1])

	return last_element.isdigit()

def last_element_was_operator(used_list):
	last_element = str(used_list[-1])

	return last_element == '+' or \
			last_element == '-' or \
			last_element == '*' or \
			last_element == '/'

def last_element_was_starting_parenthesis(used_list):
	last_element = str(used_list[-1])

	return last_element == '('

def last_element_was_ending_parenthesis(used_list):
	last_element = str(used_list[-1])

	return last_element == ')'

def calculate_sum(expression_list):
	sum = calculate_sum_helper(0, len(expression_list), expression_list)

	return sum

def calculate_sum_helper(start_index, less_than_bound, expression_list):
	active_parenthesises = 0
	# first solve parenthesises
	index = start_index
	while index < less_than_bound:
		if expression_list[index] == '(':
			if active_parenthesises == 0:
				new_start_index = index+1
			active_parenthesises += 1
		elif expression_list[index] == ')':
			active_parenthesises -= 1 	# no need to check < 0, because it cannot be
			if active_parenthesises == 0:
				parenthesis_sum = calculate_sum_helper(start_index+1, index, expression_list)
				expression_list_length = len(expression_list)
				expression_list = expression_list[0:start_index] + [parenthesis_sum] + expression_list[index+1:len(expression_list)]
				less_than_bound = less_than_bound - expression_list_length + len(expression_list) # recalculating the less_than_bound
				index = index - expression_list_length + len(expression_list)

		index += 1

	# secondly, solve multiplikation and division
	index = start_index
	while index < less_than_bound:
		if expression_list[index] == '*':
			if (index+1) == less_than_bound:
				return None
			first_number = expression_list[index-1]
			second_number = expression_list[index+1]
			if not str(first_number).isdigit() or not str(second_number).isdigit():
				return None
			product = first_number * second_number
			expression_list = expression_list[0:index-1] + [product] + expression_list[index+2:len(expression_list)]
			index -= 1
			less_than_bound -= 2
		elif expression_list[index] == '/':
			if (index+1) == less_than_bound:
				return None
			first_number = expression_list[index-1]
			second_number = expression_list[index+1]
			if not str(first_number).isdigit() or not str(second_number).isdigit():
				return None
			quotient = first_number * second_number
			expression_list = expression_list[0:index-1] + [quotient] + expression_list[index+2:len(expression_list)]
			index -= 1
			less_than_bound -= 2

		index += 1

	# thirdly, solve adding and subtracting
	index = start_index
	while index < less_than_bound:
		if expression_list[index] == '+':
			if (index+1) == less_than_bound:
				return None
			first_number = expression_list[index-1]
			second_number = expression_list[index+1]
			if not str(first_number).isdigit() or not str(second_number).isdigit():
				return None
			sum_value = first_number + second_number
			expression_list = expression_list[0:index-1] + [sum_value] + expression_list[index+2:len(expression_list)]
			index -= 1
			less_than_bound -= 2
		elif expression_list[index] == '-':
			if (index+1) == less_than_bound:
				return None
			first_number = expression_list[index-1]
			second_number = expression_list[index+1]
			if not str(first_number).isdigit() or not str(second_number).isdigit():
				return None
			difference = first_number - second_number
			expression_list = expression_list[0:index-1] + [difference] + expression_list[index+2:len(expression_list)]
			index -= 1
			less_than_bound -= 2

		index += 1

	if len(expression_list) == 0:
		return None
	return expression_list[start_index]

numbers = [3, 5, 7]
target = 14

solve_for_target(numbers, target)