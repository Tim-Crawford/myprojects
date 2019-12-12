import * as net from "net";
import { Readable, Writable } from "stream";

/**
 * Representation of a player's client state.
 */
export type ClientState<TClientInfo> =
    | {
          stateName: "connecting";
      }
    | {
          stateName: "ready";
          info: TClientInfo;
      }
    | {
          stateName: "playing";
          info: TClientInfo;
      };

/**
 * Representation of a player's client attributes.
 */
export type Client<TClientInfo> = {
    id: number;
    socket: net.Socket;
    inStream: Readable;
    outStream: Writable;
    state: ClientState<TClientInfo>;
};