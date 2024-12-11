import sys
sys.path.append('./')

from cryptography.des_resources import S_BOX, IP, E, P, IP_INVERSE, PC_1, BITS_ROTATION, COMPRESSION_PERMUTATION
from util.util import dec2bin, bin2dec, bin2hex, hex2bin, hex2char, char2hex, padder, string_to_hex, hex_to_string
from cryptography.md5 import md5_hash
##########################################
# constant DES tables were provided by wikipedia's page 'DES supplementary material':   https://en.wikipedia.org/wiki/DES_supplementary_material
# This code is HEAVILY inspired from Aditya Jain's implementation on GeeksforGeeks :    https://www.geeksforgeeks.org/data-encryption-standard-des-set-1/
# The implementation was then further enhanced to accept larger plain texts split into chunks (TODO)
##########################################

#generate a 64 bit key given a seed
def generate_64b_key(input_string):
	hashed_input = md5_hash(input_string)
	return hashed_input[:16]


#permute function to rearrange the bits
def permute(k, arr, n):
	permutation = ""
	for i in range(0, n):
		permutation = permutation + k[arr[i] - 1]
	return permutation


#shifting the bits towards left by n
def shift_left(k, nth_shifts):
	s = ""
	for i in range(nth_shifts):
		for j in range(1, len(k)):
			s = s + k[j]
		s = s + k[0]
		k = s
		s = ""
	return k

#calculating xor of two strings of binary number a and b
def xor(a, b):
	ans = ""
	for i in range(len(a)):
		if a[i] == b[i]:
			ans = ans + "0"
		else:
			ans = ans + "1"
	return ans


#key Generation Functions
def generate_round_keys(key):
    #permute the key to 56 bits
    key = permute(key, PC_1, 56)

    #splitting into two halves
    left = key[0:28]
    right = key[28:56]

    round_keys_binary = []
    round_keys = []

    #generating the 16 keys
    for i in range(0, 16):
        #shifting the bits
        left = shift_left(left, BITS_ROTATION[i])
        right = shift_left(right, BITS_ROTATION[i])

        #combine halves and compress to 48 bits
        combine_str = left + right
        round_key = permute(combine_str, COMPRESSION_PERMUTATION, 48)

        round_keys_binary.append(round_key)
        round_keys.append(bin2hex(round_key))

    return round_keys_binary, round_keys

#main encryption function
#encrypt one single block
def encrypt(plain_text, key, decrypt=False):

	#generate keys
	round_keys_binary = 0
	
	#change behavior in case the decryption methods called this function
	if (decrypt):
		#decrypt sends the reversed round key binary instead of the actual key, so interpret that value as rkb instead.
		round_keys_binary = key
	else:
		key_binary = hex2bin(key)
		round_keys_binary, round_keys = generate_round_keys(key_binary)
	

	plain_text = hex2bin(plain_text)

	#initial Permutation IP
	plain_text = permute(plain_text, IP, 64)
	#print("After initial permutation", bin2hex(plain_text))

	#splitting
	left = plain_text[0:32]
	right = plain_text[32:64]
	for i in range(0, 16):
		#expansion D-box: expanding the 32 bits data into 48 bits
		right_expanded = permute(right, E, 48)

		#XOR roundKey[i] and right_expanded
		xor_x = xor(right_expanded, round_keys_binary[i])

		#s-boxes: substituting the value from s-box table by calculating row and column
		S_BOX_str = ""
		for j in range(0, 8):
			row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
			col = bin2dec(
				int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
			val = S_BOX[j][row][col]
			S_BOX_str = S_BOX_str + dec2bin(val)

		#straight D-box: After substituting rearranging the bits
		S_BOX_str = permute(S_BOX_str, P, 32)

		#XOR left and S_BOX_str
		result = xor(left, S_BOX_str)
		left = result

		#swapper
		if(i != 15):    #don't swap at the last permutation (final permutation stage)
			left, right = right, left
		#print("Round ", i + 1, " ", bin2hex(left),
		#	" ", bin2hex(right), " ", round_keys[i])

	#combination
	combine = left + right

	#final permutation: final rearranging of bits to get cipher text
	cipher_text = permute(combine, IP_INVERSE, 64)
	return bin2hex(cipher_text)

#decrypt one single block
def decrypt(cipher_text, key):
	key_binary = hex2bin(key)
	round_keys_binary, round_keys = generate_round_keys(key_binary)

	rkb_rev = round_keys_binary[::-1]
	decrypted_text = encrypt(cipher_text, rkb_rev, decrypt=True)
	return decrypted_text

'''
#TEST PROGRAM
plain_text = "123456ABCD132536"
key = "AABB09182736CCDD"
print("Original Text:", plain_text)

#encrypt
cipher_text = encrypt(plain_text, key)
print("Cipher Text :", cipher_text)

#decrypt
decrypted_text = decrypt(cipher_text, key)

print("Decrypted Text :", decrypted_text)
'''

'''
#test hex char2hex and hex2char
character = 'H'
print(f'character = {character}')
to_hex = char2hex(character)
print(f'to hex = {to_hex}')
print(f'Back to character: {hex2char(to_hex)}')
'''

#split a string into a list of blocks of size N, size is 8 by default
#size can be modified depending on context (dealing with hex vs strings)
def string_block_splitter(input_string, size=8):
	padded_string = padder(input_string)
	blocks_list = []
	for i in range(len(padded_string)//size):
		one_block = padded_string[:size]
		padded_string = padded_string[size:]
		blocks_list.append(one_block)
	#print('blocks = ', blocks_list)
	return blocks_list


#encrypt whole text into a hex string
def encrypt_des(input_string, key):
	blocks_string_list = string_block_splitter(input_string)
	encrypted_blocks = []
	output_hex = ""

	for string in blocks_string_list:
		encrypted_block = encrypt(string_to_hex(string, padding_value=8), key)
		#encrypted_blocks.append(encrypted_block)
		output_hex = output_hex + encrypted_block

	#print('encrypted blocks = ', encrypted_blocks)
	return output_hex

#decrypt a hex string into a string
def decrypt_des(input_string, key):
	hex_blocks_list = string_block_splitter(input_string, size=16)
	decrypted_blocks = []
	output_string = ""
	for string in hex_blocks_list:
		decrypted_block = hex_to_string(decrypt(string, key))
		#decrypted_blocks.append(decrypted_block)
		output_string = output_string+decrypted_block
	#print('decrypted blocks = ', decrypted_blocks)
	return output_string.rstrip()
	
'''
#MAIN DRIVER TESTER: can accept any string
key = "AABB09182736CCDD"
encrypted_text = encrypt_des('test string that is quite long', key)
print(encrypted_text)

decrypted_text = decrypt_des(encrypted_text, key)
print(decrypted_text)
'''