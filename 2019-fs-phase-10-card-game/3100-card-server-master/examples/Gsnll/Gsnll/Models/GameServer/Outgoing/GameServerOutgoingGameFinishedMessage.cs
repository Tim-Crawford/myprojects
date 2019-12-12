namespace Gsnll.Models.GameServer.Outgoing
{
    internal sealed class GameServerOutgoingGameFinishedMessage : GameServerOutgoingMessage
    {
        public GameServerOutgoingGameFinishedMessage() : base("game-finished") { }
    }
}