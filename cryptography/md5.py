import sys
sys.path.append('./')
from util.util import hex_to_string, string_to_hex, hex2bin, bin2hex, dec2bin, binary_add
from cryptography.md5_resources import K, SHIFT_AMOUNT, A, B, C, D

#funciton that rotates bits to the left
def rotate_bits(num, rot):
    return ((num << rot) | (num >> (32 - rot))) & 0xFFFFFFFF

#F funciton. Used during all stages, behavior changes after every 16 iteration
def F(b, c, d, i):
    if i >= 0 and i < 16:
        return (b & c) | ((~b) & d)
    elif i >= 16 and i < 32:
        return (b & d) | (c & (~d))
    elif i >= 32 and i < 48:
        return b ^ c ^ d
    elif i >= 48 and i < 64:
        return c ^ (b | (~d))

#value that adds a, F(X), text block, and K[i], then shifts the value to SHIFT_AMOUNT[i]. K and SHIFT_AMOUNT have fixed values.
def redBox(value, i):
    return rotate_bits(binary_add(value,K[i],0,bits=32), SHIFT_AMOUNT[i])

#function that hashes one single block, returns a,b,c,d
def md5_hash_one_block(block, A, B, C, D):
    #split the block into 16 words, each having 32 bits
    divided_words = []
    for i in range(16):
        divided_words.append(block[:32])
        block = block[32:]


    a = A
    b = B
    c = C
    d = D

    for i in range(64):
        #permutation
        a_p = d
        c_p = b
        d_p = c

        #print(f'i = {i}\nA TYPE:{type(a)}\nF(B,C,D,I) TYPE:{type(F(b,c,d,i))}\nDIVIDEDWORDTYPE:{type(int(divided_words[i%16],2))}\n\n')
        if i >= 0 and i < 16:
            b_p = redBox(binary_add(a, F(b,c,d,i), int(divided_words[i%16],2)),i)
        elif i >= 16 and i < 32:
            b_p = redBox(binary_add(a, F(b,c,d,i), int(divided_words[(5*i+1)%16],2)),i)
        elif i >= 32 and i < 48:
            b_p = redBox(binary_add(a, F(b,c,d,i), int(divided_words[(3*i+5)%16],2)),i)
        elif i >= 48 and i < 64:
            b_p = redBox(binary_add(a, F(b,c,d,i), int(divided_words[(7*i)%16],2)),i)

        a = a_p
        b = b_p
        c = c_p
        d = d_p

    return a, b, c, d


#main hashing function, takes any arbitrary string
def md5_hash(input_string):
    #store the length of message in binary, pad it with 0 on the left to have a 64 bit representation for the message size
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
    

    #convert string to hex value
    hex_string = string_to_hex(input_string)
    #print(f'hex string = {hex_string}')
    for i in range (0, len(hex_string)):
        binary_string = f'{binary_string}' + hex2bin(hex_string[i]) #first argument is of formatted string in case we want to add spacers for debugging
        pass
    #print('length before padding: ', len(binary_string))
    #print(f'hex to bin =\t {binary_string}')

    #make sure the block size is congruent to 448 modulo 512
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

    #add the 64 bit representation of size to have a 512 compatible block
    binary_string = binary_string+length_in_binary
    
    #split each block to 512 to properly apply hashing
    blocks_of_512 = []
    while (len(binary_string) > 0):
            blocks_of_512.append(binary_string[:512])
            binary_string = binary_string[512:]
    #print('after appending size:\t', binary_string)
    #print('% 512 ==', len(binary_string) % 512)
    a = A
    b = B
    c = C
    d = D

    #iterate through each block and hash it, PRESERVING the values of a,b,c,d
    for block in blocks_of_512:
        a, b, c, d =  md5_hash_one_block(block, a, b, c, d)

    #return the hash in hex format, 32 letters long (128 bits)
    return  str(hex(a)[2:] + hex(b)[2:] + hex(c)[2:] + hex(d)[2:]).upper()
    #if (len(input_string.encode('ascii'))*8 % 512 == 448):
    #    input_string = input_string + '1'
    #    pass


#for testing
#print(md5_hash('This is a string that is probably longer than 512 bits or something idk'))