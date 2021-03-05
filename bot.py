import socket, string, os, utils
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

def game_started():
    # Print game has started and wait for chat inputs

    # result = gather_input()
    pass

def gather_input():
    # Gather each input, MAX of 1 input per user, in a time frame of x seconds, return winning input
    pass

def getMessage(line):
    separate = line.split(":", 2)
    print(line)
    message = separate[2]
    return message
   
def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)
    return user[0]

while True:
    readbuffer = readbuffer + server.recv(2048).decode('utf-8')
    temp = readbuffer.split("\n")
    readbuffer = temp.pop()
    for line in temp:
                if line == "PING :tmi.twitch.tv\r":
                    utils.Pong(server)
                else:
                    msg = getMessage(line)
                    usr = getUser(line)

                    print(msg, usr)