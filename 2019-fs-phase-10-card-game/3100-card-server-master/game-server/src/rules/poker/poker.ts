import { ICard } from "../common-cards"; 
import { CommonGameRules } from "../common-game-rules";
import pokerClientInfoSchemaJson from "./poker-client-info.schema.json";
import pokerStateInfoSchemaJson from "./poker-state-info.schema.json";

interface IHand {
  cards: ICard[]
  bet: number;
}

interface IGameOptions {
  decks: number;
}

export interface IPokerState {
  stage: string,
  state: {
    players: {
      [id: number]: {
        hand: IHand;
        initialBet: number;
      };
    };
    global: {
      activePlayer: number;
      deck: ICard[];
      tableCards: ICard[];
      options: IGameOptions;
    };
  },
  messages?: string[];
}

export interface IPokerClientInfo {
  name: string;
  money: number;
}

/**
 * Game rules for Poker.
 */
export class PokerGameRules extends CommonGameRules<IPokerState, IPokerClientInfo> {
  public readonly transitionValidators: ((prev: IPokerState | undefined, next: IPokerState) => IPokerState | undefined)[];

  public constructor() {
    super("Poker", 2, Infinity, pokerStateInfoSchemaJson, pokerClientInfoSchemaJson)

    this.transitionValidators = [
      (_, next) => next
    ]
  }
}