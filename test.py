from cryptography.asymmetric import generate_rsa_keys, rsa_encrypt, rsa_decrypt
from util.util import encode_string, decode_string

#TESTING the algorithm on text

encryption, decryption = generate_rsa_keys()
text = 'Big message to test the keys or something lol'
encrypted = rsa_encrypt(text, encryption)
print('encrypted text: ', encrypted)
decrypted = rsa_decrypt(encrypted, decryption)
print('decrypted text: ', decrypted) 