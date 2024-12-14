import sys
import time
sys.path.append('./')

from cryptography.md5 import md5_hash
from cryptography.symmetric import generate_64b_key, encrypt_des, decrypt_des

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import hashlib


input_file = './tests/512kb_file.txt'
with open(input_file, 'r') as myFile:
    half_mb_string = myFile.read()
symmetric_key = generate_64b_key('any item works here, even objects')

#####################################################################
#MD5
#####################################################################
print('\nMD5 Test:')
print('testing speed for hashing a 512KB input:')

print('\n----==============LIBRARY IMPLEMENTATION:==============----')
time_start = time.time()
hashlib.md5(half_mb_string.encode()).hexdigest()
time_end = time.time()
print(f'Time taken for hashing: {time_end - time_start} seconds')
print('----==========:END OF LIBRARY IMPLEMENTATION:==========----')

print('\n----==============LOCAL IMPLEMENTATION:==============----')
time_start = time.time()
hash_value = md5_hash(half_mb_string)
time_end = time.time()
print(f'Time taken for hashing: {time_end - time_start} seconds')
print('----==========:END OF LOCAL IMPLEMENTATION:==========----')


#####################################################################
#DES
#####################################################################
print('\nDES Test:')
print('testing speed of encrypting and decrypting a 512KB input:')

print('\n----==============LIBRARY IMPLEMENTATION:==============----')
key = half_mb_string.encode()[:8]
cipher = DES.new(key, DES.MODE_CBC)

time_start = time.time()
ciphertext = cipher.encrypt(pad(half_mb_string.encode(), DES.block_size))
time_end = time.time()
print(f'Time taken for encryption: {time_end - time_start} seconds')

time_start = time.time()
iv = ciphertext[:8]
ciphertext = ciphertext[8:]
cipher = DES.new(key, DES.MODE_CBC, iv=iv)
decrypted = unpad(cipher.decrypt(ciphertext), DES.block_size)
time_end = time.time()
print(f'Time taken for decryption: {time_end - time_start} seconds')
print('----==========:END OF LIBRARY IMPLEMENTATION:==========----')


print('\n----==============LOCAL IMPLEMENTATION:==============----')
time_start = time.time()
encrypted_file = encrypt_des(half_mb_string, symmetric_key)
time_end = time.time()
print(f'Time taken for encryption: {time_end - time_start} seconds')

time_start = time.time()
decypted_file = decrypt_des(encrypted_file, symmetric_key)
time_end = time.time()
print(f'Time taken for decryption: {time_end - time_start} seconds')
print('----==========:END OF LOCAL IMPLEMENTATION:==========----')