import util.config_file
import cryptography.variables
import console.commands
from console.terminal_emulator import terminal_emulator

import socket
import pickle
import requests

from threading import Thread
from cryptography.symmetric import encrypt_des, decrypt_des
from cryptography.asymmetric import generate_rsa_keys, rsa_encrypt, rsa_decrypt

from cryptography.md5 import md5_hash


#handle receiving messages here
def handle_receive(connection):
    try:
        while True:
            message_object = pickle.loads(connection.recv(2048))
            message = decrypt_des(message_object['message_content'], cryptography.variables.alice_sym_key)
            if not message:
                print('ERROR: couldn\'t properly parse received message...' )
                break
            
            message_hash = md5_hash(message)
            message_decrypted_hash = rsa_decrypt(message_object['message_hash_encrypted'],cryptography.variables.bob_public_pair)
            if not message_decrypted_hash:
                print('ERROR: couldn\'t properly parse encrypted hashed message...' )
            
            if (message_hash == message_decrypted_hash):
                print('Hash match.')
            else:
                print("Not a hash match")
                print(f'encrypted hash:{rsa_decrypt(message_object["message_hash_encrypted"],cryptography.variables.alice_public_pair)}')
                print(f'normal hash: {message_hash}')
                print(f'md5(message): {md5_hash(message)}')
                print(f'message: \"{message}\"')
                exit(0)
            
            print(f"\nBob: {message}")
            
    #gracefully exit and close socket when main thread closes the connection
    except (ConnectionAbortedError, OSError):
        print("READING THREAD: Connection closed by main thread, exiting.")
    finally:
        connection.close()
        util.config_file.alice_connection_flag = False    #set flag to false to alert the main thread that the connetion was closed


def main():
    #generate key pair
    cryptography.variables.alice_public_pair, cryptography.variables.alice_private_pair = generate_rsa_keys()
    #issue a certificate before connecting.
    csr_obj = {
        'csr':
            {
                'id':"alice",
                'public_key': str(cryptography.variables.alice_public_pair)
            }
    }
    request_message = requests.post('http://127.0.0.1:42021/certificates', json=csr_obj)
    request_message_json = request_message.json()
    if request_message_json['status'] == 'success':
        print('-=-=-=-=-=-CA HAS SUCCESSFULLY CREATED A CERTIFICATE-=-=-=-=-=-')
    elif request_message_json['status'] == 'error':
        print(f'-=-=-=-=-=-ERROR: CA FAILED TO CREATE A CERTIFICATE:-=-=-=-=-=-\n{request_message_json["message"]}')
        exit(1)
        
    
    #server socket creation routine
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', util.config_file.alice_port))
    sock.listen(1)
    print('Alice is listening for a connection')
    
    connection, address = sock.accept()
    print(f'Connection established with Bob on address:{address}')
    util.config_file.alice_connection_flag = True
    
    ##################################
    #SYMMETRIC KEY EXCHANGE PROTOCOL:
    from cryptography.secure_messages_protocol import secure_messages_protocol
    cryptography.variables.alice_sym_key, cryptography.variables.bob_public_pair = secure_messages_protocol(connection, name='alice')
    ##################################

    #start a thread for receiving messages
    receive_thread = Thread(target=handle_receive, args=(connection,))
    receive_thread.start()
    
    #main thread sends messages
    while True:
        message = terminal_emulator(name='Alice')
        if (message == f'/{console.commands.EXIT_COMMAND}'):
            connection.close()
            break
        
        elif (message == '/'):
            continue
        
        #check flag before sending to avoid errors
        elif util.config_file.alice_connection_flag:
            #create the message object:
            message = message.rstrip()
            message_object ={
                'message_content': encrypt_des(message,cryptography.variables.alice_sym_key),
                'message_hash_encrypted': rsa_encrypt(md5_hash(message),cryptography.variables.alice_private_pair)
            }
            
            connection.sendall(pickle.dumps(message_object))
            #print(f'hashed message: {md5_hash(message)}')
        else:
            print('Bob closed the connection.')
            break


if __name__ == '__main__':
    main()