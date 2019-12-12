import * as debug from 'debug';
import { Encoder } from 'fringe';
import * as net from 'net';
import * as log from 'npmlog';
import { IClient } from './Client';
import {
  GAME_SERVER_DISCONNECTED,
  KICK_MESSAGE,
  MATCH_FOUND,
  VALID_CLIENT_CONFIG,
} from './messages';

export interface ILobby {
  leader: IClient;
  clients: Set<IClient>;
}

export interface IGameRules {
  minPlayers: number;
  maxPlayers: number;
  waitTime?: number;
}

// @ts-ignore
log.level = process.env.LOG_LEVEL || 'info';
const gameDebug = debug('game-server');

/**
 * Server configuration options that can be sent during the initial connection
 * message.
 */
export interface IServerConfiguration {
  ip: string;
  port: number;
  rules: IGameRules;
}

/**
 * Class representing a GameServer. Used to track GameServer connections and
 * lobbies for those game servers for the clients.
 */
export class GameServer {
  /**
   * Static list of all GameServers connected to the Matchmaking server.
   */
  public static servers: { [key: string]: Set<GameServer> } = {};

  /**
   * The IP of the connected game server.
   */
  public readonly ip: string;

  /**
   * The port of the connected game server.
   */
  public readonly port: number;

  /**
   * The rules the game server abides by (i.e. minimum number of players
   * necessary, maximum number players allowed, etc.).
   */
  public readonly rules: IGameRules;

  /**
   * The identifier for the game (gofish, poker).
   */
  public readonly game: string;

  /**
   * Lobby representation for the current game server.
   */
  public lobby?: ILobby;

  /**
   * Missive write encoder for sending messages to the server.
   */
  protected write: Encoder['write'];

  /**
   * Socket connected to the game server.
   */
  private socket: net.Socket;

  /**
   * If the current lobby has enough players and is currently waiting to
   * initiate a match.
   */
  private waiting: Promise<void> | undefined;

  /**
   * The time the game server will wait for more players when it has enough
   * players.
   */
  private readonly waitTime: number;

  constructor(
    game: string,
    ip: string,
    port: number,
    rules: IGameRules,
    socket: net.Socket,
    write: Encoder['write'],
  ) {
    const errors: string[] = [];

    if (!net.isIP(ip)) {
      gameDebug('invalid ip provided %s', ip);
      errors.push('Invalid "ip" specified');
    }
    this.ip = ip;

    if (port < 0 || port > 65535) {
      gameDebug('invalid port provided %d', port);
      errors.push('Invalid "port" specified. Must be between [0, 65535]');
    }
    this.port = port;

    if (!game) {
      errors.push('Invalid "game" specified');
    }
    this.game = game;

    if (!rules || !rules.minPlayers || !rules.maxPlayers) {
      errors.push(
        'Invalid "rules" specified. MustContain "minPlayers" and "maxPlayers"',
      );
    }
    this.rules = rules;
    this.socket = socket;
    this.write = write;
    this.waitTime = this.rules.waitTime || 30;
    this.lobby = {
      leader: undefined,
      clients: new Set([]),
    };

    if (errors.length > 0) {
      throw new Error(errors.join(', '));
    }

    // If the socket disconnects before ready kill server
    this.socket.on('end', () => {
      gameDebug('server disconnected');
      if (!this.isReady()) {
        this.kill();
      }
      // TODO: Handle if server is ready
    });

    const myGameServers = GameServer.servers[this.game];
    if (myGameServers) {
      myGameServers.add(this);
    } else {
      GameServer.servers[this.game] = new Set<GameServer>([this]);
    }
  }

  /**
   * Find a connected game server by its game identifier.
   *
   * @param game - The game identifier
   *
   * @return {GameServer | undefined} The found game server or undefined.
   */
  public static FIND(game: string): GameServer | undefined {
    const myGameServers: Set<GameServer> = GameServer.servers[game];

    if (!myGameServers) {
      return undefined;
    }

    return Array.from(myGameServers).sort((a: GameServer, b: GameServer) => {
      return a.lobby.clients.size > b.lobby.clients.size ? -1 : 1;
    })[0];
  }

  /**
   * Delete the current game server from the list of all game servers.
   */
  // tslint:disable-next-line:no-reserved-keywords
  public delete() {
    GameServer.servers[this.game].delete(this);
  }

  /**
   * Add a client to the lobby for the game server.
   *
   * @param client - The client representation to add.
   */
  public addClient(client: IClient) {
    gameDebug('adding client to server');
    if (!this.lobby.leader) {
      gameDebug('new client is now lobby leader');
      this.lobby.leader = client;
    }
    this.lobby.clients.add(client);
    client.write(VALID_CLIENT_CONFIG);
    client.socket.pause();

    client.socket.on('end', () => {
      log.verbose(
        'Game',
        `Client (${client.configuration.id}) disconnected before finished`,
      );
      this.removeClient(client, false);
    });

    if (this.isReady() && this.waiting === undefined) {
      gameDebug('lobby is ready, waiting for max players or wait time');
      // Wait for players to join
      this.waiting = Promise.race([
        this.maxPlayersReached(),
        this.notEnoughPlayers(),
      ])
        .then((success: boolean) => {
          if (success) {
            gameDebug('lobby complete or waiting, finishing connection');

            this.finish();
          } else {
            gameDebug('lobby incomplete, waiting for more players to connect');
            this.waiting = undefined;
          }
        })
        .catch((error: Error) => {
          gameDebug('error intializing lobby, %s', error.name);
        });
    }
  }

  /**
   * Remove a client from the lobby for the game server.
   *
   * @param client - The client representation to remove.
   * @param kick - If the client should be sent a 'kick' message.
   */
  public removeClient(client: IClient, kick: boolean = false) {
    gameDebug('removing client from server');
    this.lobby.clients.delete(client);

    if (client === this.lobby.leader) {
      gameDebug('removed client was lobby leader, replacing if possible');
      this.lobby.leader =
        this.lobby.clients.size > 0
          ? Array.from(this.lobby.clients)[0]
          : undefined;
    }

    if (kick) {
      gameDebug('kicked client %s', client.configuration.id);
      client.write(KICK_MESSAGE);
    }
    client.socket.destroy();
  }

  /**
   * Broadcast a message to all clients.
   *
   * @param message - The message to broadcast.
   * @param kick - If the clients should be kicked after the message is sent.
   * @param pause - If the sockets for each client should be paused after the
   *                message is send
   */
  public notifyClients(
    message: object,
    kill: boolean = false,
    pause: boolean = false,
  ) {
    gameDebug('notifiying clients%s', kill ? ' and killing connections' : '');
    for (const client of this.lobby.clients) {
      client.socket.resume();
      client.write(message);

      if (pause) {
        client.socket.pause();
      }

      if (kill) {
        client.socket.end();
      }
    }
  }

  /**
   * Kill the game server, cleaning up after itself by disconnecting all
   * clients, deleting itself from the game server list, and destroying the
   * socket.
   */
  public kill() {
    gameDebug('killing gameserver');
    this.notifyClients(GAME_SERVER_DISCONNECTED, true);
    this.delete();
    this.socket.destroy();
  }

  /**
   * Determines if a game is ready to be played by the number of clients.
   *
   * @returns {boolean} If the game is ready
   */
  public isReady(): boolean {
    const numClients: number = this.lobby.clients.size;

    return (
      numClients >= this.rules.minPlayers && numClients <= this.rules.maxPlayers
    );
  }

  /**
   * Finish the matchmaking process by notifying all clients and the server that
   * there was a match found, proxying the clients to the server, and then
   * cleaning up the game server.
   */
  public finish() {
    gameDebug('finishing matchmaking process');
    log.info('MM-Server', `${this.game} found a match!`);
    const connectionMessage = {
      ...MATCH_FOUND,
      ip: this.ip,
      port: this.port,
    };
    const serverConnectionMessage = {
      ...MATCH_FOUND,
      clients: Array.from(this.lobby.clients).map(
        (c: IClient) => c.configuration.id,
      ),
    };

    this.proxyClients();
    this.notifyClients(connectionMessage);
    this.write(serverConnectionMessage);
    this.delete();
    this.socket.end();
  }

  /**
   * Helper function to clear an interval call after a set timeout.
   *
   * @param resolve - The upper level promise to resolve
   * @param interval - The interval associated with the setInterval call
   */
  private setIntervalTimeout(resolve: Function, interval: NodeJS.Timeout) {
    return setTimeout(() => {
      clearInterval(interval);

      return resolve(true);
    }, this.waitTime * 1000);
  }

  /**
   * Proxy the connection for all clients in the lobby to the gameserver
   * server.
   */
  private proxyClients(): void {
    for (const client of this.lobby.clients) {
      client.socket.resume();
      const proxy: net.Socket = new net.Socket().connect(
        this.port,
        this.ip,
      );

      proxy
        .pipe(client.socket)
        .on('error', (err: Error) => {
          log.warn(
            'MM-Server',
            `An error occurred within the client-server proxy:\n${err.name}: ${
              err.message
            }\n${err.stack}`,
          );
        })
        .pipe(proxy)
        .on('error', (err: Error) => {
          log.warn(
            'MM-Server',
            `An error occurred within the client-server proxy:\n${err.name}: ${
              err.message
            }\n${err.stack}`,
          );
        });

      client.socket.on('end', () => {
        log.verbose('MM-Server', `Client ended for ${client.configuration.id}`);
      });

      proxy.on('end', () => {
        log.verbose('MM-Server', `Proxy ended for ${client.configuration.id}`);
      });
      client.socket.setKeepAlive(true, 1000);
      proxy.setKeepAlive(true, 1000);
    }
  }

  /**
   * Promise resolving if all the maximum number of players for the game has
   * been reached.
   */
  private async maxPlayersReached(): Promise<boolean> {
    return new Promise((resolve: Function) => {
      const interval: NodeJS.Timeout = setInterval(() => {
        if (this.lobby.clients.size === this.rules.maxPlayers) {
          gameDebug('max players reached');
          clearInterval(interval);

          return resolve(true);
        }
      }, 2000);

      return this.setIntervalTimeout(resolve, interval);
    });
  }

  /**
   * Promise resolving if the lobby has gone under the minimum number of players
   * for the game.
   */
  private async notEnoughPlayers(): Promise<boolean> {
    return new Promise((resolve: Function) => {
      const interval: NodeJS.Timeout = setInterval(() => {
        if (!this.isReady()) {
          gameDebug('not enough players');
          clearInterval(interval);

          return resolve(false);
        }
      }, 2000);

      return this.setIntervalTimeout(resolve, interval);
    });
  }
}
