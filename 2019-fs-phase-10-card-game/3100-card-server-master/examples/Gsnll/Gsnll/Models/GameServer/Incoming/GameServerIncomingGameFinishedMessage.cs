namespace Gsnll.Models.GameServer.Incoming
{
    internal sealed class GameServerIncomingGameFinishedMessage : GameServerIncomingMessage
    {
        public GameServerIncomingGameFinishedMessage() : base("game-finished") { }
    }
}