namespace Gsnll.Models.GameServer.Incoming
{
    internal sealed class GameServerIncomingDisconnectMessage : GameServerIncomingMessage
    {
        public GameServerIncomingDisconnectMessage() : base("disconnect") { }
    }
}