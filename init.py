import string
from vars import data

def join(server):
    readbuffer = ""
    Loading = True
    while Loading:
        readbuffer = readbuffer + server.recv(2048).decode('utf-8')
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()

        for line in temp:
            print(line)
            Loading = complete(line)


<<<<<<< HEAD
def complete:
=======
def complete(line):
    if("End of /NAMES list" in line):
        return False
    else:
        return True
>>>>>>> 8294dfb6d5a0d7e781331a3f9c1e2943ad2a17bb
    