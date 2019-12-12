using Newtonsoft.Json;

namespace Gsnll.Models.GameServer.Outgoing
{
    internal sealed class GameServerOutgoingClientInfoMessage<TClientInfo> : GameServerOutgoingMessage, IMessageWithData<GameServerOutgoingClientInfoMessage<TClientInfo>.MessageData>
    {
        [JsonProperty("data")]
        public MessageData Data { get; }

        [JsonConstructor]
        public GameServerOutgoingClientInfoMessage(TClientInfo clientInfo) : base("client-info")
        {
            this.Data = new MessageData(clientInfo);
        }

        public class MessageData
        {
            [JsonProperty("clientInfo")]
            public TClientInfo ClientInfo { get; }

            public MessageData(TClientInfo clientInfo)
            {
                this.ClientInfo = clientInfo;
            }
        }
    }
}
