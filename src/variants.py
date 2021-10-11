class Variant:

	def __init__(self):
		self.name = ''
		self.original_sequence = ''
		self.variant_sequence = ''
		self.instructions_list = []

	def upload(self, original_sequence):
		self.original_sequence = original_sequence

	def generate(self, instructions_list, name):
		self.name = name
		self.variant_sequence = ''

		previous_index = 0
		total = 0

		print(self.original_sequence[28279:28282])

		for instruction in instructions_list:

			# if deletion
			if instruction[-4:].upper() == "_DEL":

				start_index = int(instruction.split('_')[0])-1
				end_index = int(instruction.split('_')[1])-1

				self.variant_sequence += self.original_sequence[previous_index:start_index]

				previous_index = end_index 

			elif instruction[-4:].upper() == "_SUB":

				start_index = int(instruction.split('_')[0])-1

				print(start_index)

				print(instruction.split('_'))

				self.variant_sequence += self.original_sequence[previous_index:start_index]
				self.variant_sequence += instruction.split('_')[2]

				previous_index = start_index + len(instruction.split('_')[2])

				print(previous_index)


			# if substitution
			else:

				# index-1 because the nucleotide notaion starts at index 1
				# while in Python notaion starts at index 0
				index = int(instruction[1:-1])-1

				total += index-previous_index

				self.variant_sequence += self.original_sequence[previous_index:index-1] + instruction[-1]

				previous_index = index

		self.variant_sequence += self.original_sequence[previous_index:]

		total+= len(self.original_sequence)-previous_index

		print(total)

	def save_to_txt(self, filepath):

		print("Original length:", len(self.original_sequence))
		print("Variant length:", len(self.variant_sequence))

		file = open(filepath, "w")
		file.write(self.variant_sequence)
		file.close()
