import socket
import select
import sys
from thread import * 


"""Set up server connection
Args:
    AF_INET: Address domain of our socket. 
    SOCK_STREAM: type of socket being used. 
"""
# The IRC protocol is a layer on top of the IP protocol. 
irc_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# check to make sure the user has entered in the correct format.
if len(sys.argv) != 3: 
    print("Error!!! Please follow the format: script, IP_Address, port_number")
    exit()

else:
    # grab IP_Address from command line. 
    IP_Address = str(sys.argv[1])
    # grab port # from command line. 
    Port = int(sys.argv[2])

# using the above information bind the server to the desired IP_Adress and Port Number. 
server.bind((IP_Adress, Port))

server.listen(100)
list_of_clients = []

def clientthread(conn, addr):
    # sends a message to the client whose user obj is conn
    conn.send("welcome to this chat room.")

    while True:
        try: 
            message = conn.recv(2048)
            if message:
                print("<" + addr[0] + "> " + message)
                message_to_send = "<" + addr[0] + "> " + message
                broadcast(message_to_send, conn)

            else:
                remove(conn)
        except:
            continue


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0] + " connected")
    start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()

















