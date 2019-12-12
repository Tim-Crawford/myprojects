import json
from struct import pack, unpack
import socket

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


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = json.dumps(
        {
            "messageType": "connect",
            "data": {
                "configuration": {
                    "ip": "127.0.0.1",
                    "port": "8000",
                    "rules": {
                        "minPlayers": 2,
                        "maxPlayers": 3,
                        "waitTime": 5
                    }
                },
                "game": "test",
                "clientType": "server"
            },
        }
    )
    response = send_json(s, data)
    print('Received', response)

    if response.get("messageType") == "response":
        print('Waiting for clients to connect')
        print('Response:', recv_json(s))
    else:
        print('Error when connecting to server')
