declare module "missive" {
    import { Parser, Encoder, MessageFormat } from "fringe";
    export function parse(opts?: Partial<MessageFormat> & { deflate?: boolean }): Parser;
    export function encode(opts?: Partial<MessageFormat> & { inflate?: boolean }): Encoder;
}