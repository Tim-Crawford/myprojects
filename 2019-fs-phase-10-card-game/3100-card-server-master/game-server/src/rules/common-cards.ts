/**
 * The common suits.
 */
export type CardSuit = "spades" | "diamonds" | "hearts" | "clubs";

/**
 * The common values.
 */
export type CardFace = "A" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "10" | "J" | "Q" | "K";

/**
 * An abstract representation of a playing card.
 */
export interface ICard {
    suit: CardSuit;
    face: CardFace;
};