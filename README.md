Bar Movshovich  
CS 594 Internetworking Protocls  
https://github.com/movshov/IRC_chat_room  
# IRC Chat Room
Description: IRC or Internet Relay Chat is an application that lets multiple users communicate via text
messages with each other in common "virtual" rooms. I have implemented an IRC
client and server from scratch in python. As the programmer, I am in charge of all of the protocol
specifications and functionality of my IRC application. However, at a minimum, the
basic functionality of being able to create a room, join a room, leave a room, and list
rooms available have be implemented. Other features such as private chat, file
transfer, buddy lists, etc. can be added later, but must be specified and documented.

# Build
Thankfully there isn't any setup to run this program aside from the user already having 
python3 installed on their computer. 

To install python3 run this command:
```
sudo apt-get update
sudo apt-get install python3
```

If you already have python installed make sure you are using python3. You can update your 
version of python by running the command:
```
sudo apt-get upgrade python3
```
# Run
To run the program you will need at least two terminals open. First, we are going to be setting up the IRC server.
To do so run the following command:
```
python3 server_v2.py
```

Now that the server is running we can create a client by running the following command:
```
python3 client_v2.py
```

Now we are ready to begin using the program. 

# Commands
Listed below are the commands that are currently avialable to you as a client:
```
CREATE - Create a room with a given name such as Music
Ex: CREATE Music

LIST - List all rooms currently available on the server. 
Ex: LIST

JOIN - Join a room that exists on the server. 
Ex: JOIN Music

LEAVE - Leave a room that exists on the server. 
Ex: LEAVE Music

SHOW_MEM - List all members of a specific room on the server. 
Ex: SHOW_MEM Music

```

Every client that joins this server will have access to these commands. 
Currently there isn't an EXIT command to close the client so to exit simply hit "ctrl + c". 

