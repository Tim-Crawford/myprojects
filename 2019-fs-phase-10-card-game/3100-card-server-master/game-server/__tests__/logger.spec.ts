const consoleSpy = jest.spyOn(global.console, "log");
import { ConsoleLoggingOutputStream, Logger, LogLevel } from "../src/logger";

describe("console logger", () => {
    const expectedMessage = "test message";

    // Test every output level
    for (const level of [LogLevel.Trace, LogLevel.Debug, LogLevel.Info, LogLevel.Warn, LogLevel.Error]) {
        test(`writes to the console at level ${level}`, () => {
            const logger = new Logger();
            logger.addOutputStream(new ConsoleLoggingOutputStream(), LogLevel.Trace);
            logger.log(level, expectedMessage);
            expect(consoleSpy).toBeCalledWith(expect.stringMatching(new RegExp(`(?:\\[(?:\\d+;)*\\d+m)?${expectedMessage}(?:\\[(?:\\d+;)*\\d+m)?`)));
        });
    }
})

describe("logger", () => {
    const loggingFunctions: [LogLevel, (logger: Logger, message: string | (() => string)) => void][] = [
        [LogLevel.Trace, (l, m) => l.trace(m)],
        [LogLevel.Debug, (l, m) => l.debug(m)],
        [LogLevel.Info, (l, m) => l.info(m)],
        [LogLevel.Warn, (l, m) => l.warn(m)],
        [LogLevel.Error, (l, m) => l.error(m)]
    ];

    for (const outputStreamData of loggingFunctions) {
        const logger: Logger = new Logger();
        let logged = false;
        const expectedMessage = "test message";

        // Add a mock output stream
        logger.addOutputStream({
            write: (l, m) => {
                expect(l).toBeGreaterThanOrEqual(outputStreamData[0]);
                expect(m).toBe(expectedMessage);
                logged = true;
            }
        }, outputStreamData[0]);

        for (const loggingFunction of loggingFunctions) {
            if (loggingFunction[0] >= outputStreamData[0]) {
                it(`writes "${expectedMessage}" (at logging level ${loggingFunction[0]}) to an output stream of level ${outputStreamData[0]} using the logging method for that level`, () => {
                    logged = false;
                    loggingFunction[1](logger, expectedMessage);
                    expect(logged).toBe(true);

                    logged = false;
                    loggingFunction[1](logger, () => expectedMessage);
                    expect(logged).toBe(true);
                });

                it(`writes "${expectedMessage}" (at logging level ${loggingFunction[0]}) to an output stream of level ${outputStreamData[0]} using Logger.log`, () => {
                    logged = false;
                    logger.log(loggingFunction[0], expectedMessage);
                    expect(logged).toBe(true);

                    logged = false;
                    logger.log(loggingFunction[0], () => expectedMessage);
                    expect(logged).toBe(true);
                });
            } else {
                it(`doesn't write "${expectedMessage}" (at logging level ${loggingFunction[0]}) to an output stream of level ${outputStreamData[0]} using the logging method for that level`, () => {
                    logged = false;
                    loggingFunction[1](logger, expectedMessage);
                    expect(logged).toBe(false);

                    logged = false;
                    loggingFunction[1](logger, () => expectedMessage);
                    expect(logged).toBe(false);
                });

                it(`doesn't write "${expectedMessage}" (at logging level ${loggingFunction[0]}) to an output stream of level ${outputStreamData[0]} using Logger.log`, () => {
                    logged = false;
                    logger.log(loggingFunction[0], expectedMessage);
                    expect(logged).toBe(false);

                    logged = false;
                    logger.log(loggingFunction[0], () => expectedMessage);
                    expect(logged).toBe(false);
                });
            }
        }

        it("clears all output streams", () => {
            logger.clearOutputStreams();
            logged = false;
            logger.error(expectedMessage);
            expect(logged).toBe(false);
        });
    }
});