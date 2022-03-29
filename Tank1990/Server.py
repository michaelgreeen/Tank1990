import socket
from _thread import *
import sys
import Common

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((Common.IP_ADDRESS, Common.PORT))
except socket.error as e:
    str(e)

s.listen(5)
print("Waiting for a connection, Server Started")


pos = [(0,0),(100,100)]

def threaded_client(conn, player):
    conn.send(str.encode(Common.make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = Common.read_pos(conn.recv(2048/2).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(Common.make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1