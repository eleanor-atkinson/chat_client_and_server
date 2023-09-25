import socket
import threading

HOST = "localhost"
PORT = 5050

clients = {}  # Store clients + their connections


# wait for connection request from client
def listen_to_client(client_sock):
    username = None

    if len(clients) >= 64:
        client_sock.send('BUSY\n'.encode())

    try:
        while True:
            message = ""

            while True:
                data = client_sock.recv(4096)

                if not data:
                    break
                message += data.decode("utf-8")

                # continue if decoded message doesn't end with a new line
                if not message.endswith('\n'):
                    continue
                else:
                    break
            # Receive the initial HELLO-FROM message from the client
            # message = client_sock.recv(4096).decode().strip()

            if not message.startswith(('HELLO-FROM', 'LIST', 'SEND', '!quit')):
                client_sock.send('BAD-RQST-HDR\n'.encode())

            if message.startswith('HELLO-FROM'):
                username = message[11:]

                # Check if given username has any spaces; if invalid send out error
                if " " in username:
                    client_sock.send('BAD-RQST-BODY\n'.encode())
                    message = client_sock.recv(4096).decode().strip()

                # Check if the username is already taken / in use
                if username in clients:
                    client_sock.send('IN-USE\n'.encode())

                # Add the client to the dictionary of clients
                # + Send a welcome message to the client
                else:
                    clients[username] = client_sock.recv(4096).decode().strip()
                    client_sock.send(('HELLO ' + username + "\n").encode())

            while True:
                message = client_sock.recv(4096).decode().strip()

                if message == 'LIST':
                    # Send the list of current users that are logged in
                    client_sock.send(('LIST-OK\n' + ', '.join(clients.keys()) + '\n').encode())

                elif message.startswith('SEND '):
                    # split message into recipient and message
                    split_msg = message.split(' ', 2)

                    if len(split_msg) == 3:
                        recipient = split_msg[1]
                        msg = split_msg[2]

                        if recipient in clients:
                            # Confirm to client that the message can be sent
                            client_sock.send('SEND-OK\n'.encode())
                            # Forward the message to the recipient
                            clients[recipient].send(('DELIVERY ' + username + ' ' + msg + '\n').encode())
                        else:
                            # Send an error to sender if the recipient username isn't logged in
                            client_sock.send('BAD-DEST-USER\n'.encode())
                    else:
                        # Send an error to the sender if there are issues with the message body
                        client_sock.send('BAD-RQST-BODY\n'.encode())

                elif message == "":
                    del clients[username]
                    break

            # except OSError as msg:
            #     print(msg)
            #     socket.close()
            #     break

    except:
        pass


# start server upon connection request
def start_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    server_sock.listen()

    try:
        while True:
            client_sock, addr = server_sock.accept()
            print("New user connected:", addr)

            client_thread = threading.Thread(target=listen_to_client, args=(client_sock,))
            client_thread.start()

    except KeyboardInterrupt:
        print("Chat server has been closed.")
    finally:
        server_sock.close()


#############################################
# This is where the program starts running. #
#############################################

start_server()
