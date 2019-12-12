import { Encoder } from 'fringe';
import * as net from 'net';

export type ConnectionType = 'server' | 'client';

/**
 * Data the client can configure with the initial connection message.
 */
export interface IClientConfiguration {
  id?: string;
}

/**
 * The Matchmaking server client representation.
 */
export interface IClient {
  socket: net.Socket;
  write: Encoder['write'];
  game: string;
  configuration: IClientConfiguration;
}
