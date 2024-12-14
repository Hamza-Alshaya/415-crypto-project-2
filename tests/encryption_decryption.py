import sys
sys.path.append('./')

from cryptography.asymmetric import rsa_encrypt, rsa_decrypt, generate_rsa_keys
from cryptography.symmetric import encrypt_des, decrypt_des, generate_64b_key

input_string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."

#RSA tests
print("RSA test 1:")
#test encrypting and decrypting a text. It should return the same value:

public_key, private_key = generate_rsa_keys()
encrypted_rsa_text = rsa_encrypt(input_string, public_key)
decrypted_rsa_text = rsa_decrypt(encrypted_rsa_text, private_key)
if (input_string == decrypted_rsa_text):
    print('the decrypted text matches the original')
else:
    print('the decrypted text does NOT match the original')
    print(f'"{decrypted_rsa_text}"\n"{input_string}')

print('\nRSA Test 2:')
print('Encrypting and decrypting an empty string: ')
encrypted_empty_string = rsa_encrypt("", public_key)
decrypted_empty_string = rsa_decrypt(encrypted_empty_string, public_key)
if (decrypted_empty_string == ""):
    print('The decrypted empty string matches the original.')
else:
    print('The decrypted empty string does NOT the original.')
    
print('\nRSA Test 3:')
print('Attempt to encrypt and decrypt a large input:')
large_rsa_input = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
try:
    large_rsa_encrypt = rsa_encrypt(large_rsa_input, public_key)
except:
    print(f"ERROR: encountered an exception during text encryption:")
try:
    large_rsa_decrypt = rsa_decrypt(large_rsa_encrypt, private_key)
    if large_rsa_input == large_rsa_decrypt:
        print('The decrypted ciphertext matches the original string')
    else:
        print('The decrypted ciphertext does NOT match the original string')
        print(f'"{large_rsa_input}"\n"{large_rsa_decrypt}')        
except:
    print(f"ERROR: encountered an exception during text decryption:")
    
print('\nRSA Test 4:')
print('Attempt to tamper with the encrypted text before decrypting:')

rsa_test4_input = 'hello'
rsa_test4_encrypt = rsa_encrypt(rsa_test4_input, private_key)
rsa_test4_encrypt = rsa_test4_encrypt-10
try:
    rsa_test4_decrypt = rsa_decrypt(rsa_test4_encrypt, public_key)
    print('Original text:', rsa_test4_input)
    print('Decrypted text =', rsa_test4_decrypt)
except:
    print('ERROR: encountered an error during decrypting the tampered text.')
    

#DES test
print("\n===================================================")
#test encrypting and decrypting a text. It should return the same value:
print("DES test1:")
symmetric_key = generate_64b_key('any item works here, even objects')
encrypted_des = encrypt_des(input_string, symmetric_key)
decrypted_des = decrypt_des(encrypted_des, symmetric_key)
if (input_string == decrypted_des):
    print('the decrypted text matches the original')
else:
    print('the decrypted text does NOT match the original')
    print(f'"{decrypted_rsa_text}"\n"{input_string}')
    
    

print('\nDES Test 2:')
print('Encrypting and decrypting an empty string: ')
encrypted_empty_string = encrypt_des("", symmetric_key)
decrypted_empty_string = decrypt_des(encrypted_empty_string, symmetric_key)
if (decrypted_empty_string == ""):
    print('The decrypted empty string matches the original.')
else:
    print('The decrypted empty string does NOT the original.')
    
print('\nDES Test 3:')
print('Attempt to encrypt and decrypt a large input:')
large_des_input = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
try:
    large_des_encrypt = encrypt_des(large_des_input, symmetric_key)
    large_des_decrypt = decrypt_des(large_des_encrypt, symmetric_key)
    if large_des_decrypt == large_des_input:
        print('The decrypted ciphertext matches the original string')
    else:
        print('The decrypted ciphertext does NOT match the original string')
except:
    print(f"ERROR: encountered an exception during text decryption:")


print('\nDES Test 4:')
print('Attempt to tamper with the encrypted text before decrypting:')
des_test5_input = 'hello'
des_test5_encrypt = encrypt_des(des_test5_input, symmetric_key)
des_test5_modified = des_test5_encrypt.replace('A', 'C')
des_test5_decrypt = decrypt_des(des_test5_modified, symmetric_key)
print(f'Original text = {des_test5_input}')
print(f'Decrypted text = {des_test5_decrypt}')


print('\nDES Test 5:')
print('Attempt to decrypt a text with an invalid key: ')
try:
    invalid_decryption = decrypt_des(encrypted_des, "ABGH")
except:
    print(f"ERROR: encountered an exception during text decryption:")
    
    
'''
print('\nDES Test6:')
print('testing speed of encrypting and decrypting a 512KB input:')
input_file = './tests/512kb_file.txt'
with open(input_file, 'r') as myFile:
    ten_mb_string = myFile.read()

import time
time_start = time.time()
encrypted_file = encrypt_des(ten_mb_string, symmetric_key)
time_end = time.time()
print(f'Time taken for encryption: {time_end - time_start} seconds')

time_start = time.time()
decypted_file = decrypt_des(encrypted_file, symmetric_key)
time_end = time.time()
print(f'Time taken for decryption: {time_end - time_start} seconds')
'''