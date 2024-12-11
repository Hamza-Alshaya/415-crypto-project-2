import sys
sys.path.append('./')
from cryptography.asymmetric import generate_rsa_keys, rsa_encrypt, rsa_decrypt
from cryptography.diffie_hellman import generator, agreement
from cryptography.symmetric import generate_64b_key
from cryptography.md5 import md5_hash

from Crypto.Util.number import getPrime

import socket
import pickle
import requests     

def authenticate_with_CA(id, public_key):
    #get CA's public key:
    request_response_key = requests.get(f'http://127.0.0.1:42021/key')
    request_response_key_json = request_response_key.json()
    if request_response_key_json['status'] == 'success':
        ca_pk = tuple(request_response_key_json['public_key'])
        print('\n\n-=-=-=-=-=RECEIVED CA\'S PUBLIC KEY-=-=-=-=-=')
        
        #print('CA PUBLIC KEY = ', ca_pk)
    else:
        print('FAILED TO RETRIEVE CERTIFICATE\'S PUBLIC KEY, ABORTING.')
        exit(1)
    
    
    request_response_cert = requests.get(f'http://127.0.0.1:42021/certificates/{id}')
    request_response_cert_json = request_response_cert.json()
    if request_response_cert_json['status'] == 'success':
        decrypted_hash = rsa_decrypt(request_response_cert_json['certificate']['signature'], ca_pk)
        hashed_public_key = md5_hash(str(public_key))
        
        if (decrypted_hash == hashed_public_key):
            print('-=-=-=-=-=PUBLIC KEY\'s HASH HAS MATCHED WITH CA\'s ENCRYPTED HASH!-=-=-=-=-=')
        else:
            print('-=-=-=-=-=PUBLIC KEY\'s HASH HAS FAILED TO MATCH WITH CA\'s ENCRYPTED HASH, ABORTING...-=-=-=-=-=')
            exit(0)
        
        print('DECRYPTED SIGNATURE =\t', decrypted_hash)
        print(f"{id.upper()}\'S HASHED KEY:\t {hashed_public_key}\n\n\n")
        
        pass
    else:
        print('FAILED TO RETRIEVE CERTIFICATE FROM CA, ABORTING.')
        exit(1)
    
    #print(request_response_cert_json)
    pass

def secure_messages_protocol(connection_socket: socket.socket, name):
#########################
    #alice's logic
    if (name == 'alice'):
        from cryptography.variables import alice_dh_secret, alice_dh_public, alice_public_pair, alice_private_pair

        print(f'sent public key: {alice_public_pair}')
        connection_socket.sendall(pickle.dumps(alice_public_pair))

        bob_pk = pickle.loads(connection_socket.recv(2048))
        print(f'received public_key: {bob_pk}')
        authenticate_with_CA('bob', bob_pk)

        alice_dh_secret = getPrime(12)
        alice_dh_public = generator(alice_dh_secret)

        connection_socket.sendall(pickle.dumps(alice_dh_public))
        bob_pdh = pickle.loads(connection_socket.recv(2048))
        alice_sc = agreement(bob_pdh, alice_dh_secret)
        print('shared secret = ', alice_sc)
        
        alice_sym_key = generate_64b_key(str(alice_sc))
        print('generated key = ', alice_sym_key)

        return alice_sym_key, bob_pk
        



        pass
#########################
    #bob's logic
    if (name == 'bob'):
        alice_pk = pickle.loads(connection_socket.recv(2048))
        print(f'received public_key: {alice_pk}')
        authenticate_with_CA('alice', alice_pk)
        
        from cryptography.variables import bob_dh_secret, bob_dh_public, bob_public_pair, bob_private_pair

        print(f'sent public key: {bob_public_pair}')
        connection_socket.sendall(pickle.dumps(bob_public_pair))

        bob_dh_secret = getPrime(12)
        bob_dh_public = generator(bob_dh_secret)

        alice_pdh = pickle.loads(connection_socket.recv(2048))
        bob_sc = agreement(alice_pdh, bob_dh_secret)
        connection_socket.sendall(pickle.dumps(bob_dh_public))
        print('shared secret = ', bob_sc)

        bob_sym_key = generate_64b_key(str(bob_sc))
        print('generated key = ', bob_sym_key)

        return bob_sym_key, alice_pk



        pass
#########################