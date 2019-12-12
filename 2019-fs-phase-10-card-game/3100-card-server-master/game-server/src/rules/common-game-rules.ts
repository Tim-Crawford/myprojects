import * as Ajv from "ajv";
import { IGameRules } from "../game-rules";

/**
 * Common base class for game rules using ajv to validate a schema for the game state and client information.
 */
export abstract class CommonGameRules<TState, TClientInfo> implements IGameRules<TState, TClientInfo> {

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
    public abstract readonly transitionValidators: ((prev: TState | undefined, next: TState) => TState | undefined)[];

    private readonly gameStateValidator: Ajv.ValidateFunction;
    private readonly clientInfoValidator: Ajv.ValidateFunction;

    protected constructor(gameName: string, minPlayers: number, maxPlayers: number, stateSchema: object | boolean, clientInfoSchema: object | boolean) {
        this.gameName = gameName;
        this.minPlayers = minPlayers;
        this.maxPlayers = maxPlayers;

        const ajv = new Ajv();
        this.gameStateValidator = ajv.compile(stateSchema);
        this.clientInfoValidator = ajv.compile(clientInfoSchema);
    }

    /**
     * Determines if the given object adheres to the state schema.
     * @param raw The raw object being validated
     * @return If the given object adheres to the state schema.
     */
    public isState(raw: unknown): raw is TState {
        return !!this.gameStateValidator(raw);
    }

    /**
     * Determines if the given object adheres to the client info schema.
     * @param raw The raw object being validated
     * @return If the given object adheres to the client info schema.
     */
    public isClientInfo(raw: unknown): raw is TClientInfo {
        return !!this.clientInfoValidator(raw);
    }
}