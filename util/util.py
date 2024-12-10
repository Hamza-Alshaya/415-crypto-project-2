#convert a string to encoded ascii bytes, then convert those bytes to an integer
def encode_string(input_string):
    encoded_bytes = input_string.encode('ascii')
    encoded_integer = int.from_bytes(encoded_bytes, byteorder='big')
    return encoded_integer

#reverse operation: convert an integer to bytes, then decode the bytes to an ascii string
def decode_string(input_encoded_integer):
    decoded_bytes = input_encoded_integer.to_bytes((input_encoded_integer.bit_length() + 7) // 8, byteorder='big')
    decoded_message = decoded_bytes.decode('ascii')
    return decoded_message


def hex2bin(s):
	mp = {'0': "0000",
		'1': "0001",
		'2': "0010",
		'3': "0011",
		'4': "0100",
		'5': "0101",
		'6': "0110",
		'7': "0111",
		'8': "1000",
		'9': "1001",
		'A': "1010",
		'B': "1011",
		'C': "1100",
		'D': "1101",
		'E': "1110",
		'F': "1111"}
	bin = ""
	for i in range(len(s)):
		bin = bin + mp[s[i]]
	return bin

# Binary to hexadecimal conversion


def bin2hex(s):
	mp = {"0000": '0',
		"0001": '1',
		"0010": '2',
		"0011": '3',
		"0100": '4',
		"0101": '5',
		"0110": '6',
		"0111": '7',
		"1000": '8',
		"1001": '9',
		"1010": 'A',
		"1011": 'B',
		"1100": 'C',
		"1101": 'D',
		"1110": 'E',
		"1111": 'F'}
	hex = ""
	for i in range(0, len(s), 4):
		ch = ""
		ch = ch + s[i]
		ch = ch + s[i + 1]
		ch = ch + s[i + 2]
		ch = ch + s[i + 3]
		hex = hex + mp[ch]

	return hex


# Binary to decimal conversion
def bin2dec(binary):

	binary1 = int(binary)
	decimal, i, n = 0, 0, 0
	while(binary1 != 0):
		dec = binary1 % 10
		decimal = decimal + dec * pow(2, i)
		binary1 = binary1//10
		i += 1
	return decimal

# Decimal to binary conversion


def dec2bin(num):
	res = bin(num).replace("0b", "")
	if(len(res) % 4 != 0):
		div = len(res) / 4
		div = int(div)
		counter = (4 * (div + 1)) - len(res)
		for i in range(0, counter):
			res = '0' + res
	return res

#character to hexadecimal
def char2hex(character):
    return bin2hex(dec2bin(ord(character)))

#hexadecimal to character
def hex2char(hex_input):
    return chr(bin2dec(hex2bin(hex_input)))

def string_to_hex(input):
    padded_string = padder(input)
    hex_string = ""
    for i in range(len(padded_string)):
        character_hex = char2hex(padded_string[i])
        hex_string = hex_string + character_hex
    #print('string to hex: ', hex_string)
    return hex_string

def hex_to_string(input):
    string_output = ""
    for i in range(0, len(input), 2):
        character = hex2char(input[i]+input[i+1])
        string_output = string_output + character
    #print('normal_string = ', string_output)
    return string_output