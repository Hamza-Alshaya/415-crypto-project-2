import sys
sys.path.append('./')
#testing hashing, hashing should provide the same value on same data.

from cryptography.md5 import md5_hash
input_string = 'string for hashing'
print("Test1: consistent hashing")
hash1 = md5_hash(input_string)
hash2 = md5_hash(input_string)
if (hash1 == hash2):
    print('hash is consistent')
else:
    print('hash is NOT consistent')

print('\n\nTest2: Testing the avalanche effect of the hash function')
#test the "avalanche effect" of the hash function
input_string_1 = 'string for hashing'
input_string_2 = 'string for Hashing'
print(f"{input_string_1} = {md5_hash(input_string_1)}\n{input_string_2} = {md5_hash(input_string_2)}")

#hashing an empty string test
print('\n\nTest3:')
print(f"Hashing an empty string: {md5_hash('')}")

#hashing a non-string object
myObject = (1, 2, 'something')

print('\n\nTest3: Hashing a non-string object')
try:
    print(f"Hashing a non-string object: {md5_hash(myObject)}")
except:
    print(f"ERROR: could not hash a non-string object")
    
print('\n\nTest4: Hashing a large string.')
large_hash_input = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
large_hash_result = md5_hash(large_hash_input)
print(f"resulting hash: {large_hash_result}")
      