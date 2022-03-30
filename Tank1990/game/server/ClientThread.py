from conf.Common import *

def clientThread(connection, playerNumber):
    connection.send(str.encode(make_pos(CLIENT_STARTING_POSITIONS[playerNumber])))
    reply = ""
    while True:
        try:
            data = read_pos(connection.recv(2048/2).decode())
            CLIENT_STARTING_POSITIONS[playerNumber] = data

            if not data:
                print("Disconnected")
                break
            else:
                if playerNumber == 1:
                    reply = CLIENT_STARTING_POSITIONS[0]
                else:
                    reply = CLIENT_STARTING_POSITIONS[1]

                print("Received: ", data)
                print("Sending : ", reply)

            connection.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    connection.close()