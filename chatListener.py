from init import join
import socket, string, os
from init import join
from vars import data

dest = "irc.chat.twitch.tv"
port = 6667
nickname = data.get("CHANNEL_NAME")
token = data.get("OAUTH_TOKEN")
channel = "#"+nickname
readbuffer = ""

server = socket.socket()
server.connect((dest, port))
server.send(bytes(f"PASS {token}\n".encode('utf-8')))
server.send(bytes(f"NICK {nickname}\n".encode('utf-8')))
server.send(bytes(f"JOIN {channel}\n".encode('utf-8')))

def openSocket():
    server = socket.socket()
    server.connect((dest, port))
    server.send(bytes(f"PASS {token}\n".encode('utf-8')))
    server.send(bytes(f"NICK {nickname}\n".encode('utf-8')))
    server.send(bytes(f"JOIN {channel}\n".encode('utf-8')))
    return server

def runListener():
    def getMessage(line):
        global message
        separate = line.split(":", 2)
        #print(separate)
        message = separate[2]

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
                getMessage(line)
                user = getUser(line)
                print(message)

