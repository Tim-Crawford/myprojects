// The JSON schema generator we're using doesn't support `unknown` yet, so `any` is being used instead
// tslint:disable: no-any

/**
 * Sent to ask the client to identify itself.
 */
interface IOutboundWhoIs {
    messageType: "whois";
    data: {
        /**
         * The game server's ID for this client.
         */
        id: number;
    };
}

/**
 * Received when a client wants to update its own information.
 */
interface IInboundClientInfo {
    messageType: "client-info";
    data: {
        /**
         * This client's information about itself.
         */
        clientInfo: any;
    };
}

/**
 * Sent to all clients when a client's information is updated or when it has connected and identified itself.
 */
interface IOutboundClientInfo {
    messageType: "client-info";
    data: {
        /**
         * The game server's ID for this client.
         */
        id: number;

        /**
         * This client's information about itself.
         */
        clientInfo: any;

        /**
         * Whether this client is a lobby leader.
         */
        isLobbyLeader: boolean;
    };
}

/**
 * Received whenever a client wants to update the game state or when the game is started.
 */
interface IInboundGameState {
    messageType: "game-state";
    data: {
        /**
         * The requested game state.
         */
        state: any;
    };
}

/**
 * Sent to all clients when the game state has been updated.
 */
interface IOutboundGameState {
    messageType: "game-state";
    data: {
        /**
         * The current actual game state.
         */
        state: any;

        /**
         * This lobby's leader.
         */
        lobbyLeader: number;
    };
}

/**
 * Received when a client wants to stop the game.
 */
interface IInboundGameFinished {
    messageType: "game-finished";
    data?: { };
}

/**
 * Sent when the game has stopped.
 */
interface IOutboundGameFinished {
    messageType: "game-finished";
    data: { }
}

/**
 * Sent when the server is about to close the connection.
 */
interface IOutboundDisconnect {
    messageType: "disconnect";
    data: { }
}

/**
 * Received when a client wants a list of all the connected clients.
 */
interface IInboundClientList {
    messageType: "client-list";
    data?: { };
}

/**
 * Sent when the server is giving a client a list of connected clients.
 */
interface IOutboundClientList {
    messageType: "client-list";
    data: {
        /**
         * The game server's ID for this client.
         */
        id: number;
        
        /**
         * This client's information about itself.
         */
        clientInfo: any;

        /**
         * Whether this client is a lobby leader.
         */
        isLobbyLeader: boolean;
    }[];
}

/**
 * Sent whenever a client disconnects from the server.
 */
interface IOutboundClientDisconnected {
    messageType: "client-disconnected"
    data: {
        /**
         * The game server's ID for this client.
         */
        id: number;
        
        /**
         * This client's information about itself.
         */
        clientInfo: any;
    }
}

/**
 * Received when a client wants to broadcast random, unchecked data.
 */
interface IInboundRandomData {
    messageType: "random-data";
    data: any;
}

/**
 * Sent when random data has been received by a client.
 */
interface IOutboundRandomData {
    messageType: "random-data";
    data: any;
}

/**
 * Sent to a client when an error occurs with processing a message from it.
 */
interface IOutboundError {
    messageType: "error";
    data: {
        /**
         * The reason the error occurred. This is defined by the protocol.
         */
        reason: ErrorReason;

        /**
         * A user friendly description of the error message.
         */
        message: string;
        
        /**
         * The current actual game state.
         */
        state: any;
    };
}

/**
 * The reason an error occurs.
 */
export type ErrorReason = "invalid message format" | "invalid state format" | "invalid client information format" | "game already running" | "not enough clients" | "too many clients" | "clients not ready" | "state rejected" | "unexpected message" | "server error";

/**
 * The expected structure of messages that are sent by the server to clients.
 */
export type OutboundData = IOutboundWhoIs | IOutboundClientInfo | IOutboundGameState | IOutboundGameFinished | IOutboundDisconnect | IOutboundClientList | IOutboundClientDisconnected | IOutboundRandomData | IOutboundError;

/**
 * The expected structure of messages that are sent by clients to the server.
 */
export type InboundData = IInboundClientInfo | IInboundGameState | IInboundGameFinished | IInboundClientList | IInboundRandomData;