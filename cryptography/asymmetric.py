#RSA

from Crypto.Util import number

import sys
sys.path.append('./')
import util.config_file
import util.util

#returns public, private keys
def generate_rsa_keys():
    #step 1: get 2 random prime numbers of specified size
    p = number.getPrime(util.config_file.rsa_key_size//2)
    q = number.getPrime(util.config_file.rsa_key_size//2)

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

def rsa_encrypt(string, key_pair):
    text_converted = util.util.encode_string(string)
    text_encrypted = pow(text_converted, key_pair[0], key_pair[1])
    return text_encrypted

def rsa_decrypt(string, key_pair):
    text_decrypted = pow(string, key_pair[0], key_pair[1])
    text_decoded = util.util.decode_string(text_decrypted)
    return text_decoded

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