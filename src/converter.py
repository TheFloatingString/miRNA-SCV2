dna_complements = {
	'A':'T',
	'C':'G',
	'T':'A',
	'G':'C'
}

rna_complements = {
	'A':'U',
	'C':'G',
	'U':'A',
	'G':'C'
}

def find_dna_complement(initial_dna):
	return ''.join([dna_complements[char] for char in initial_dna])

def find_rna_complement(initial_rna):
	return ''.join([rna_complements[char] for char in initial_rna])