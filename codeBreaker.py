letters = {0: ' ', 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k', 12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v', 23: 'w', 24: 'x', 25: 'y', 26: 'z'}

numbers = {' ': 0, 'a': 1, 'c': 3, 'b': 2, 'e': 5, 'd': 4, 'g': 7, 'f': 6, 'i': 9, 'h': 8, 'k': 11, 'j': 10, 'm': 13, 'l': 12, 'o': 15, 'n': 14, 'q': 17, 'p': 16, 's': 19, 'r': 18, 'u': 21, 't': 20, 'w': 23, 'v': 22, 'y': 25, 'x': 24, 'z': 26}

import random
from fractions import Fraction

def convert_to_words(matrix):
	to_return = ''
	for i in matrix:
		try:
			to_return += letters[int(abs(round(i)))]
		except:
			return ''
	return to_return

def convert_to_numbers(string):
	to_return = []
	for i in string:
		to_return.append(numbers[i.lower()])
	return to_return

def two_column(matrix):
	matrix = list(matrix)
	if len(matrix) % 2 != 0:
		matrix.append(0)
	
	m1 = []
	m2 = []
	for i in range(0, len(matrix)):
		if i % 2 == 0:
			m1.append(matrix[i])
		else:
			m2.append(matrix[i])
	
	to_return = []
	for i in range(0, len(m1)):
		if m2[i]:
			to_return.append([m1[i], m2[i]])
		else:
			to_return.append([m1[i], 0])
	return to_return

def one_column(matrix):
	matrix = list(matrix)
	to_return = []
	for row in matrix:
		for element in row:
			to_return.append(element)
	return to_return

def multRows(row1, row2):
	addition = 0
	for i in range(0, len(row2)):
		addition += row1[i] * row2[i]
	return addition

def get_column(matrix, index):
	to_return = []
	for row in matrix:
		to_return.append(row[index])
	return to_return

def multiply(m1, m2):
	answer = []
	count = -1
	for row1 in m1:
		count += 1
		to_add = []
		for row2count in range(0,len(m2)):
			to_add.append(multRows(row1, get_column(m2, row2count)))
		answer.append(to_add)
	return answer

def encode(matrix, key):
	return one_column(multiply(two_column(matrix), key))

def discriminate(k):
	return k[0][0] * k[1][1] - k[0][1] * k[1][0]

def generate_key():
	a = random.randint(0,9)
	b = random.randint(0,9)
	c = random.randint(0,9)
	d = random.randint(0,9)
	return [[a, b], [c, d]]

def inverse(matrix):
	#a = matrix[0][0]
	#b = matrix[0][1]
	#c = matrix[1][0]
	#d = matrix[1][1]
	disc = discriminate(matrix)
	if disc == 0:
		return False
	inv = [[matrix[1][1]/disc,-1 * matrix[1][0]/disc], [-1 * matrix[0][1]/disc,matrix[0][0]/disc]]
	return inv

def test(matrix, key):
	if not key:
		return False
	return multiply(two_column(matrix),key)

def main():
	try:
		answer = int(input("Would you like to convert (1) letters to code or (2) decode? "))
	except:
		print("Error: enter 1 or 2")
		return 1
	
	if answer == 1:
		matrix = convert_to_numbers(input("Enter passphrase: "))
		print("Letters --> Numbers: ",matrix)
		cont = False
		while True:
			key = generate_key()
			if key != False:
				break
		actual_key = [[key[0][0], key[1][0]], [key[0][1], key[1][1]]]
		print("Key:",actual_key)
		inverted_key = inverse(key)
		print("Inverse of Key:",inverted_key)
		en = encode(matrix, inverted_key)
		for i in range(0, len(en)):
			en[i] = Fraction(en[i]).limit_denominator(82)
		print("Encoded Version:", end=" ")
		count = 0
		for i in en:
			if count == len(en) - 1:
				print(i)
			else:
				print(i,end=" ")
				count += 1
		#print("Encoded Version:",en)
		return 0
	elif answer != 2:
		print("Error: enter 1 or 2")
		return 1
	
	code = input("Enter code numbers separated by a space: ")
	if ',' in code:
		elements = code.split(', ')
	else:
		elements = code.split(' ')
	count = -1
	for i in elements:
		count += 1
		if '/' in i:
			to_divide = i.split('/')
			elements[count] = float(to_divide[0]) / float(to_divide[1])
		elif '-' == i[:1]:
			to_neg = i[1:]
			elements[count] = -1 * float(to_neg)
		else:
			elements[count] = float(i)

	tests = 0
	start = 0
	end = 9
	count = 0
	keys = []
	for a in range(start,end):
		for b in range(start,end):
			for c in range(start,end):
				for d in range(start,end):
					t = test(elements,[[a,b],[c,d]])
					if t:
						words = convert_to_words(one_column(t))
						if words != "":
							count += 1
							print(str(count) + '.',words)
							keys.append([[a,b],[c,d]])
	print("\n"*3)
	new_count = 0
	for k in keys:
		new_count += 1
		print(str(new_count) + '.',k[0],k[1])


if __name__ == '__main__':
	main()
