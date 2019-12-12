import { CommonGameRules } from "../common-game-rules";
import * as unoClientInfoSchemaJson from "./uno-client-info.schema.json";
import * as unoStateSchemaJson from "./uno-state.schema.json";

type CardColor = "red" | "yellow" | "green" | "blue";
type CardFace = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "reverse" | "skip" | "drawTwo" | "drawFour" | "wild";

interface ICard {
    color: CardColor | "wild";
    face: CardFace;
};

interface IHand {
    cards: ICard[];
}

interface IGameOptions {
    decks: number;
}

export interface IUnoState {
    stage: string,
    state: {
        players: {
            [id: number]: {
                hand: IHand;
            };
        };
        global: {
            activePlayer: number;
            deck: ICard[];
            topColor: CardColor;
            topFace: CardFace;
            options: IGameOptions;
        };
    },
    messages?: string[];
}

export interface IUnoClientInfo {
    name: string;
}

/**
 * Game rules for Uno.
 */
export class UnoGameRules extends CommonGameRules<IUnoState, IUnoClientInfo> {
    public readonly transitionValidators: ((prev: IUnoState | undefined, next: IUnoState) => IUnoState | undefined)[];

    public constructor() {
        super("Uno", 2, Infinity, unoStateSchemaJson, unoClientInfoSchemaJson);
        
        // Create state transition validators
        this.transitionValidators = [
           (_, next) => next
        ];
    }
}
