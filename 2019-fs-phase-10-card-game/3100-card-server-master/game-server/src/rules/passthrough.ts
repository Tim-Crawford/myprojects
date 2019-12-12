import { IGameRules } from "../game-rules";

/**
 * Game rules without state validation.
 */
export class PassthroughGameRules implements IGameRules<unknown, unknown> {
    /**
     * The title of the game type.
     */
    public readonly gameName: string;
    
    /**
     * The minimum amount of players required to start.
     */
    public readonly minPlayers: number;
    
    /**
     * The maximum amount of players allowed in the game mode.
     */
    public readonly maxPlayers: number;
    
    /**
     * A list of validators to move to the next transition.
     */
    public readonly transitionValidators: ((prev: unknown, next: unknown) => unknown)[];

    public constructor(gameName: string, minPlayers: number, maxPlayers: number) {
        this.gameName = gameName;
        this.minPlayers = minPlayers;
        this.maxPlayers = maxPlayers;
        this.transitionValidators = [(_, next) => next];
    }

    /**
     * Determines if the given object adheres to the state schema. (Always true for a passthrough validator)
     * @param raw The raw object being validated
     * @return If the given object adheres to the state schema. (Always true for a passthrough validator)
     */
    public isState(_: unknown): _ is unknown {
        return true;
    }

    /**
     * Determines if the given object adheres to the client info schema. (Always true for a passthrough validator)
     * @param raw The raw object being validated
     * @return If the given object adheres to the client info schema. (Always true for a passthrough validator)
     */
    public isClientInfo(_: unknown): _ is unknown {
        return true;
    }
}