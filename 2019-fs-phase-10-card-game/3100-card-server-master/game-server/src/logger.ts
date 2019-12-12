import * as colors from "colors";
import * as npmlog from "npmlog";

export enum LogLevel {
    Trace,
    Debug,
    Info,
    Warn,
    Error,
}

export interface ILogger {
    /**
     * Logs a message.
     * @param level The logging level of the message.
     * @param message The message to log.
     */
    log(level: LogLevel, message: string | (() => string)): void;

    /**
     * Logs a trace message.
     * @param message The message to log.
     */
    trace(message: string | (() => string)): void;

    /**
     * Logs a debug message.
     * @param message The message to log.
     */
    debug(message: string | (() => string)): void;

    /**
     * Logs an info message.
     * @param message The message to log.
     */
    info(message: string | (() => string)): void;

    /**
     * Logs a warning message.
     * @param message The message to log.
     */
    warn(message: string | (() => string)): void;

    /**
     * Logs an error message.
     * @param message The message to log.
     */
    error(message: string | (() => string)): void;
}

export interface ILoggingOutputStream {
    write(level: LogLevel, message: string): void;
}

/**
 * Outputs messages to the console.
 */
export class ConsoleLoggingOutputStream implements ILoggingOutputStream {
    public write(level: LogLevel, message: string) {
        // tslint:disable-next-line: no-console
        console.log(this.color(level, message));
    }

    private color(level: LogLevel, message: string): string {
        switch (level) {
            case LogLevel.Trace:
                return colors.dim(message);
            case LogLevel.Debug:
                return colors.gray(message);
            case LogLevel.Info:
                return colors.reset(message);
            case LogLevel.Warn:
                return colors.yellow(message);
            case LogLevel.Error:
                return colors.bgRed(colors.white(message));
            default:
                return message;
        }
    }
}

/**
 * Outputs messages through npmlog.
 */
export class NpmLogOutputStream implements ILoggingOutputStream {
    public write(level: LogLevel, message: string): void {
        switch (level) {
            case LogLevel.Trace:
                npmlog.silly("Game Server", message);
                break;
            case LogLevel.Debug:
                npmlog.verbose("Game Server", message);
                break;
            case LogLevel.Info:
                npmlog.info("Game Server", message);
                break;
            case LogLevel.Warn:
                npmlog.warn("Game Server", message);
                break;
            case LogLevel.Error:
                npmlog.error("Game Server", message);
                break;
            default:
                npmlog.verbose("Game Server", message);
        }
    }
}

/**
 * Logs messages to the console.
 */
export class Logger implements ILogger {
    private outputStreams: [ILoggingOutputStream, LogLevel][];

    public constructor() {
        this.outputStreams = [];
    }

    public addOutputStream(stream: ILoggingOutputStream, level: LogLevel) {
        this.outputStreams.push([stream, level]);
    }

    public clearOutputStreams() {
        this.outputStreams = [];
    }

    public log(level: LogLevel, message: string | (() => string)) {
        let actualMessage: string | undefined;

        // Write the message to all applicable streams
        for (const outputStream of this.outputStreams) {
            if (level >= outputStream[1]) {
                // Generate the message if necessary (lazy)
                if (actualMessage === undefined) {
                    if (typeof message === "string") {
                        actualMessage = message;
                    } else {
                        actualMessage = message();
                    }
                }

                // Write the message to the stream
                outputStream[0].write(level, actualMessage);
            }
        }
    }

    public trace(message: string | (() => string)) {
        return this.log(LogLevel.Trace, message);
    }

    public debug(message: string | (() => string)) {
        return this.log(LogLevel.Debug, message);
    }

    public info(message: string | (() => string)) {
        return this.log(LogLevel.Info, message);
    }

    public warn(message: string | (() => string)) {
        return this.log(LogLevel.Warn, message);
    }

    public error(message: string | (() => string)) {
        return this.log(LogLevel.Error, message);
    }
}
