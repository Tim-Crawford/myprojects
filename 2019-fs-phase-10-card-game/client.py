import json
import socket
import time
from random import randint
from struct import pack, unpack

HOST = '127.0.0.1'
PORT = 8000


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
                #"clientInfo": {
                    "clientInfo": self.player_id
                #}
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


def main():
    with socket.socket() as s:
        player_id = str(randint(0, 9))
        # Connect to matchmaking server
        s.connect((HOST, PORT))

        client = Client('player-' + player_id, s)
        try:
            client.waitForMM()
            client.sendGSInit()
            client.updateState({"test": "test"})
            # Wait for all clients to send initial message
            time.sleep(.25)
            client.updateState({"test": "test"})
            client.finish()
        except Exception as e:
            print('Error:', e)
            return
        print('done')
        return


if __name__ == '__main__':
    main()
