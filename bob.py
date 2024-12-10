import dotenv
import socket
from threading import Thread

#handle receiving messages here
def handle_receive(sock):
    try:
        while True:
            message = sock.recv(2048).decode()
            if not message:
                break
            print(f"Alice: {message}")
            
    #gracefully exit and close socket when main thread closes the connection
    except (ConnectionAbortedError, OSError):
        print("READING THREAD: Connection closed by main thread, exiting.")
    finally:
        sock.close()
        dotenv.bob_connection_flag = False



def main():
    sock = socket.socket()
    sock.connect((dotenv.alice_ip, dotenv.alice_port))
    print('Connection established with Alice.')
    dotenv.bob_connection_flag = True

    
    #start the thread for receiving messages
    receive_thread = Thread(target=handle_receive, args=(sock,))
    receive_thread.start()
    
    #main thread will send messages here
    while True:
        message = input("")
        if (message == '/close' or message == '/c'):
            sock.close()
            break
        elif dotenv.bob_connection_flag:
            sock.send(message.encode())
        else:
            print('Server closed the connection.')
            break

if __name__ == '__main__':
    main()