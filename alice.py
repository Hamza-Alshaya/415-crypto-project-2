import util.config_file
import cryptography.variables
import console.commands
from console.terminal_emulator import terminal_emulator

import socket
import pickle

from threading import Thread
from cryptography.symmetric import encrypt_des, decrypt_des

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
            print(f"\nBob: {message}")
            
    #gracefully exit and close socket when main thread closes the connection
    except (ConnectionAbortedError, OSError):
        print("READING THREAD: Connection closed by main thread, exiting.")
    finally:
        connection.close()
        util.config_file.alice_connection_flag = False    #set flag to false to alert the main thread that the connetion was closed


def main():
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
    cryptography.variables.alice_sym_key = secure_messages_protocol(connection, name='alice')
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
            message_object ={
                'message_content': encrypt_des(message,cryptography.variables.alice_sym_key),
                'message_hash_encrypted': encrypt_des(md5_hash(message),cryptography.variables.alice_sym_key)
            }
            
            connection.sendall(pickle.dumps(message_object))
        else:
            print('Bob closed the connection.')
            break


if __name__ == '__main__':
    main()