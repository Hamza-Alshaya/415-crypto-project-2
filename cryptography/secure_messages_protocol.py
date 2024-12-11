import sys
sys.path.append('./')
from cryptography.asymmetric import generate_rsa_keys, rsa_encrypt, rsa_decrypt
from cryptography.diffie_hellman import generator, agreement
from cryptography.symmetric import generate_64b_key
from cryptography.md5 import md5_hash

from Crypto.Util.number import getPrime

import socket
import pickle

def secure_messages_protocol(connection_socket: socket.socket, name):
#########################
    #alice's logic
    if (name == 'alice'):
        from cryptography.variables import alice_dh_secret, alice_dh_public, alice_public_pair, alice_private_pair
        alice_public_pair, alice_private_pair = generate_rsa_keys()

        print(f'sent public key: {alice_public_pair}')
        connection_socket.sendall(pickle.dumps(alice_public_pair))

        bob_pk = pickle.loads(connection_socket.recv(2048))
        print(f'received public_key: {bob_pk}')

        alice_dh_secret = getPrime(12)
        alice_dh_public = generator(alice_dh_secret)

        connection_socket.sendall(pickle.dumps(alice_dh_public))
        bob_pdh = pickle.loads(connection_socket.recv(2048))
        alice_sc = agreement(bob_pdh, alice_dh_secret)
        print('shared secret = ', alice_sc)
        
        alice_sym_key = generate_64b_key(str(alice_sc))
        print('generated key = ', alice_sym_key)

        return alice_sym_key
        



        pass
#########################
    #bob's logic
    if (name == 'bob'):
        alice_pk = pickle.loads(connection_socket.recv(2048))
        print(f'received public_key: {alice_pk}')

        from cryptography.variables import bob_dh_secret, bob_dh_public, bob_public_pair, bob_private_pair
        bob_public_pair, bob_private_pair = generate_rsa_keys()

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

        return bob_sym_key



        pass
#########################