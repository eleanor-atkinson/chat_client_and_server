# Chat_Client_And_Server

This is a text-based chat client running on a chat server designed using the same network protocol. 

## **Background**

The goal of this project for me was to learn more about Computer Networks through the best way I know how– experimenting! Specifically, I wanted to explore the widely used Transmission Control Protocol (TCP), one of the core internet protocols, used for ensuring reliable and ordered delivery of data between two (or more) devices over a network. 

## **About**

This is a text-based chat client and server that connects clients that allows for the exchange of messages between different computers. It is built on top of TCP and uses its own application layer protocol. The client can ask the server to perform actions by sending predefined types of messages. For example, the client can ask the server to forward a message to another user’s client by sending the string <html> <body> SEND username [insert your message] here\n </body> </html> to the server, where “username” is the user to whom they want to send the message. You  will then be notified whether the message was sent successfully. The server can host at least 64 simultaneous clients. 

## **Technicalities**

Similar to Web browsers and other modern applications that prioritize cybersecurity, the chat client does not expose the protocol it uses to the user. Instead, it provides a user-friendly text-based interface that makes it easy for users to chat with others without knowing protocol specifications. 

## **Techniques** 

I learned about Python sockets and practiced getting comfortable using the socket interface to leverage connection requests using network-layer and transport-layer addresses. I also familiarized myself with the concept of Deamon threading  using Python’s threading library and implemented a daemon thread to run in the background for the “logging in” function and to perform clean-up periodic tasks such as checking who’s logged in at any given time. 

## **Important Note**

The host port I was using to run this is no longer functioning. Please reach out to me if you have a port I can run it on. I really want to document how the client looks while running. :)

## **TCP Trace Analysis**

TCP uses a three-way handshake mechanism to establish a connection between the client and server. 

First, a synchronization packet (SYN) is sent by our local host IP to the chat server. 
The server then reciprocates by sending an acknowledgement packet (ACK) to the local host signaling that it has received the SYN request to connect. The server also sends a synchronization packet (SYN) to the local host to confirm connection. 
The host answers the server by sending the acknowledgement packet (ACK) once it receives the SYN. 

In TCP segments, the 16 byte hex dump represents the chat message data. This is found by locating the TCP packet that corresponds to the chat message, expanding the "Data" field within the TCP segment details, and examining its content (which can be done in the application Wireshark). 

The segments that contain the FIN (Finish) flag set close the TCP connection. The FIN flag indicates that a party (in this case, the chat client) wants to close its end of the connection. Futhermore, we needed to verify that the server acknowledged the FIN packet by ensuring that there was a ACK packet from the client. Once we saw the FIN and ACK packets being exchanged in both directions, indicating to us that the TCP connection is closing we identified the following segments. 
