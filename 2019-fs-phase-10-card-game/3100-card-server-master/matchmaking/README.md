# Matchmaking Server
Simple Matchmaking Server for CS 2300. Allows TCP connections and then redirects
users if the lobby limit is reached. The server is ran by yarn which can be
obtained at https://yarnpkg.com/lang/en/docs/install/

## Running the Server
In **development**, the best way to run the server is using nodemon:
```bash
$ yarn install
$ yarn start:dev
...
Server is now listening on 127.0.0.1:8000...
```

## Examples
An example client / game server implementation for connecting to the matchmaking
server in Python can be found in `examples/` directory.
