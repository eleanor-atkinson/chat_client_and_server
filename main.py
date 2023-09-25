from threading import Thread

import Chat_Client

import Chat_Server


def main():
    print("Starting up chat client...")

    Chat_Client.get_username()

    Chat_Client.thread2 = Thread(target=Chat_Client.receive, daemon=True, name="Receive")

    Chat_Client.thread2.start()

    Chat_Client.get_input()

    Chat_Server.start_server()
