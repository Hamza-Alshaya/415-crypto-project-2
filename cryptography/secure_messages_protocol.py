import sys
sys.path.append('./')
from cryptography.asymmetric import generate_rsa_keys, rsa_encrypt, rsa_decrypt
from cryptography.diffie_hellman import generator, agreement
from cryptography.symmetric import generate_64b_key
from cryptography.md5 import md5_hash

from console.format_util import tf_presets
colorize = tf_presets.colorize

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
        print(colorize("-=-=-=-=-=RECEIVED CA\'S PUBLIC KEY-=-=-=-=-=", tf_presets.green))
        
        #print('CA PUBLIC KEY = ', ca_pk)
    else:
        print(colorize('FAILED TO RETRIEVE CERTIFICATE\'S PUBLIC KEY, ABORTING.',tf_presets.danger))
        exit(1)
    
    
    request_response_cert = requests.get(f'http://127.0.0.1:42021/certificates/{id}')
    request_response_cert_json = request_response_cert.json()
    if request_response_cert_json['status'] == 'success':
        decrypted_hash = rsa_decrypt(request_response_cert_json['certificate']['signature'], ca_pk)
        hashed_public_key = md5_hash(str(public_key))
        
        if (decrypted_hash == hashed_public_key):
            print(colorize('-=-=-=-=-=PUBLIC KEY\'S HASH MATCHES CA\'s ENCRYPTED HASH!-=-=-=-=-=', tf_presets.green))
        else:
            print(colorize('-=-=-=-=-=PUBLIC KEY\'S HASH HAS FAILED TO MATCH WITH CA\'s ENCRYPTED HASH, ABORTING...-=-=-=-=-=', tf_presets.danger))
            exit(0)
        
        #print('DECRYPTED SIGNATURE =\t', decrypted_hash)
        #print(f"{id.upper()}\'S HASHED KEY:\t {hashed_public_key}\n\n\n")
        
        pass
    else:
        print(colorize('FAILED TO RETRIEVE CERTIFICATE FROM CA, ABORTING.', tf_presets.danger))
        exit(1)
    
    #print(request_response_cert_json)
    pass

def secure_messages_protocol(connection_socket: socket.socket, name):
#########################
    #alice's logic
    if (name == 'alice'):
        from cryptography.variables import alice_dh_secret, alice_dh_public, alice_public_pair, alice_private_pair

        #sending public key
        print(colorize('Public key sent to Bob.',tf_presets.green))
        connection_socket.sendall(pickle.dumps(alice_public_pair))

        #Receiving public key
        bob_pk = pickle.loads(connection_socket.recv(2048))
        print(colorize('Reveived Bob\'s public key.',tf_presets.green))
        
        #authenticate the key with the CA
        authenticate_with_CA('bob', bob_pk)

        #Selecting secret key a for Diffie-Hellman, then calculating the public value A
        alice_dh_secret = getPrime(12)
        alice_dh_public = generator(alice_dh_secret)

        #send the public value A
        connection_socket.sendall(pickle.dumps(alice_dh_public))
        
        #Receive the public value B from Bob and generate the agreed key
        bob_pdh = pickle.loads(connection_socket.recv(2048))
        alice_sc = agreement(bob_pdh, alice_dh_secret)
        print(colorize(f'shared secret = {alice_sc}', tf_presets.blue))
        
        #generate a symmetric key from the hash of the shared key
        alice_sym_key = generate_64b_key(str(alice_sc))
        print(colorize(f'generated key = {alice_sym_key}', tf_presets.blue))

        return alice_sym_key, bob_pk
        



        pass
#########################
    #bob's logic
    if (name == 'bob'):
        
        #receiving public key from Alice
        alice_pk = pickle.loads(connection_socket.recv(2048))
        print(colorize('Reveived Alice\'s public key.',tf_presets.green))

        
        #authenticate the key with the CA
        authenticate_with_CA('alice', alice_pk)
        
        from cryptography.variables import bob_dh_secret, bob_dh_public, bob_public_pair, bob_private_pair

        #send public key
        print(colorize('Public key sent to Alice.',tf_presets.green))
        connection_socket.sendall(pickle.dumps(bob_public_pair))

        #Selecting secret key b for Diffie-Hellman, then calculating the public value B
        bob_dh_secret = getPrime(12)
        bob_dh_public = generator(bob_dh_secret)

        #receive the public value A from Alice, calculate the shared secret, then send Bob's public value B
        alice_pdh = pickle.loads(connection_socket.recv(2048))
        bob_sc = agreement(alice_pdh, bob_dh_secret)
        connection_socket.sendall(pickle.dumps(bob_dh_public))
        print(colorize(f'shared secret = {bob_sc}', tf_presets.blue))

        #generate a symmetric key from the hash of the shared key
        bob_sym_key = generate_64b_key(str(bob_sc))
        print(colorize(f'generated key = {bob_sym_key}', tf_presets.blue))

        return bob_sym_key, alice_pk



        pass
#########################