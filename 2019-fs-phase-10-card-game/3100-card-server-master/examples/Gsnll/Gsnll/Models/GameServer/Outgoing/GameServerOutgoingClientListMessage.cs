namespace Gsnll.Models.GameServer.Outgoing
{
    internal sealed class GameServerOutgoingClientListMessage : GameServerOutgoingMessage
    {
        public GameServerOutgoingClientListMessage() : base("client-list") { }
    }
}