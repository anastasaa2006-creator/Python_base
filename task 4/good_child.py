test_cases = int(input())

def convert_list_to_int(lst):
	lst_int = []
	for lst_idx in range(len(lst)):
		lst_int.append(int(lst[lst_idx]))
	return lst_int

def compute_product(array_int):
	product = 1
	for array_idx in range(len(array_int)):
		product *= array_int[array_idx]
	return product

def add_one(lst, idx):
	lst[idx] += 1


for test_case_idx in range(test_cases):
	num_digit = int(input())
	array = input()
	array = array.split()
	array_int = convert_list_to_int(array)

	min_index = 0
	for i in range(len(array_int)):
		if array_int[i] < array_int[min_index]:
			min_index = i

	add_one(array_int, min_index)

	max_product = compute_product(array_int)

	print(max_product)