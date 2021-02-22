import socket, string
from vars import data

connection_data = ("irc.chat.twitch.tv", 6667)
user = data.get("CHANNEL_NAME")
token = data.get("OAUTH_TOKEN")
channel = user
readbuffer = ""

server = socket.socket()
server.connect(connection_data)
server.send(bytes('PASS ' + token + '\r\n', 'utf-8'))
server.send(bytes('NICK ' + user + '\r\n', 'utf-8'))
server.send(bytes('JOIN ' + channel + '\r\n', 'utf-8'))

print(server)

while True:
    readbuffer = readbuffer + server.recv(2048)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        if (line[0] == "PING"):
            server.send("PONG %s\r\n" % line[1])
        else:
            parts = string.split(line, ":")