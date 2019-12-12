import { IClientConfiguration } from './Client';
import { IServerConfiguration } from './GameServer';

/**
 * Message structure the client or game server must send in the initial
 * connection as the 'data' attribute.
 */
export interface IConnectionData {
  configuration: IClientConfiguration & IServerConfiguration;
  game: string;
  clientType: 'client' | 'server';
}

/**
 * Message structure the client or game server must send in the connection
 * message
 */
export interface IConnectionRequest {
  messageType: 'connect';
  data: IConnectionData;
}
