namespace Gsnll.Models.GameServer.Incoming
{
    internal abstract class GameServerIncomingMessage : IGameServerIncomingMessage
    {
        public string MessageType { get; }

        protected GameServerIncomingMessage(string messageType) {
            this.MessageType = messageType;
        }
    }
}
