import socket, string, os, time, sys
import pygame
import connect4
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


def game_loop():
    global message
    # Gather each input, MAX of 1 input per user, in a time frame of x seconds, return winning input
    TIME_TO_WAIT = 5
    game_over = False

    # Wait for input to start the game
    while message == "":
        continue

    # Game loop
    while not game_over:
        t_end = time.time() + TIME_TO_WAIT
        array = [0,0,0,0,0,0,0]
        print("----- GATHERING INPUT -----")
        while time.time() < t_end:
            try:
                num = int(message)
                if 1<= num <= 7:
                    array[num-1] += 1
                    message = ""
            except ValueError:
                pass

        game_over = connect4.chooseLocation(array.index(max(array)))
        print(game_over)

def twitch():
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


if __name__ == '__main__':
    # Initiate program
    connect4.loadGame()
    join(server)
    try:
        t1 = threading.Thread(target=twitch)
        t1.start()
        t2 = threading.Thread(target=game_loop)
        t2.start()
    except:
        print("Error starting threads.")
    