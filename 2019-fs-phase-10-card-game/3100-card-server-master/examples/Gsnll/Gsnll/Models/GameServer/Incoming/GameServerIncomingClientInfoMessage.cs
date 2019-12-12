namespace Gsnll.Models.GameServer.Incoming
{
    internal sealed class GameServerIncomingClientInfoMessage<TClientInfo> : GameServerIncomingMessage, IMessageWithData<GameServerIncomingClientInfoMessage<TClientInfo>.MessageData>
    {
        public MessageData Data { get; }

        public GameServerIncomingClientInfoMessage(int id, TClientInfo clientInfo) : base("client-info")
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