import socket 
import select

HEADER_LENGTH = 40
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}
rooms = []  # List of rooms by name only for quick display. 
class_rooms = [] # List of all rooms using the class below for other functionality.

class room():
    members = [] # List of people that have joined this room. 

    def __init__(self, name): # Constructor. 
        self.name = name

    def join(self, client_socket):
        members.append(client_socket) # Add a client to the list of members in this room.

    def leave(self, client_socket):
        members.remove(client_socket) # Remove a client from the list of members.

    def list_members(self): # List all members that are inside this room.
        list = ""
        for x in members:
            print(x) # Displaying for server side(NOT NECESSARY). 
            list += x + ","
        return list # Return a list of all members of this room.

 #   def message(self, message):


def list_rooms():
    """list all rooms that are currently available 
       on this server. Rooms are stored in the rooms list
       created at the top of this file on line 17. 
    """
    print("inside list_rooms func")
    list = ""
    for x in rooms: # Display for server side what rooms exits. 
        print(x)
        list += (x + ',')
    return list  # Return a list of all rooms. 


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):  # If we didn't get any data. 
            return False

        message_length = int(message_header.decode("utf-8").strip())

        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False

while True:
    read_sockets, _, exception_socket = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue
            
            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

        else:
            message = receive_message(notified_socket) 
            if message is False:
                print(f"closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]

            print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            # This is where we check for client commands such as CREATE, LIST, JOIN, LEAVE, ...
            for client_socket in clients: 

                if "CREATE" in message['data'].decode('utf-8'): # Create a new room. 
                    temp_room = message['data'].decode('utf-8').replace('CREATE ', '')
                    rooms.append(temp_room)
                    class_rooms.append(temp_room) 
                    print("created a new room: '{}'\n".format(temp_room))

                if "LIST" in message['data'].decode('utf-8'): # List all rooms available.
                    if client_socket == notified_socket:    # Make sure we are the user who issued this command.
                        if len(rooms) == 0:
                            print("Error, there are currently no rooms to list")
                        else:
                            all_rooms = list_rooms()
                            message = all_rooms.encode('utf-8')
                            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                            user_header = user['header']
                            user_data = user['data']
                            client_socket.send(user['header'] + user['data'] + message_header + message) #Sending message 

                if "JOIN" in message['data'].decode('utf-8'): # List all rooms available.
                    if client_socket == notified_socket:    # Make sure we are the user who issued this command.
                        temp_room = message['data'].decode('utf-8').replace('JOIN ', '')
                        if temp_room in rooms:  # Make sure the room we are trying to join exists first. 
                           class_rooms[temp_room].join(client_socket) # Call Join method in class room. 
                        else:
                            print("Error attempting to join room. Make sure you are spelling the room correctly.\n")

                if "LEAVE" in message['data'].decode('utf-8'): # Leave a specific room.
                    if client_socket == notified_socket:    # Make sure we are the user who issued this command.
                        temp_room = message['data'].decode('utf-8').replace('LEAVE ', '')
                        if temp_room in rooms:  # Make sure the room we are trying to join exists first. 
                           class_rooms[temp_room].leave(client_socket) # Call Join method in class room. 
                        else:
                            print("Error attempting to leave room. Make sure you are spelling the room correctly.\n")

                if "LIST_MEM" in message['data'].decode('utf-8'): # List all members of a specific room.
                    if client_socket == notified_socket:    # Make sure we are the user who issued this command.
                        temp_room = message['data'].decode('utf-8').replace('LIST_MEM', '')
                        if temp_room in rooms:  # Make sure the room we are trying to join exists first. 
                           room_members = class_rooms[temp_room].list_members() # Call list_members method in class room. 
                           message = room_members.encode('utf-8')
                           message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                           client_socket.send(user['header'] + user['data'] + message_header + message) #Sending message 
                        else:
                            print("Error attempting to leave room. Make sure you are spelling the room correctly.\n")




                if client_socket != notified_socket: # If we are not the ones who sent the message, send it.
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_socket:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]



