import { GameServer } from "./game-server";
import { Logger, LogLevel, NpmLogOutputStream } from "./logger";
import { PassthroughGameRules } from "./rules/passthrough";

// Initialization
const logger: Logger = new Logger();
// logger.addOutputStream(new ConsoleLoggingOutputStream(), LogLevel.Trace);
logger.addOutputStream(new NpmLogOutputStream(), LogLevel.Trace);
logger.info("Initializing server");

// Parse arguments
// const parser = new ArgumentParser({
//     version: "0.1",
//     description: "General game server without state validation",
//     addHelp: true
// });
//
// parser.addArgument(["-p", "--port"], {
//     help: "The port the game server will listen to.",
//     defaultValue: () => 8008,
//     type: "number"
// });
//
// parser.addArgument(["-n", "--name"], {
//     help: "The name of the game.",
//     type: "string"
// });
//
// const args = parser.parseArgs() as {
//     port: number;
//     name?: string;
// };

// Create the game server
const gameServer: GameServer<unknown, unknown> = new GameServer(
    "default",
    logger,
    new PassthroughGameRules("echo", 2, 4),
);
gameServer
    .listen()
    .catch(reason => logger.error(`An error occurred: ${reason}`));
