import sys
sys.path.append('./')
from util.util import hex_to_string, string_to_hex, hex2bin, bin2hex, dec2bin

A = 0x67452301
B = 0xefcdab89
C = 0x98badcfe
D = 0x10325476

def md5_hash(input_string):
    binary_string = ""
    length_of_original_message = len(input_string)
    length_in_binary = dec2bin(length_of_original_message)
    if len(length_in_binary) < 64:
        for i in range(64-len(length_in_binary)):
            length_in_binary = '0'+length_in_binary

    #print('message: ', input_string)
    #print('length: ', length_of_original_message)
    #print('length in binary: ', length_in_binary)
    #print('length in binary:', len(length_in_binary))
    

    hex_string = string_to_hex(input_string)
    #print(f'hex string = {hex_string}')
    for i in range (0, len(hex_string)):
        binary_string = f'{binary_string }' + hex2bin(hex_string[i]) #first argument is of formatted string in case we want to add spacers for debugging
        pass
    #print('length before padding: ', len(binary_string))
    #print(f'hex to bin =\t {binary_string}')
    if (len(binary_string.encode('ascii')) % 512 != 448):
        binary_string = binary_string+'1'
        padding_value = 448 - (len(binary_string) % 512)
        if (padding_value > 0):
            for i in range(padding_value):
                binary_string = binary_string+'0'
        elif (padding_value < 0):
            for i in range(512+padding_value):
                binary_string = binary_string+'0'
    
    #print('after padding:\t', binary_string)
    #print('length: ', len(binary_string))
    #print('% 512 ==', len(binary_string) % 512)

    binary_string = binary_string+length_in_binary
    #print('after appending size:\t', binary_string)
    #print('% 512 ==', len(binary_string) % 512)

        


    #if (len(input_string.encode('ascii'))*8 % 512 == 448):
    #    input_string = input_string + '1'
    #    pass

md5_hash('ABC')