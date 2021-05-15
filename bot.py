import random
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


def game():
    global message
    global game_started

    TIME_TO_WAIT = 18
    # Thread loop
    while True:
        if game_started:
            # with open("current.txt", "w") as f:
            #     f.write("Game in progress!")
            view.updateCurrentText("Game in progress!")
            board = connect4.create_board()
            view.screen.fill((0,0,0))
            view.removeText()

            game_over = False
            # Gather each input, MAX of 1 input per user, in a time frame of x seconds, return winning input
            if message != "":
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
                    

                    maxElem = array.index(max(array))
                    maxes = [maxElem]
                    # Checking if more than 1 elements have the same value
                    for i in range(len(array)):
                        print(i, "greater")
                        if array[i] == array[maxElem] and i != maxElem:
                            print(i)
                            maxes.append(i)
                    print(maxes)
                    if len(maxes) > 1:
                        print("gone to max array")
                        game_tuple = connect4.chooseLocation(random.choice(maxes), board) 
                        print(array)
                    else:
                        game_tuple = connect4.chooseLocation(maxElem, board)
                        print(array)
                
                    if not game_tuple == None:
                        print("Player {player} wins!".format(player=game_tuple[1]))
                        game_over = game_tuple[0]
                        view.updateWinner(game_tuple[1])
                        message = ""
                    print(game_over)
                    if not game_over:
                        time.sleep(4.2)
            game_started = False 
            view.updateCurrentText("Game over, waiting to restart...")

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
                print(message)
                try:
                    if 1 <= int(message) <= 7  and not game_started:
                        print("Game started")
                        game_started = True
                        # event = pygame.event.Event(pygame.JOYBUTTONUP)
                        # pygame.event.post(event)
                except ValueError:
                    pass

if __name__ == '__main__':
    # Initiate program
    join(server)
    board = connect4.create_board()
    view.removeText()
    view.loadGame(board)
    view.updateCurrentText("Waiting to start...")
    game_started = False

    t1 = threading.Thread(target=twitch)
    t1.daemon = True
    t1.start()

    t2 = threading.Thread(target=game)
    t2.daemon = True
    t2.start()

    difficulties = ["debug", "Easy", "Medium", "Hard"]
    with open("difficulty.txt", "w") as f:
        f.write(difficulties[connect4.DIFFICULTY_LEVEL-1])

    # pygame loop
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                view.removeText()
                view.updateCurrentText("Waiting to start...")
                game_over = True
                raise SystemExit

            # if event.type == pygame.JOYBUTTONUP:
            #     print("post worked")