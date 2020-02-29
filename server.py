import socket
import select
import sys
import thread import * 


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
    print("Error!!! Please follow the format: script, IP_Address, port_number)"
    return;

else:
    # grab IP_Address from command line. 
    IP_Address = str(sys.argv[1])
    # grab port # from command line. 
    Port = int(sys.argv[2])

