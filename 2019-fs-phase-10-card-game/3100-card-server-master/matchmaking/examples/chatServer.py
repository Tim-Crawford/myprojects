"""
Demo Chat Server

    Essentially just acts as a switch to any connected
    clients for their messages
"""

import threading
import socket
import queue
import json
import sys

# Connects to the matchmaker to find clients
def matchmaker(host = '127.0.0.1', port = 8000, localIP = '127.0.0.1', localPort = 8001):
    # Creates the socket communicating with the matchmaker
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # sends ID to matchmaker
        payload = {
            "ip": localIP,
            "port": localPort,
            "game": "Chat",
            "type": "server",
            "gameRules": {
                "minPlayers": 2,
                "maxPlayers": 2,
            }
        }
        s.sendall(json.dumps(payload).encode("utf-8"))

        # Wait for response
        data = s.recv(1024)
        response = json.loads(data)
        #print('Received', response)

        if response.get("type") == "message":
            print('Waiting for clients to connect')
            data = s.recv(1024)
            response = json.loads(data)

            # If mm finds clients, ID's will be returned
            if response.get("type") == "connect":
                #print(response)
                s.close()
                return response.get("clients")
        else:
            print('Error when connecting to matchmaker')
            s.close()
            return []

# Threads for handling individual messages
def getMsgs(conn, Q):
    while True:
        Q.put(conn.recv(1024))
    return
def sendMsgs(conn, Q):
    for i in range(len(conn)):
        conn[i].sendall(('Welcome to the chat server').encode("utf-8"))

    while True:
        data = Q.get()
        for i in range(len(conn)):
            conn[i].sendall(data)
    return

if __name__ == "__main__":
    print('Demo Chat Server\n')

    # Get local IP Address
    addr = input('Local Address(Default localhost): ') or '127.0.0.1'
    port = input('Local Port(Default 8001): ') or 8001

    # Get matchmaker Address
    mmAddr = input('Matchmaker Address(Default localhost): ') or '127.0.0.1'
    mmPort = input('Matchmaker Port(Default 8000): ') or 8000

    # Determine the number of clients to expect
    clients = matchmaker(mmAddr, mmPort, addr, port)
    clientNum = len(clients)
    if clientNum == 0:
        print('Error: No clients found')
        sys.exit()

    # Create a socket to listen for new client connections
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((addr, port))
    except socket.error:
        print('Error: Socket bind failed')
        sys.exit()
    print('\nSocket bound to address')

    listener.listen(clientNum)
    print('Listening for new connections')

    # Handle route messages in seperate threads
    Q = queue.Queue()
    conn = []
    threading.Thread(target=sendMsgs, args=(conn, Q,)).start()
    while True:
        # Accept client connection
        temp, addr = listener.accept()
        conn.append(temp)
        print('Connection established with ' + str(addr[0]) + ':' + str(addr[1]))

        threading.Thread(target=getMsgs, args=(temp, Q,)).start()

    listener.close()