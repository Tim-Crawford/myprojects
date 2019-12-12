import * as Ajv from "ajv";
import { Encoder } from "fringe";
import * as missive from "missive";
import * as net from "net";
import { Client, ClientState } from "./game-client";
import { IGameRules } from "./game-rules";
import { ILogger } from "./logger";
import { ErrorReason, InboundData, OutboundData } from "./protocol";
import * as protocolInboundSchemaJson from "./protocol-inbound.schema.json";
import { TimeSpan } from "./util/time-span";

/**
 * Representation of a server endpoint.
 */
interface IServer {
    ip: string;
    port: number;
}

/**
 * The primary game server. This should manage all individual functions of the server.
 * @name GameServer
 */
export class GameServer<TState, TClientInfo> {
    /**
     * Whether the game server is currently running and listening for connections.
     */
    public get isRunning(): boolean {
        return this.server.listening;
    }

    /**
     * The address of this server.
     */
    public get address(): string | net.AddressInfo {
        return this.server.address();
    }

    /**
     * The port the game server is listening on.
     */
    public readonly port: number;

    public readonly name: string;
    private lobbyClosed: boolean;
    private readonly server: net.Server;
    private readonly logger: ILogger;
    private readonly rules: IGameRules<TState, TClientInfo>;
    private clients: Client<TClientInfo>[];
    private nextClientId: number = 0;
    private readonly mmServer: IServer;
    private gameState?: TState;
    private readonly inboundValidator: Ajv.ValidateFunction;
    private readonly idleTime: TimeSpan;

    /**
     * Creates a new game session.
     * @param name The name of the game server
     * @param logger The logger instance associated with the server
     * @param rules The game rules for the session
     * @param port The server port to be binded
     * @param mmServer The matchmaking server host
     */
    public constructor(name: string, logger: ILogger, rules: IGameRules<TState, TClientInfo>, port: number = 8008, mmServer: IServer = { ip: "127.0.0.1", port: 8000 }, idleTime: TimeSpan = new TimeSpan(undefined, undefined, 60)) {
        this.name = name;
        this.logger = logger;
        this.rules = rules;
        this.port = port;
        this.clients = [];
        this.inboundValidator = new Ajv().compile(protocolInboundSchemaJson);
        this.mmServer = mmServer;
        this.idleTime = idleTime;

        setTimeout(() => {
            this.logger.debug("hi");
        }, this.idleTime.totalMilliseconds);

        // Create the TCP server and assign events to it
        this.logger.info(`Creating game server for ${rules.gameName}.`);
        this.server = net
            .createServer()
            .on("connection", socket => {
                this.lobbyClosed = false;
                // Encode sent data
                const encodeStream = missive.encode();
                encodeStream.pipe(socket);

                // Parse received data
                const parsedStream = socket.pipe(missive.parse());

                // Create the client state
                const client: Client<TClientInfo> = {
                    id: this.nextClientId++,
                    socket: socket,
                    inStream: parsedStream,
                    outStream: encodeStream,
                    state: {
                        stateName: "connecting",
                    },
                };

                // Send keep-alive packets on inactivity
                socket.setKeepAlive(true, 1000);

                // Close socket after a long period of inactivity
                socket.setTimeout(120000, () => {
                    this.logger.warn(`Client ${client.id} timed out.`);
                    this.clientDisconnected(client).catch(r => `An error occurred: ${r}`);
                });

                // Make sure the client isn't joining a game that's running
                if (this.gameState !== undefined) {
                    // Reply with an error message
                    this.sendMessage(client, this.createError("game already running", "The game has already begun. New clients can't join a game in progress."))
                        .then(() => client.socket.destroy())
                        .catch(reason => this.logger.error(`Error disconnecting client: ${reason}`));

                    // Don't track this client since it's being rejected
                    return;
                }

                // Keep track of the client
                this.clients.push(client);

                // Listen for data from the client
                parsedStream
                    .on("data", (data: Buffer) => this.logger.trace(`Message from ${client.id}: ${data.toString()}`))
                    .on("message", data => this.messageReceived(client, data))
                    .on("end", () => this.clientDisconnected(client))
                    .on("close", () => this.clientDisconnected(client))
                    .on("error", reason => {
                        if (reason instanceof SyntaxError) {
                            this.sendMessage(client, this.createError("invalid message format", "The message failed to parse.")).catch(r => `An error occurred: ${r}`);
                        } else {
                            this.sendMessage(client, this.createError("server error", `${reason.name}: ${reason.message}\n${reason.stack}`)).catch(r => `An error occurred: ${r}`);
                        }
                    });

                // Ask the client who they are
                this.sendMessage(client, {
                    messageType: "whois",
                    data: {
                        id: client.id,
                    },
                }).catch(reason => this.logger.error(`Error sending message to client: ${reason}`));
            })
            .on("error", error => {
                // Track the error
                this.logger.error(`${error.name}: ${error.message}\n${error.stack}`);

                // Close the connection
                this.broadcastMessage(this.createError("server error", `An error occurred with the server. Please report this error to the server team.\n${error.name}: ${error.message}\n${error.stack}`))
                    .then(() => this.stop())
                    .catch(reason => this.logger.error(`Error stopping the server: ${reason}`));
            });

        if (this.rules.maxPlayers !== Infinity) {
            this.server.maxConnections = this.rules.maxPlayers;
        }

        this.register().catch(reason => this.logger.error(`An error occurred while registering with the matchmaking server: ${reason}`));
    }

    /**
     * Registers the game session with the matchmaking server,
     *  to be searched for by players.
     */
    public register(): Promise<boolean> {
        this.logger.info("Registering with matchmaking server");
        let socket: net.Socket;

        try {
            socket = new net.Socket().connect(
                this.mmServer.port,
                this.mmServer.ip,
            );
        } catch (e) {
            this.logger.error("Failed to connect to the matchmaking server");
            return Promise.resolve(false);
        }

        const config: object = {
            messageType: "connect",
            data: {
                clientType: "server",
                game: this.name,
                configuration: {
                    ip: "127.0.0.1",
                    port: this.port,
                    rules: this.rules,
                },
            },
        };

        const encode = missive.encode();
        encode.pipe(socket);
        encode.write(config);
        socket
            .pipe(missive.parse())
            // tslint:disable-next-line:no-reserved-keywords
            .once("message", (response: { type: string; message: string }) => {
                if (response.type === "error") {
                    this.logger.error("Could not connect to the matchmaking server");
                }
            });

        socket.on("close", (hadError: boolean) => {
            if (hadError) {
                this.logger.warn(`An error has occured between game server and matchmaking (Connection)`);
            } else if (this.clients.length === 0) {
                this.reconnectMM(socket, encode, config);
            }
        });

        return Promise.resolve(true);
    }

    public reconnectMM(socket: net.Socket, encode: Encoder, config: object) {
        let retries = 5;

        const interval = setInterval(() => {
            if (retries <= 0) {
                this.logger.warn("Failed to reconnect to matchmaking.");
                clearInterval(interval);
                this.stop()
                    .then(() => this.logger.info("Successfully shutdown the game server."))
                    .catch((e: Error) => this.logger.warn(`Error while attempting to shutdown server: ${e}`));
            } else {
                socket
                    .connect(
                        this.mmServer.port,
                        this.mmServer.ip,
                    )
                    .on("connect", () => {
                        this.logger.info(`Successfully reconnected to matchmaking on ${this.mmServer.ip}:${this.mmServer.port}`);
                        encode.pipe(socket);
                        encode.write(config);
                        clearInterval(interval);
                    })
                    .on("error", (e: Error) => {
                        this.logger.warn(`Error encountered when trying to reconnect: ${e}`);
                        this.logger.info(`Retries left: ${--retries}`);
                    });
            }
        }, 5000);
    }

    /**
     * Listens for client connections.
     */
    public listen(): Promise<void> {
        return new Promise((resolve, reject) => {
            let errorHandler: (error: Error) => void;

            // Handler for when the server starts listening
            const listeningHandler = () => {
                // Remove the handlers so they don't trigger anymore
                this.server.removeListener("listening", listeningHandler);
                this.server.removeListener("error", errorHandler);

                // Show message indicating the server is listening
                const serverAddress = this.server.address();
                if (typeof serverAddress === "string") {
                    this.logger.info(`Listening on ${serverAddress}...`);
                } else {
                    this.logger.info(`Listening on ${serverAddress.address}:${serverAddress.port}...`);
                }

                // Resolve the promise
                resolve();
            };

            // Handler for when the server throws an error
            errorHandler = error => {
                // Remove the handler so they don't trigger anymore
                this.server.removeListener("listening", listeningHandler);
                this.server.removeListener("error", errorHandler);

                // Reject the promise because there was an error
                reject(`An error occurred while the server was starting:\n${error.name}: ${error.message}\n${error.stack}`);
            };

            // Bind the handler
            this.server.on("error", errorHandler).listen(this.port, "127.0.0.1", undefined, listeningHandler);
        });
    }

    /**
     * Stops the server.
     */
    public async stop() {
        await this.broadcastMessage({ messageType: "disconnect", data: {} });
        await new Promise((resolve, reject) => {
            this.server.close(error => {
                if (error !== undefined) {
                    reject(error);
                } else {
                    resolve();
                }
            });
        });
    }

    /**
     * Checks if an object is a valid inbound message.
     * @param data The data being checked.
     * @returns { boolean } True if `data` is a valid `InboundData`.
     */
    private isValidInboundData(data: unknown): data is InboundData {
        return !!this.inboundValidator(data);
    }

    /**
     * Validates JSON data sent by a client and processes it if able.
     * @param client The client that sent the message.
     * @param inboundData The JSON data that was sent by the client.
     */
    private async messageReceived(client: Client<TClientInfo>, data: object) {
        // Make sure the client is being tracked
        if (this.clients.find(c => c.id === client.id) === undefined) {
            return;
        }

        // Deserialize the data that was sent by the client
        const inboundData: unknown = data as unknown;

        // Make sure the data is valid
        if (!this.isValidInboundData(inboundData)) {
            // Return an error
            await this.sendMessage(client, this.createError("invalid message format", "The message structure does not conform to the protocol."));

            // Ignore the message
            return;
        }

        try {
            // Process the data
            await this.processMessage(client, inboundData);
        } catch {
            // Return an error
            await this.sendMessage(client, this.createError("invalid message format", "The message is not valid JSON."));
        }
    }

    /**
     * Processes a message received by a client.
     * @param client The client that sent the message.
     * @param message The message the client received.
     */
    private async processMessage(client: Client<TClientInfo>, message: InboundData) {
        // Depending on the client state and message type, perform some action
        const clientState = client.state;
        switch (clientState.stateName) {
            case "connecting":
                switch (message.messageType) {
                    case "client-info":
                        // Validate the client information that was received
                        const clientInfo: unknown = message.data.clientInfo as unknown;
                        if (!this.rules.isClientInfo(clientInfo)) {
                            await this.sendMessage(client, this.createError("invalid client information format", "The received client information does not conform to the expected format for this game."));
                            return;
                        }

                        // Update the client's state
                        await this.updateClient(client, {
                            stateName: "ready",
                            info: clientInfo,
                        });
                        return;

                    case "random-data":
                        // Broadcast the random data
                        await this.broadcastMessage({
                            messageType: "random-data",
                            data: message.data,
                        });
                        return;

                    default:
                        // Message type is invalid
                        await this.sendMessage(client, this.createError("unexpected message", `The given message was unexpected for a client in state "${clientState.stateName}".`));
                        return;
                }

            case "ready":
                switch (message.messageType) {
                    case "client-info":
                        // Validate the client information that was received
                        const clientInfo: unknown = message.data.clientInfo as unknown;
                        if (!this.rules.isClientInfo(clientInfo)) {
                            await this.sendMessage(client, this.createError("invalid client information format", "The received client information does not conform to the expected format for this game."));
                            return;
                        }

                        // Update the client's state
                        await this.updateClient(client, {
                            stateName: clientState.stateName,
                            info: clientInfo,
                        });
                        return;

                    case "client-list":
                        const clients: { id: number; clientInfo: TClientInfo; isLobbyLeader: boolean }[] = [];

                        // Create a list of all the connected clients
                        for (const c of this.clients) {
                            if (c.state.stateName === "connecting") {
                                continue;
                            }

                            clients.push({
                                id: c.id,
                                clientInfo: c.state.info,
                                isLobbyLeader: c === this.clients[0],
                            });
                        }

                        // Send the client list
                        await this.sendMessage(client, {
                            messageType: "client-list",
                            data: clients,
                        });
                        return;

                    case "game-state":
                        // Make sure there are enough connected players
                        if (this.clients.length < this.rules.minPlayers) {
                            await this.sendMessage(client, this.createError("not enough clients", `${this.clients.length} player(s) are connected.`));
                            return;
                        }

                        // Make sure there aren't too many connected players
                        if (this.clients.length > this.rules.maxPlayers) {
                            await this.sendMessage(client, this.createError("too many clients", `${this.clients.length} players are connected.`));
                            return;
                        }

                        // Make sure everybody is ready
                        const notReadyClients = this.clients.filter(c => c.state.stateName !== "ready").length;
                        if (notReadyClients > 0) {
                            await this.sendMessage(client, this.createError("clients not ready", `${notReadyClients} client(s) are not ready to start.`));
                            return;
                        }

                        // Validate the requested state
                        const response = this.validateState(message.data.state as unknown);
                        if (!response.success) {
                            await this.sendMessage(client, this.createError(response.reason, response.message));
                            return;
                        }

                        // Update each connected client's state
                        for (const curClient of this.clients) {
                            const curState = curClient.state;

                            // This check is redundant but restricts the client's state type
                            if (curState.stateName !== "ready") {
                                this.logger.warn(`Client isn't ready when ${message.messageType} was received.`);
                                continue;
                            }

                            // Update the client's state to "playing"
                            await this.updateClient(curClient, {
                                stateName: "playing",
                                info: curState.info,
                            });
                        }

                        // Update the game state
                        this.gameState = response.newState;
                        await this.broadcastMessage({
                            messageType: "game-state",
                            data: {
                                state: response.newState,
                                lobbyLeader: this.clients[0].id,
                            },
                        });
                        return;

                    case "random-data":
                        // Broadcast the random data
                        await this.broadcastMessage({
                            messageType: "random-data",
                            data: message.data,
                        });
                        return;

                    default:
                        // Message type is invalid
                        await this.sendMessage(client, this.createError("unexpected message", `The given message was unexpected for a client in state "${clientState.stateName}".`));
                        return;
                }

            case "playing":
                switch (message.messageType) {
                    case "client-info":
                        // Validate the client information that was received
                        const clientInfo: unknown = message.data.clientInfo as unknown;
                        if (!this.rules.isClientInfo(clientInfo)) {
                            await this.sendMessage(client, this.createError("invalid client information format", "The received client information does not conform to the expected format for this game."));

                            return;
                        }

                        // Update the client's state
                        await this.updateClient(client, {
                            stateName: clientState.stateName,
                            info: clientInfo,
                        });
                        return;

                    case "client-list":
                        const clients: { id: number; clientInfo: TClientInfo; isLobbyLeader: boolean }[] = [];

                        // Create a list of all the connected clients
                        for (const c of this.clients) {
                            if (c.state.stateName === "connecting") {
                                continue;
                            }

                            clients.push({
                                id: c.id,
                                clientInfo: c.state.info,
                                isLobbyLeader: c === this.clients[0],
                            });
                        }

                        // Send the client list
                        await this.sendMessage(client, {
                            messageType: "client-list",
                            data: clients,
                        });
                        return;

                    case "game-state":
                        // Validate the requested state
                        const response = this.validateState(message.data.state as unknown);
                        if (!response.success) {
                            await this.sendMessage(client, this.createError(response.reason, response.message));
                            return;
                        }

                        // Update the game state
                        this.gameState = response.newState;

                        // Notify the clients
                        await this.broadcastMessage({
                            messageType: "game-state",
                            data: {
                                state: response.newState,
                                lobbyLeader: this.clients[0].id,
                            },
                        });
                        return;

                    case "game-finished":
                        await this.endGame();
                        return;

                    case "random-data":
                        // Broadcast the random data
                        await this.broadcastMessage({
                            messageType: "random-data",
                            data: message.data,
                        });
                        return;

                    default:
                        // Message type is invalid
                        await this.sendMessage(client, this.createError("unexpected message", "This message type was not expected."));
                        return;
                }

            default:
                // Client state is invalid somehow
                await this.sendMessage(client, this.createError("unexpected message", "The client is in an invalid state. Please report this as a bug to the server team as well as the steps you took to get to here."));
                return;
        }
    }

    /**
     * Called whenever a client disconnects from the server.
     * @param client The client that disconnected.
     */
    private async clientDisconnected(client: Client<TClientInfo>) {
        this.logger.warn(`Client ${client.id} disconnected during play.`);

        // Close the socket
        client.socket.end();
        client.socket.destroy();

        // Make sure the client is being tracked
        if (this.clients.find(c => c.id === client.id) === undefined) {
            return;
        }

        // Stop tracking the client
        this.clients = this.clients.filter(c => c.id !== client.id);

        // Make sure enough players are still playing
        if (this.clients.length < this.rules.minPlayers && !this.lobbyClosed) {
            await this.endGame();
        }
    }

    /**
     * Ends the game. This does not update any clients.
     */
    private async endGame() {
        // Update each connected client's state
        if (this.lobbyClosed) {
            this.logger.warn("Ending game has already been initiated.");
            return;
        }

        this.logger.info("Ending the game.");
        this.lobbyClosed = true;

        // Update the game's state
        this.gameState = undefined;

        // Let everyone know the game has finished
        await this.broadcastMessage({
            messageType: "game-finished",
            data: {},
        });

        // Tell all clients to disconnect
        await this.broadcastMessage({
            messageType: "disconnect",
            data: {},
        });

        for (const curClient of this.clients) {
            this.logger.warn(`Disconnecting client ${curClient.id}.`);
            curClient.socket.end();
            curClient.socket.destroy();
        }

        // Clear the clients array
        this.clients = [];
        await this.register();
    }

    /**
     * Updates a client's state.
     * @param client The client which should have its state updated.
     * @param newState The new state for the client.
     */
    private async updateClient(client: Client<TClientInfo>, newState: ClientState<TClientInfo>) {
        this.logger.info(`Updating client ${client.id}'s state from ${client.state.stateName} to ${newState.stateName}.`);

        // Update the client's state internally
        client.state = newState;

        // Let all the connected players know that a client's state has been updated (if relevant)
        if (newState.stateName === "ready") {
            await this.broadcastMessage({
                messageType: "client-info",
                data: {
                    id: client.id,
                    clientInfo: newState.info,
                    isLobbyLeader: client === this.clients[0],
                },
            });
        }
    }

    /**
     * Checks if a requested state is valid.
     * @param requestedState The new state being requested.
     */
    private validateState(requestedState: unknown): { success: true; newState: TState } | { success: false; reason: ErrorReason; message: string } {
        // Check the structure of the requested state
        if (!this.rules.isState(requestedState)) {
            return {
                success: false,
                reason: "invalid state format",
                message: "The game state structure does not conform to the protocol.",
            };
        }

        // Validate the requested state
        for (const validator of this.rules.transitionValidators) {
            // Check if the requested state is valid or a valid state can be inferred from it
            const newState: TState | undefined = validator(this.gameState, requestedState);
            if (newState !== undefined) {
                // Success, don't create a response
                return {
                    success: true,
                    newState: newState,
                };
            }
        }

        // None of the validators accepted the requested state
        return {
            success: false,
            reason: "state rejected",
            message: "The requested state is not valid. The previous state has been provided for convenience.",
        };
    }

    /**
     * Creates an error message to send to a client.
     * @param reason The reason the error occurred.
     * @param message Extra information about the error.
     * @returns { OutboundData } The resulting message to send to clients.
     */
    private createError(reason: ErrorReason, message: string): OutboundData {
        return {
            messageType: "error",
            data: {
                reason: reason,
                message: message,
                state: this.gameState,
            },
        };
    }

    /**
     * Sends a message to a specific client.
     * @param client The client to send the message to.
     * @param message The message to send.
     */
    private sendMessage(client: Client<TClientInfo>, message: OutboundData): Promise<void> {
        this.logger.trace(() => `Sending message to ${client.id} of type "${message.messageType}": ${JSON.stringify(message)}`);

        // Write the message to the client's socket
        // tslint:disable-next-line: no-unnecessary-callback-wrapper
        return new Promise<void>((resolve, reject) =>
            client.outStream.write(message, response => {
                if (response instanceof Error) {
                    reject(response);
                }

                resolve();
            }),
        );
    }

    /**
     * Sends a message to all connected clients.
     * @param message The message to broadcast.
     */
    private async broadcastMessage(message: OutboundData) {
        this.logger.trace(`Broadcasting message: ${message.messageType}`);

        // Send the message to each client
        for (const client of this.clients) {
            await this.sendMessage(client, message);
        }
        // await Promise.all(this.clients.map(c => this.sendMessage(c, message)));
    }
}

