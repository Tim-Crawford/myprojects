/**
 * Defines rules for a specific game.
 */
export interface IGameRules<TState, TClientInfo> {
    /**
     * The name of the game.
     */
    readonly gameName: string;

    /**
     * The minimum number of players allowed in this game.
     */
    readonly minPlayers: number;

    /**
     * The maximum number of players allowed in this game.
     */
    readonly maxPlayers: number;

    /**
     * A collection of state transition validators. If any transition validator returns a state, the returned state is accepted. Otherwise, the new state is rejected. The previous state may be `undefined`, indicating that `next` is the initial state of the game.
     */
    readonly transitionValidators: ((prev: TState | undefined, next: TState) => TState | undefined)[];

    /**
     * Checks if a raw object is a valid state for this game.
     * @param raw The raw object which should be checked.
     */
    isState(raw: unknown): raw is TState;

    /**
     * Checks if a raw object is valid client information for this game.
     * @param raw The raw object which should be checked.
     */
    isClientInfo(raw: unknown): raw is TClientInfo;
}