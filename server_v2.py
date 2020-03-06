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
rooms = []

def list_rooms():
    """list all rooms that are currently available 
       on this server. Rooms are stored in the rooms list
       created at the top of this file on line 17. 
    """
    print("inside list_rooms func")
    list = ""
    for x in rooms:
        print(x)
        list += x + ","
    return list


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):  #if we didn't get any data. 
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

            for client_socket in clients:
                if "CREATE" in message['data'].decode('utf-8'): #create a new room. 
                    room = message['data'].decode('utf-8').replace('CREATE ', '')
                    rooms.append(room)
                    print("create room\n")
                if "LIST" in message['data'].decode('utf-8'):    #List all rooms available.
                    print("\ninside list\n")
                    if client_socket == notified_socket:    #make sure we are the user who issued this command.
                        all_rooms = list_rooms()
                        print("all_rooms is: {}".format(all_rooms))
                        message = all_rooms.encode('utf-8')
                        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(user['header'] + user['data'] + message_header + message) #Sending message 
                    
                if client_socket != notified_socket: #if we are not the ones who sent the message, send it.
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_socket:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]



