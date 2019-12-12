import { Client } from "./game-client";

/**
 * Defines a validator for a specific game mechanic.
 */
export class GameTransitionValidator<TState, TClientInfo> {

    /**
     * The description of the validated mechanic
     */
    public readonly description: string;

    /**
     * Transitions the previous state into the next state.
     * @returns the next state or the reason for which the transition was rejected.
     */
    public readonly transition: (client: Client<TClientInfo>, prev: TState | undefined, next: TState) => TState | string;
    
    /**
     * Constructs a new transition validator.
     * @param description The description of what this function is supposed to validate.
     * @param transition The transition tri-function.
     */
    public constructor(description: string, transition: (client: Client<TClientInfo>, prev: TState | undefined, next: TState) => TState | string) {
        this.description = description;
        this.transition = transition;
    }
    
}