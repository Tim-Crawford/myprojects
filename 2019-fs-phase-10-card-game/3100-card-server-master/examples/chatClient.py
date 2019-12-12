'''
Demo Chat Client

    End points for sending messages between everyone connected to a server
'''

import sys
import json
import time
import socket
import threading
from random import randint
from struct import pack, unpack

def recv_json(server_socket):
    header = server_socket.recv(8)
    size = unpack('<I', header[4:8])[0]
    if not(header.startswith(b"JSON")):
        raise "Invalid JSON format (Missive)"
    if size < 0 or size > 1024 * 1024:
        raise "Incoming JSON is too large: " + str(size)
    # read incoming size from socket, then remove the trailing newline
    body = server_socket.recv(size)[:-1]
    # parse into json
    return json.loads(body)


def send_json(server_socket, msg_payload):
    if msg_payload[-1] != "\n":
        msg_payload += "\n"
    prefix = "JSON".encode("utf-8")
    size = pack("<I", len(msg_payload))
    message = msg_payload.encode("utf-8")
    server_socket.sendall(prefix + size + message)

    return recv_json(server_socket)


class Client(object):
    def __init__(self, player_id, server_socket):
        super().__init__()
        self.player_id = player_id
        self.server_socket = server_socket

    def waitForMM(self):
        data = json.dumps({
            "messageType": "connect",
            "data": {
                "game": "default",
                "clientType": "client",
                "configuration": {
                    "id": self.player_id,
                }
            }
        })
        json_response = send_json(self.server_socket, data)
        while json_response.get('messageType') != 'connect':
            if json_response.get('messageType') == 'error':
                raise Exception(json_response.get('data'))
            if json_response.get('messageType') == 'response':
                print("Message:", json_response.get('data'))
                json_response = recv_json(self.server_socket)

        print('Connect:', json_response.get('data'))

    def sendGSInit(self):
        game_connect_payload = json.dumps({
            "messageType": "client-info",
            "data": {
                "clientInfo": {
                    "id": self.player_id
                }
            }
        })
        gs_response = send_json(self.server_socket, game_connect_payload)
        messageType = gs_response.get("messageType")
        messageData = gs_response.get("data")
        if messageType == "error":
            raise Exception(messageData)
        elif messageType == "client-info":
            print("client-info:", messageData)
        elif messageType == 'game-state':
            print("game-state:", messageData)

    def updateState(self, state):
        game_state_payload = json.dumps({
            "messageType": "game-state",
            "data": {
                "state": state
            }
        })
        gs_response = send_json(self.server_socket, game_state_payload)
        print(gs_response)
        messageType = gs_response.get("messageType")
        messageData = gs_response.get("data")
        if messageType == "error":
            raise Exception(messageData)
        elif messageType == 'game-state':
            print("game-state:", messageData)

    def finish(self):
        game_finish_payload = json.dumps({"messageType": "game-finished"})
        gs_response = send_json(self.server_socket, game_finish_payload)
        print(gs_response)
        messageType = gs_response.get("messageType")
        messageData = gs_response.get("data")
        if messageType == "error":
            raise Exception(messageData)
        elif messageType == "game-finished":
            print("game-finish", messageData)
 
# Listen for messages from the server
def listen(serv):
    while True:
        response = recv_json(serv)
        print(response.get("data"))
    return

if __name__ == "__main__":
    print("Demo Chat Client")

    # Get matchmaker address
    mmAddr = input('Matchmaker Address(Default localhost): ') or '127.0.0.1'
    mmPort = input('Matchmaker Port(Default 8000): ') or 8000

    # Find address of chat server
    name = input("Enter screen name(Default test#): ") or "test" + str(randint(0, 9))
    

    #Sleep to allow server sockets to open
    time.sleep(1)

    # Connect to the chat server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
        serv.connect((mmAddr, mmPort))

        client = Client(name, serv)
        client.waitForMM()
        client.sendGSInit()

        threading.Thread(target = listen, args = (serv,)).start()
        welcome = name + " has entered the server."
        # payload = {
        #     "messageType": "random-data",
        #     "data": welcome
        # }
        send_json(serv, welcome)

        while True:
            msg = input()
            msg = name + ': ' + msg
            payload = {
            "messageType": "random-data",
            "data": msg
            }
            send_json(serv, msg)

        serv.close()
    sys.exit()
