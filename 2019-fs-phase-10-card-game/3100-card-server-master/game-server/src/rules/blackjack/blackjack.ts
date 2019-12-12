import { ICard } from "../common-cards";
import { CommonGameRules } from "../common-game-rules";
import * as blackjackClientInfoSchemaJson from "./blackjack-client-info.schema.json";
import * as blackjackStateSchemaJson from "./blackjack-state.schema.json";

interface IHand {
    cards: ICard[];
    bet: number;
}

interface IGameOptions {
    decks: number;
}

export interface IBlackjackState {
    stage: string,
    state: {
        players: {
            [id: number]: {
                hands: IHand[];
                initialBet: number;
            };
        };
        global: {
            activePlayer: number;
            deck: ICard[];
            options: IGameOptions;
        };
    },
    messages?: string[];
}

export interface IBlackjackClientInfo {
    name: string;
    money: number;
}

/**
 * Game rules for Blackjack.
 */
export class BlackjackGameRules extends CommonGameRules<IBlackjackState, IBlackjackClientInfo> {
    public readonly transitionValidators: ((prev: IBlackjackState | undefined, next: IBlackjackState) => IBlackjackState | undefined)[];
    
    public constructor() {
        super("Blackjack", 2, Infinity, blackjackStateSchemaJson, blackjackClientInfoSchemaJson);

        // Create state transition validators
        this.transitionValidators = [
           (_, next) => next
        ];
    }
}
