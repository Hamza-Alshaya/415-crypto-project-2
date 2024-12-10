import sys
sys.path.append('./')

from cryptography.des_resources import S_BOX, IP, E, P, IP_INVERSE, PC_1, BITS_ROTATION, COMPRESSION_PERMUTATION
from util.util import dec2bin, bin2dec, bin2hex, hex2bin, hex2char, char2hex

##########################################
# constant DES tables were provided by wikipedia's page 'DES supplementary material':   https://en.wikipedia.org/wiki/DES_supplementary_material
# This code is HEAVILY inspired from Aditya Jain's implementation on GeeksforGeeks :    https://www.geeksforgeeks.org/data-encryption-standard-des-set-1/
# The implementation was then further enhanced to accept larger plain texts (TODO)
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


#main encryption function
def encrypt(plain_text, round_keys_binary, round_keys):
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
	return cipher_text


plain_text = "123456ABCD132536"
key = "AABB09182736CCDD"

# --hex to binary
key = hex2bin(key)

#getting 56 bit key from 64 bit using the parity bits
key = permute(key, PC_1, 56)

#splitting
left = key[0:28] # round_keys_binar
right = key[28:56] # round_keys in hexadecimal

round_keys_binary = []
round_keys = []
for i in range(0, 16):
	#shifting the bits by nth shifts by checking from shift table
	left = shift_left(left, BITS_ROTATION[i])
	right = shift_left(right, BITS_ROTATION[i])

	#combination of left and right string
	combine_str = left + right

	#compression of key from 56 to 48 bits
	round_key = permute(combine_str, COMPRESSION_PERMUTATION, 48)

	round_keys_binary.append(round_key)
	round_keys.append(bin2hex(round_key))

'''
print("original text:", plain_text)
print("Encryption")
cipher_text = bin2hex(encrypt(plain_text, round_keys_binary, round_keys))
print("Cipher Text : ", cipher_text)

print("Decryption")
rkb_rev = round_keys_binary[::-1]
rk_rev = round_keys[::-1]
text = bin2hex(encrypt(cipher_text, rkb_rev, rk_rev))
print("Plain Text : ", text)
'''

'''
#test hex char2hex and hex2char
character = 'H'
print(f'character = {character}')
to_hex = char2hex(character)
print(f'to hex = {to_hex}')
print(f'Back to character: {hex2char(to_hex)}')
'''