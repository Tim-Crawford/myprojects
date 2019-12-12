## Expected Interaction
 1. Client connects to server. -> **Client state is `connecting`.**
 2. Server sends `whois` message to client.
 3. Client sends `client-info` to server. -> **Client state is `ready`.**
 4. Client receives `client-info` from server containing the information it sent.
 5. Client receives `client-info` from server for all other clients that connect.
 6. Game starts: -> **Client state is `playing`**
    - Client sends `game-state` to server containing the initial game state.
    - Client receives `game-state` from server containing the initial game state. This occurs if another client starts the game first.
 7. Game progress:
    - Client requests state update:
       1. Client sends `game-state` to server containing a requested state.
       2. Client either receives `error` from server or `game-state` from server. It should update its local state with the state in this message.
    - Client receives state update:
       1. Client receives `game-state` from server containing an updated state.
    - Game ends:
       1. Client receives `client-info` from server for each connected client.
       2. Client receives `game-finished` from server.
       3. Go to step 4. -> **Client state is `ready`.**

### Notes:
 - If the game is running, all error messages contain the current game state.
 - The client can receive `client-info` at any time containing updated client information for a connected client. This may include information about clients who have just connected. If it does, the client should do any necessary work to initialize that client locally (if necessary).

## Events

### On connection:
 - Client state set to `connecting`.
 - Server sends `whois` message to client.
    - Client is expected to send `client-info` to server to identify itself.

### On message received:
- Check `GameServer.processMessage()` for details.