import socket
import sys
from threading import Thread

# to create a socket object

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# to establish a connection with the chat server
host_port = ("143.47.184.219", 5378)
client_sock.connect(host_port)

# to establish a connection with the chat server assignment
host_port = ("localhost", 5050)
client_sock.connect(host_port)


# retrieve the username when the user is prompted to log in
def get_username():
    global client_sock
    global host_port
    while True:
        user_name = input('Enter a unique user name: ')
        message = 'HELLO-FROM {}\n'.format(user_name)
        client_sock.send(message.encode())
        response = client_sock.recv(4096).decode()

        if response.startswith('HELLO '):
            print('You are logged in as {}'.format(response[6:].strip()))
            break

        elif response == 'IN-USE\n':
            print('That username is already in use. Please input an alternative.')
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host_port = ("localhost", 5050)
            client_sock.connect(host_port)

        elif response == 'BAD-RQST-BODY\n':
            print('error in header')
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host_port = ("localhost", 5050)
            client_sock.connect(host_port)

        elif response == 'BUSY\n':
            print(
                'The maximum number of clients has been reached. Please try again later.'
            )
            sys.exit()

        else:
            print('Unexpected response from server.')


# retrieve any input from the user
def get_input():
    while True:
        user_input = input('> ')

        if user_input == '!who':
            message = 'LIST\n'
            client_sock.send(message.encode())

        if user_input == '!quit':
            print('Chat client has been shutdown')
            message = 'client_quit'
            client_sock.send(message.encode())
            client_sock.close()
            break

        if user_input.startswith("@"):
            user_input = user_input.replace('@', ' ')
            split_into_list = user_input.split(' ', 2)
            if len(split_into_list) >= 3:
                recv_username = split_into_list[1]
                message_to_send = split_into_list[2]
            else:
                print("Message not sent to user; message body missing")
                continue

            message = 'SEND {} {}\n'.format(recv_username, message_to_send)
            # send first handshake message
            client_sock.send(message.encode())


# buffer function ensuring that client is constantly listening for new messages
def receive():
    while True:
        try:
            response = ""

            while True:
                data = client_sock.recv(4096)
                if not data:
                    break
                response += data.decode("utf-8")
                # continue if decoded message doesn't end with a new line
                if not response.endswith('\n'):
                    continue
                else:
                    break

            if not response:
                print("Socket is closed.")
                break

            if response.startswith('LIST-OK\n'):
                print('Here is a list of all currently logged in users: {}'.format(response[8:].strip()))
                continue

            if response.startswith('SEND-OK\n'):
                print('Message sent successfully')
                continue

            if response.startswith('BAD-DEST-USER\n'):
                print('Message not sent; receiving user not found')
                continue

            if response.startswith('BAD-RQST-HDR\n'):
                print('Message not sent to server; error in header')
                continue

            if response.startswith('BAD-RQST-BODY\n'):
                print('Message not sent to server; error in body')
                continue

            print("Response from {}".format(response[8:].strip()))

        except OSError as msg:
            print(msg)
            socket.close()
            break


#############################################
# This is where the program starts running. #
#############################################

get_username()

thread2 = Thread(target=receive, daemon=True, name="Receive")

thread2.start()

get_input()
