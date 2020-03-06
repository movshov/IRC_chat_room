import socket
import select
import errno #used for mathcing error codes. 
import sys

HEADER_LENGTH = 40
IP = "127.0.0.1"
PORT = 1234

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False) # recieve won't be blocking.

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    message = input(f"{my_username} > ")

    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message) #Sending message 
    
    try:
        while True:
            # receive things
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')  # grab the username. 

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f"{username} > {message}")

    except IOError as e: # types of error messages we can expect when there are no messages to be recieved.
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error occured', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error',str(e))
        sys.exit()
        pass


    def create_room():
        """Send a message to the server starting with the keyword 
           CREATE letting the server know that we want to create a 
           new room on the server.
        """
        print("What is the name of the room you would like to create?\n")
        room_name = input(f"{room_name} > ") #grab the room name from the user.
        message = "CREATE" + room_name 

        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)


    def leave_room():
        """Send a message to the server starting with the Keyword
           LEAVE letting the server know that this person wishes 
           to leave a room.
        """
        print("Which room would you like to leave?\n")
        room_name = input(f"{room_name} > ") #grab the room name from the user.
        message = "LEAVE" + room_name 

        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)


    def list_rooms():
        """Send a message to the server starting with the keyword 
           LIST letting the server know that this person wished to
           see all the rooms that are available on this server. 
        """
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        message = "LIST"
        client_socket.send(message_header + message)


    def join_room():
        """Send a message to the server starting with the keyword
           JOIN letting the server know that this person wishes to 
           join this specific room. 
        """ 
        print("Which room would you like to join?\n")
        room_name = input(f"{room_name} > ") #grab the room name from the user.
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        message = "JOIN" + room_name
        client_socket.send(message_header + message)















