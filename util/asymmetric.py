#RSA

from Crypto.Util import number
import base64

#convert a string to encoded utf-8 bytes, then convert those bytes to an integer
def encode_string(input_string):
    encoded_bytes = input_string.encode('ascii')
    encoded_integer = int.from_bytes(encoded_bytes, byteorder='big')
    return encoded_integer

#reverse operation: convert an integer to bytes, then decode the bytes to an ascii string
def decode_string(input_encoded_integer):
    decoded_bytes = input_encoded_integer.to_bytes((input_encoded_integer.bit_length() + 7) // 8, byteorder='big')
    decoded_message = decoded_bytes.decode('ascii')
    return decoded_message

def generate_rsa_keys():
    #step 1: get 2 random prime numbers of specified size
    p = number.getPrime(1024)
    q = number.getPrime(1024)

    #step 2: calculate n, totient phi(n), and choose a public e
    n = p*q
    tot_n = (p-1)*(q-1)
    e = 65537

    #step 3: calculate private exponent d such that d is the modular inverse of e % phi(n)
    d = pow(e, -1, tot_n)

    #step 4: create public and private key pairs
    encryption = (e, n)        #public  key pair for encryption
    decryption = (d, n)        #private key pair for decryption
    
    return encryption, decryption

'''
#TESTING the algorithm on text

encryption, decryption = generate_rsa_keys()
text = 'Big message to test the keys or something lol'
#ord() to convert
text_converted = encode_string(text)

print(f'Plain text: {text_converted}')

text_encrypted = pow(text_converted, encryption[0], encryption[1])
print(f"encrypted: {text_encrypted}",)

text_decrypted = pow(text_encrypted, decryption[0], decryption[1])
print(f"decrypted: {decode_string(text_decrypted)}")
'''