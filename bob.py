import pickle
import socket
import requests
from threading import Thread

import util.config_file
import console.commands
from console.terminal_emulator import terminal_emulator

from console.format_util import tf_presets
colorize = tf_presets.colorize

from cryptography.symmetric import encrypt_des, decrypt_des
import cryptography.variables
from cryptography.asymmetric import generate_rsa_keys, rsa_encrypt, rsa_decrypt

from cryptography.md5 import md5_hash

import console.bob_config

#handle receiving messages here
def handle_receive(sock):
    try:
        while True:
            message_object = pickle.loads(sock.recv(2048))
            
            if (message_object['encrypted'] == False):
                message = message_object['message_content']
                print(f"\n{colorize('WARNING:', tf_presets.danger)} Received message is not encrypted!")
            else:
                message = decrypt_des(message_object['message_content'], cryptography.variables.bob_sym_key)

            if not message:
                print(colorize('ERROR: couldn\'t properly parse received message...', tf_presets.danger))
            
            
            message_hash = md5_hash(message)
            message_decrypted_hash = rsa_decrypt(message_object['message_hash_encrypted'],cryptography.variables.alice_public_pair)
            if not message_decrypted_hash:
                print(colorize('ERROR: couldn\'t properly parse encrypted hashed message...', tf_presets.danger))
            
            hash_match_flag = False
            if (message_hash == message_decrypted_hash):
                hash_match_flag = True
            
            else:
                print(colorize("\nNot a hash match", tf_presets.danger))
                print(f'encrypted hash:\t{rsa_decrypt(message_object["message_hash_encrypted"],cryptography.variables.alice_public_pair)}')
                print(f'normal hash:\t"{message_hash}"')
                print(f'md5(message):\t"{md5_hash(message)}"')
                print(f'message: \"{message}\"')
                
                
            if (message_object['encrypted'] == False):
                print(f"\n{colorize('Alice:', tf_presets.red)} {message}")
            else:
                if (console.bob_config.enable_decryption):
                    print(f"\n{colorize('Alice:', tf_presets.blue)} {message}")
                else:
                    print(f"\n{colorize('Alice:', tf_presets.blue)} {message_object['message_content']}")
                    
            
    #gracefully exit and close socket when main thread closes the connection
    except (ConnectionAbortedError, OSError):
        print("READING THREAD: Connection closed by main thread, exiting.")
    finally:
        sock.close()
        util.config_file.bob_connection_flag = False      #set flag to false to alert the main thread that the connetion was closed



def main():
    #generate key pair
    cryptography.variables.bob_public_pair, cryptography.variables.bob_private_pair = generate_rsa_keys()
    #issue a certificate before connecting.
    csr_obj = {
        'csr':
            {
                'id':"bob",
                'public_key': str(cryptography.variables.bob_public_pair)
            }
    }
    request_message = requests.post('http://127.0.0.1:42021/certificates', json=csr_obj)
    request_message_json = request_message.json()
    if request_message_json['status'] == 'success':
        print(colorize('-=-=-=-=-=-CA HAS SUCCESSFULLY CREATED A CERTIFICATE-=-=-=-=-=-', tf_presets.green))
    elif request_message_json['status'] == 'error':
        print(colorize(f'-=-=-=-=-=-ERROR: CA FAILED TO CREATE A CERTIFICATE:-=-=-=-=-=-\n{request_message_json["message"]}', tf_presets.danger))
        exit(1)
        
    #client socket connection routine
    sock = socket.socket()
    sock.connect((util.config_file.alice_ip, util.config_file.alice_port))
    print('Connection established with Alice.')
    util.config_file.bob_connection_flag = True

    ##################################
    #SYMMETRIC KEY EXCHANGE PROTOCOL:
    from cryptography.secure_messages_protocol import secure_messages_protocol
    cryptography.variables.bob_sym_key, cryptography.variables.alice_public_pair = secure_messages_protocol(sock, name='bob')
    ##################################

    #start the thread for receiving messages
    receive_thread = Thread(target=handle_receive, args=(sock,))
    receive_thread.start()
    
    #main thread will send messages here
    while True:
        message = terminal_emulator(name='Bob')
        if (message == f'/{console.commands.EXIT_COMMAND}'):
            sock.close()
            break
        
        elif (message == '/'):
            continue
        
        #check flag before sending to avoid errors
        elif util.config_file.bob_connection_flag:
            message = message.rstrip()
            if (message == ""):
                continue
            
            if (console.bob_config.emulate_false_hash):
                from random import randint
                message_hash = md5_hash(str(randint(1, 10000)))
            else:
                message_hash = md5_hash(message)
                
            if (console.bob_config.enable_encryption):
                message = encrypt_des(message,cryptography.variables.bob_sym_key)
            
            #create the message object:
            message_object ={
                'message_content': message,
                'message_hash_encrypted': rsa_encrypt(message_hash,cryptography.variables.bob_private_pair),
                'encrypted': console.bob_config.enable_encryption
            }
            
            sock.sendall(pickle.dumps(message_object))
        else:
            print('Alice closed the connection.')
            break

if __name__ == '__main__':
    main()