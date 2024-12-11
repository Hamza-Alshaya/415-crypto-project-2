'''
#TODO:
    - Create a function that splits a hex padded string into 8 bytes (64 bits) section/blocks, possibly into an array (internal function)
    - Create a function that applies the encryption on each section/block from the array above, then returns the encrypted string (as one string, not an array)
    - Create a function that applies the decryption on each section/block. Takes an encrypted string, splits into sections of 8 bytes, decrypts each and concat
    By then we would be finally done with symmetric algorithms!
'''

import sys
sys.path.append('./')

from cryptography.des_resources import S_BOX, IP, E, P, IP_INVERSE, PC_1, BITS_ROTATION, COMPRESSION_PERMUTATION
from util.util import dec2bin, bin2dec, bin2hex, hex2bin, hex2char, char2hex

##########################################
# constant DES tables were provided by wikipedia's page 'DES supplementary material':   https://en.wikipedia.org/wiki/DES_supplementary_material
# This code is HEAVILY inspired from Aditya Jain's implementation on GeeksforGeeks :    https://www.geeksforgeeks.org/data-encryption-standard-des-set-1/
# The implementation was then further enhanced to accept larger plain texts split into chunks (TODO)
##########################################

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
def padder(input_string):
    #print("length = ", len(input_string))
    if(len(input_string)%8 !=0):
        mod_value = len(input_string) % 8
        #print('mod value = ', mod_value)
        number_of_pads = 8-mod_value
        for i in range (number_of_pads):
            input_string = input_string + " "
        #print("new length = ", len(input_string))
    return input_string

def string_block_splitter(input_string):
	padded_string = padder(input_string)
	blocks_list = []
	for i in range(len(padded_string)//8):
		one_block = padded_string[:8]
		padded_string = padded_string[8:]
		blocks_list.append(one_block)
	#print('blocks = ', blocks_list)
	return blocks_list

def encrypt_des(input_string):
	blocks_list = string_block_splitter(input_string)
	for block in blocks_list:
		pass