import socket, string, os, time, sys
#import connect4
import threading
from init import join
from vars import data

dest = "irc.chat.twitch.tv"
port = 6667
nickname = data.get("CHANNEL_NAME")
token = data.get("OAUTH_TOKEN")
channel = "#"+nickname
message = ""

server = socket.socket()
server.connect((dest, port))
server.send(bytes(f"PASS {token}\n".encode('utf-8')))
server.send(bytes(f"NICK {nickname}\n".encode('utf-8')))
server.send(bytes(f"JOIN {channel}\n".encode('utf-8')))


def gather_input():
    # Gather each input, MAX of 1 input per user, in a time frame of x seconds, return winning input
    x = 10
    t_end = time.time() + x
    array = [0,1,2,3,4,5,6]
    while time.time() < t_end:
        if message != "":
            print(message + "test")
        
    
def twitch():
    def getMessage(line):
        global message
        separate = line.split(":", 2)
        #print(separate)
        message = separate[2]
        return message
    
    def getUser(line):
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)
        return user[0]
    
    while True:
        readbuffer = ""
        readbuffer = readbuffer + server.recv(2048).decode('utf-8')
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()
        for line in temp:
            if line == "PING :tmi.twitch.tv\r":
                server.send(("PONG :tmi.twitch.tv\r\n").encode("utf-8"))
            else:
                message = getMessage(line)
                user = getUser(line)

                print(message)


if __name__ == '__main__':
    # Initiate program
    join(server)
    #connect4.loadGame()
    t1 = threading.Thread(target=twitch)
    t1.start()
    t2 = threading.Thread(target=gather_input)
    t2.start
