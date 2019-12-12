import { GameServer } from "../src/game-server";
import { ConsoleLoggingOutputStream, Logger, LogLevel } from "../src/logger";
import { PassthroughGameRules } from "../src/rules/passthrough";

describe("game server", async () => {
    const logger = new Logger();
    logger.addOutputStream(new ConsoleLoggingOutputStream(), LogLevel.Trace);
    const server = new GameServer("test", logger, new PassthroughGameRules("test", 2, 2));

    it("starts", async () => {
        await server.listen();
        expect(server.isRunning).toBe(true);
    });

    it("stops", async () => {
        await server.stop();
        expect(server.isRunning).toBe(false);
    });
});
