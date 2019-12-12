namespace Gsnll.Models.GameServer.Incoming
{
    internal sealed class GameServerIncomingWhoisMessage : GameServerIncomingMessage, IMessageWithData<GameServerIncomingWhoisMessage.MessageData>
    {
        public MessageData Data { get; }

        public GameServerIncomingWhoisMessage(int id) : base("whois")
        {
            this.Data = new MessageData(id);
        }

        public sealed class MessageData
        {
            public int Id { get; }

            public MessageData(int id)
            {
                this.Id = id;
            }
        }
    }
}