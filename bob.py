import socket
from threading import Thread

import util.config_file
import console.commands
from console.terminal_emulator import terminal_emulator
from cryptography.symmetric import encrypt_des, decrypt_des
import cryptography.variables

#handle receiving messages here
def handle_receive(sock):
    try:
        while True:
            message = sock.recv(2048).decode()
            message = decrypt_des(message, cryptography.variables.bob_sym_key)
            if not message:
                break
            print(f"\nAlice: {message}")
            
    #gracefully exit and close socket when main thread closes the connection
    except (ConnectionAbortedError, OSError):
        print("READING THREAD: Connection closed by main thread, exiting.")
    finally:
        sock.close()
        util.config_file.bob_connection_flag = False      #set flag to false to alert the main thread that the connetion was closed



def main():
    #client socket connection routine
    sock = socket.socket()
    sock.connect((util.config_file.alice_ip, util.config_file.alice_port))
    print('Connection established with Alice.')
    util.config_file.bob_connection_flag = True

    ##################################
    #SYMMETRIC KEY EXCHANGE PROTOCOL:
    from cryptography.secure_messages_protocol import secure_messages_protocol
    cryptography.variables.bob_sym_key = secure_messages_protocol(sock, name='bob')
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
            sock.send(encrypt_des(message, cryptography.variables.bob_sym_key).encode())
        else:
            print('Server closed the connection.')
            break

if __name__ == '__main__':
    main()