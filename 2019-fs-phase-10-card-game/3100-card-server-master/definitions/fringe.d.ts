declare module "fringe" {
    import { Transform, TransformCallback, TransformOptions } from "stream";

    type LengthFormat = "UInt8" | "UInt16BE" | "UInt16LE" | "UInt32BE" | "UInt32LE";

    type MessageFormat = {
        prefix: string;
        lengthFormat: LengthFormat;
        maxSize: number;
        lengthModifier: number;
    }

    export class Message {
        /**
         * Message constructor
         * @param opts formatting options
         */
        constructor(opts?: MessageFormat);

        /**
         * Reset the internal state so we can start consuming a message
         */
        reset(): void;

        /**
         * Is this message valid and complete?
         */
        readonly valid: boolean;

        /**
         * Convert the message to a buffer
         */
        toBuffer(): Buffer;

        /**
         * Consume a chunk into the internal buffer and return the number of
         * bytes you grabbed
         * @param chunk input buffer
         * @param offset read offset within the chunk
         */
        consume(chunk: Buffer, offset: number): number;

        /**
         * Encode a message into a buffer with prefix and length
         * @param payload message payload
         */
        encode(payload: Buffer | string): Buffer;
    }

    export class Encoder extends Transform {
        /**
         * Encoder constructor
         * @param format formatting options
         * @param opts stream options
         */
        constructor(format?: MessageFormat, opts?: TransformOptions);

        /**
         * Translate a message (e.g. JSON.stringify or convert to Protobuf)
         *
         * Intended to be overridden by encoder subclasses, must return a
         * String or Buffer.
         * @param message raw message
         */
        translate(message: unknown): string | Buffer;
    }

    export class Parser extends Transform {
        /**
         * Parser constructor
         * @param format formatting options
         * @param opts stream options
         */
        constructor(format?: MessageFormat, opts?: TransformOptions);

        on(event: "message", listener: (data: object) => void): this;
        on(event: "close", listener: () => void): this;
        on(event: "data", listener: (chunk: any) => void): this;
        on(event: "end", listener: () => void): this;
        on(event: "readable", listener: () => void): this;
        on(event: "error", listener: (err: Error) => void): this;
        on<TArgs extends unknown[]>(event: string | symbol, listener: (...args: TArgs) => void): this;

        /**
         * Push a full message and reset internal state
         */
        finish(): void;
    }
}