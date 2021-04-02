import socket, string, os, time, sys
import pygame
import connect4
import view
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

board = connect4.create_board()
view.loadGame(board)
game_started = False

def game():
    global message
    global game_started

    TIME_TO_WAIT = 5
    
    game_over = False
    # Gather each input, MAX of 1 input per user, in a time frame of x seconds, return winning input
    while not game_over:
        if message != "":
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
            game_tuple = connect4.chooseLocation(array.index(max(array)), board)
            if not game_tuple == None:
                print("Player {player} wins!".format(player=game_tuple[1]))
                game_over = game_tuple[0]
                view.showWinningText(game_tuple[1])
            print(game_over)

    game_started = False 

def twitch():
    global game_started
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
                
                if int(message) and not game_started:
                    print("Game started")
                    game_started = True
                    # event = pygame.event.Event(pygame.JOYBUTTONUP)
                    # pygame.event.post(event)
                    t2.start()

                print(message)

if __name__ == '__main__':
    # Initiate program
    join(server)
    view.loadGame(board)

    t1 = threading.Thread(target=twitch)
    t1.daemon = True
    t1.start()

    t2 = threading.Thread(target=game)
    t2.daemon = True

    # game loop
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                raise SystemExit

            # if event.type == pygame.JOYBUTTONUP:
            #     print("post worked")