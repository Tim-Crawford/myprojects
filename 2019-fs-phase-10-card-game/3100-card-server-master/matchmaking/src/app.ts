import * as debug from 'debug';
import { Encoder } from 'fringe';
import * as missive from 'missive';
import * as net from 'net';
import * as log from 'npmlog';
import { IClient } from './Client';
import { GameServer, IServerConfiguration } from './GameServer';
import { IConnectionData, IConnectionRequest } from './Protocol';

import {
  INVALID_CONFIG,
  NO_SERVERS_EXIST,
  VALID_SERVER_CONFIG,
} from './messages';

// Setup debugging
// @ts-ignore
log.level = process.env.LOG_LEVEL || 'info';
const serverDebug = debug('mmserver');
const server = net.createServer();

/**
 * Setup the server socket to properly work with missive message processing
 * @param socket - The socket connected to the mm-server for the server.
 * @param writer - The missive encoder writer.
 * @param data - The data the server sent to configure the server.
 */
function setupServer(
  socket: net.Socket,
  write: Encoder['write'],
  data: IConnectionData,
): GameServer {
  const config = data.configuration as IServerConfiguration;

  if (!config) {
    throw new Error("The 'configuration' attribute has not been defined");
  }

  const gs = new GameServer(
    data.game,
    config.ip,
    config.port,
    config.rules,
    socket,
    write,
  );

  log.info(
    'MM-Server',
    `Gameserver ${gs.ip}:${gs.port} (${gs.game}) waiting for ${
      gs.rules.minPlayers
    } clients.`,
  );

  return gs;
}

/**
 * Setup the client socket to properly work with missive message processing
 * @param socket - The socket connected to the mm-server for the client.
 * @param writer - The missive encoder writer.
 * @param data - The data the server sent to configure the client.
 */
function setupClient(
  socket: net.Socket,
  write: Encoder['write'],
  data: IConnectionData,
): IClient {
  return {
    socket: socket,
    write: write,
    game: data.game,
    configuration: data.configuration,
  };
}

server.on('listening', () => {
  const { address, port } = server.address() as net.AddressInfo;
  log.info('MM-Server', `Server is now listening on ${address}:${port}...`);
});

// tslint:disable:max-func-body-length
server.on('connection', (socket: net.Socket) => {
  log.verbose('MM-Server', `Connection from ${socket.remoteAddress}`);
  const encode = missive.encode();
  encode.pipe(socket);

  // Listen for the initial connection from the client and run the setup process
  // only once per connection
  socket
    .pipe(missive.parse())
    .once('message', (request: IConnectionRequest) => {
      if (request.messageType !== 'connect') {
        log.error('MM-Server', `Invalid messageType: ${request.messageType}`);
        encode.write(INVALID_CONFIG);
        socket.end();
        return;
      }
      const data: IConnectionData = request.data;

      // Configuration specific to client and server
      switch (data.clientType) {
        case 'server':
          // Creating the GameServer representation
          serverDebug('gameserver connected for %s', data.game);
          try {
            setupServer(socket, encode.write.bind(encode), data);
          } catch (error) {
            serverDebug('could not create gameserver %s', error.name);
            encode.write(INVALID_CONFIG);
            socket.end();

            return;
          }
          encode.write(VALID_SERVER_CONFIG);
          break;
        case 'client':
          // Creating the client representation
          let client;
          try {
            client = setupClient(socket, encode.write.bind(encode), data);
          } catch (error) {
            encode.write(INVALID_CONFIG);
            socket.end();

            return;
          }

          // Find the GameServer the user wants to queue up for
          const foundGameServer = GameServer.FIND(client.game);
          if (foundGameServer === undefined) {
            log.warn(
              'MM-Server',
              `No game servers were found for ${client.game}`,
            );
            encode.write(NO_SERVERS_EXIST);
            socket.end();

            return;
          }

          // Add client to gameserver
          foundGameServer.addClient(client);
          serverDebug(
            'found game server for game %s, for client %s, waiting to finish',
            foundGameServer.game,
            client.configuration.id,
          );

          break;
        default:
          serverDebug('unknown connection (did not specify type)');
          log.warn(
            'MM-Server',
            'Connection specified invalid connection type.',
          );
          encode.write(INVALID_CONFIG);
          socket.end();
      }
    })
    .on('error', (error: Error) => {
      if (error.message === 'Invalid message prefix: JSON') {
        serverDebug('received invalid json format for missive');
        encode.write(INVALID_CONFIG);
      } else {
        log.error('MM-Server', `${error.name}: ${error.stack}`);
      }
    });
});

server.listen(8000, '127.0.0.1');
