# Wanted more of an explanation of the Kasiski Method: 

# Referenced https://en.wikipedia.org/wiki/Kasiski_examination
# Referenced https://inventwithpython.com/hacking/chapter21.html

# How I employed the Kasiski Method 
# 1. Found repeating sequences of letters and the distance between them
# 2. Find the commmon factors of the distances received
# 3. See which factor(s) appear the most -- this is a possible key_length
# 4. Starting from the first letter, construct a string every 7 letters
# 5. Repeat this process with 2nd letter, 3rd letter, up to 7th letter
# 6. Shift these strings using keys and Caesar ciphers (specifically decrypt)
# 7. Perform a frequency analysis against the frequency of letters in English
#	text vs. the frequency in your shifted strings


# finds sets of repeating letters (3 characters long)
# and length between sequence reappearances in order to find key length
# key = pattern, value = list of lengths between sequence reappearances
def repeat_seq(code): 
	pattern_len = 3
	pattern_seq = {}

	# boundary case is length of code inputted - pattern length
	for char in range(0, (len(code) - pattern_len)): 
		# use splicing to get chunks of letters
		temp = code[char: (char + pattern_len)]

		# start at char + pattern_len to avoid double-counts
		for i in range((char + pattern_len), len(code) - pattern_len):
			if (temp == code[i: (i + pattern_len)]): 
				if (temp in pattern_seq): 
					# i - char = length between reappearances
					pattern_seq[temp].append(i - char)
				else: 
					pattern_seq[temp] = []
					pattern_seq[temp].append(i - char)

	return pattern_seq

# obtains all the factors of a number (factors are no smaller than 2 and
# no larger than 50)
def factors(num): 

	factor_list = []
	# to add to list, must append

	if (num > 2): 
		# assuming that key is between 2 and 50 characters long: 
		for i in range(2, 50):
			if (num % i == 0): 
				factor_list.append(i)
	return factor_list

# gets the factors with the most occurrences
def guess_key_length(num_dict): 
	max_list = []
	max_num = 0 

	for key, value in num_dict.iteritems(): 
		if (value > max_num): 
			max_num = value

	for key in num_dict:  
		if (num_dict[key] == max_num): 
			max_list.append(key)

	return max_list

# returns probably keylengths (as a list)
def get_key_length_list(code): 

	patterns = repeat_seq(code)
	factorization_dict = {}
	num_dict = {}

	for sequence, num_list in patterns.iteritems(): 
		for num in num_list:
			if not(num in factorization_dict): 
				factorization_dict[num] = factors(num)
	#print factorization_dict - prints out all the factors for the sequence numbers

	for number, factor_list in factorization_dict.iteritems(): 
		for factor in factor_list:
			if (factor in num_dict): 
				num_dict[factor] += 1
			else: 
				num_dict[factor] = 1
	# print "\n\n"
	# print num_dict -- prints out how many times factors appear 

	#print guess_key_length(num_dict)

	return guess_key_length(num_dict)


# Assuming the key is x letters long, using the Kasiski method, 
# we want get every xth letter of the string 

# gets the frequencies of letters in a string 
def get_frequencies(string): 
	freq_dict = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0,
	'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0,
	'q': 0, 'r': 0, 's': 0,'t': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 
	'z': 0}

	char_count = float(len(string))

	for key, freq in freq_dict.iteritems():
		freq_dict[key] = (string.count(key))/char_count

	return freq_dict

# want to perform frequency analysis on each shift
# compare variances to 

letter_freq = {'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 
'E': 0.12702, 'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06996,
 'J': 0.00153, 'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749,
  'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 
  'T': 0.09056, 'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150,
   'Y': 0.01974, 'Z': 0.00074}


# first get every 7th letter starting with the first letter
# next get every 7th letter starting with the second letter
# returns a string 
def get_ith_letter(code, first_index, shift): 

	code_len = len(code)

	string_list = []

	# j is incremented index (by shift) and based on first_index
	j = first_index

	#k is index of string
	k = 0

	for i in range(0, code_len):
		if (j < code_len):
			string_list.append(code[j])
			j += shift
		else: 
			break


	for a in range(0, len(string_list)): 
		new_string = ''.join(string_list)

	return new_string

letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 
'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Vigenere decryption 
def vigenere_dec(string, key):
	global letter_list
	key_list = list(key)

	str_len = len(string)

	#strings are immutable, so use list instead to change letters
	# initalize the list 
	temp_list = []

	for i in range(0, len(key_list)):
		key_list[i] = letter_list.index(key_list[i])

	j = 0

	for i in range(0, len(string)):
	
		temp_index = (letter_list.index(string[i]) - key_list[j]) % 26
		temp_list.append(letter_list[temp_index])
		j += 1
		
		if (j == len(key)): 
			j = 0

	temp_string = ''.join(temp_list)
	return temp_string


# individual string extracted from get_ith_letter as an input:
# returns a list of possible letters 

# gets the frequencies of the letters that occur in a string
def get_frequencies(string): 
	freq_dict = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0,
	'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0,
	'Q': 0, 'R': 0, 'S': 0,'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 
	'Z': 0}

	char_count = float(len(string))

	for key, freq in freq_dict.iteritems():
		freq_dict[key] = (string.count(key))/char_count

	return freq_dict

def freq_analysis(num1, num2): 
	# chi-square analysis: smallest number means least error 
	return ((num1 - num2)**2)/float(num2)

# prints a list of keys and their chi-square sums
def determine_letters(string):
	global letter_freq

	# dict stores the population variances of string based on key shift
	dict_1 = {}
	var_dict = {}
	chi_sum = 0.0

	for key in letter_freq: 

		# perform the decryption on a Caesar shift, key = 'a' then 'b' etc...
		dec_string = vigenere_dec(string, key)
		# get frequencies 
		dict_1 = get_frequencies(dec_string)

		for letter in dict_1: 
			chi_sum += freq_analysis(dict_1[letter], letter_freq[letter])

		print "Key and chi_sum", key, chi_sum, "\n"

		chi_sum = 0.0

		# numbers with the smallest chi_sum are the best possible keys
		# look at the print statements produced by this function


ciphertext = "ULPKXWRJUGCCQDLBVKVINLCTZEVOKNLYCWQLYTCRQBMYJASZDWWLMIKZEGLIMKLLCFIMVEZYGMIAPFWVJJBSALUKEZEAYJXETWWXRYZMCKUIDIAXGLVBIVPJUCGCQEAMRWSCEUIENXZFUNZIKIYVUEVPGKAHXKVWEGWFGWBSSNFQIZNGGVOLMTFZCPIVNWIWVHDPJMRMMMDSHURLQNZUIZVMWSNVYXWGSLZJYALKJVXXATFCEASZXSNZJRAPUOIDXGDMWYVWLLLUTJRNTVYEOMIWANPYEBLAHKZKZTLSRPXPPFNZXEBTGHRIHVZFLVKYLTSNZJRUZVYIIGZJHNFBVIAZSZIXMCKYTOWBSWXZNGQADCEZWWQEUKCIULLCTNGWXHOKZVANAYEXIIYVYCZGBCAWRGIVRAHVZVQYYGFYIZYULPKXWRJUGCCQDZYRQMTJTUJZHWYEUKCIULLCTVPBSWIITEVOUIDKYBPJMTDIVNWJIVGBTUYTMCXEGAIVTPTUUCBSZTLBDNEZPVYJDKVPVUIJYVOUIDKYBLLCFIETSSLUIIADSMJPQXEAIENQIVAHXNYKSSFXJVQEZGJCEZOLISMIIVAHGMEKEAWVWCIYQUUQIZDSLPDXQDLBVJVMEAWRGPGAGMJDFTPLISMIIVKOTCEAJKNVHFCEANZNMVQWUJDFTPLIUJWWMQUETOVZOHGMEKEAWRGQMLFMTMCXEGFFBCZPDUKZHBPUBEJPWRQBRNVITKYUVRCXTYIJJTPYUCDWAFWMKCIMWWWKMSVTUZIJRBTWLWJYVOSNZJRELKCEQSTGWXZIEKLKYZIXPPMHZOILDLUKZWESAWYLYMDLCFIILHZYKCIZCWKLDVQYYMLNTMNLYUXVQXAHRGWBZHLFQMLPLBVDVLPULPKXQZFEVTWBZDUNZRNZJWVHIVEAMLIGWYKNZOYBTGHRGXPPWZWVVOFWXKCEBEZCJDWIGAICVXQZFIWOLMCAAYOSNYGNSZMVRXIIXILEGCEXVQXAHROIWYWMVGJIDYCMZRQYLBVAMNEZUDZRLX"



print "Repeated 3-letter patterns:\n\n", repeat_seq(ciphertext)

# prints out repeated sequences

print "\n\nPredicted key lengths:", get_key_length_list(ciphertext)

# Obtain 7 character key_length


print "+++++++++++++++++++++++++++++++"


print "+++++++++++++++++++++++++++++++"

print "DETERMINE 1ST CHARACTER\n\n"
test_1 = get_ith_letter(ciphertext, 0, 7)
determine_letters(test_1)

# Key and chi_sum S 0.275329451451
# S has the smallest chi_sum, so it is the strongest possible character

print "+++++++++++++++++++++++++++++++"
print "DETERMINE 2ND CHARACTER\n\n"
test_2 = get_ith_letter(ciphertext, 1, 7)
determine_letters(test_2)

# Key and chi_sum U 0.238692037172

print "+++++++++++++++++++++++++++++++"
print "DETERMINE 3ND CHARACTER\n\n"
test_3 = get_ith_letter(ciphertext, 2, 7)
determine_letters(test_3)

# Key and chi_sum R 0.156375232466

print "+++++++++++++++++++++++++++++++"
print "DETERMINE 4TH CHARACTER\n\n"
test_4 = get_ith_letter(ciphertext, 3, 7)
determine_letters(test_4)

# Key and chi_sum V 0.267457003022

print "+++++++++++++++++++++++++++++++"
print "DETERMINE 5TH CHARACTER\n\n"
test_5 = get_ith_letter(ciphertext, 4, 7)
determine_letters(test_5)

# Key and chi_sum E 0.210903725896

print "+++++++++++++++++++++++++++++++"
print "DETERMINE 6TH CHARACTER\n\n"
test_6 = get_ith_letter(ciphertext, 5, 7)
determine_letters(test_6)

# Key and chi_sum I 0.154303656129

print "+++++++++++++++++++++++++++++++"
print "DETERMINE 7TH CHARACTER\n\n"
test_7 = get_ith_letter(ciphertext, 6, 7)
determine_letters(test_7)

# Key and chi_sum L 0.217563057365


print "++++++++++++++++++++++++++++++\n"


#SUCCESS!!!

print ciphertext, "\n\n"
print "TO\n\n"
print vigenere_dec(ciphertext, "SURVEIL")
