namespace Gsnll.Models.GameServer.Incoming
{
    internal sealed class GameServerIncomingClientDisconnectedMessage<TClientInfo> : GameServerIncomingMessage, IMessageWithData<GameServerIncomingClientDisconnectedMessage<TClientInfo>.MessageData>
    {
        public MessageData Data { get; }

        public GameServerIncomingClientDisconnectedMessage(int id, TClientInfo clientInfo) : base("client-disconnected")
        {
            this.Data = new MessageData(id, clientInfo);
        }

        public sealed class MessageData
        {
            public int Id { get; }
            public TClientInfo ClientInfo { get; }

            public MessageData(int id, TClientInfo clientInfo)
            {
                this.Id = id;
                this.ClientInfo = clientInfo;
            }
        }
    }
}