import dotenv
import util.commands
from util.terminal_emulator import terminal_emulator

import socket
from threading import Thread


#handle receiving messages here
def handle_receive(connection):
    try:
        while True:
            message = connection.recv(2048).decode()
            if not message:
                break
            print(f"Bob: {message}")
            
    #gracefully exit and close socket when main thread closes the connection
    except (ConnectionAbortedError, OSError):
        print("READING THREAD: Connection closed by main thread, exiting.")
    finally:
        connection.close()
        dotenv.alice_connection_flag = False


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', dotenv.alice_port))
    sock.listen(1)
    print('Alice is listening for a connection')
    
    connection, address = sock.accept()
    print(f'Connection established with Bob on address:{address}')
    dotenv.alice_connection_flag = True
    
    # Start a thread for receiving messages
    receive_thread = Thread(target=handle_receive, args=(connection,))
    receive_thread.start()
    
    # Main thread sends messages
    while True:
        message = terminal_emulator()
        if (message == f'/{util.commands.EXIT_COMMAND}'):
            connection.close()
            break
        
        elif (message == '/'):
            continue
        
        elif dotenv.alice_connection_flag:
            connection.send(message.encode())
        else:
            print('Client closed the connection.')
            break


if __name__ == '__main__':
    main()