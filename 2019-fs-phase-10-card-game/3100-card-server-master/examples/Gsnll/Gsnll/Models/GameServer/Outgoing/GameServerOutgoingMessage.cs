using Newtonsoft.Json;

namespace Gsnll.Models.GameServer.Outgoing
{
    internal abstract class GameServerOutgoingMessage : IMessage
    {
        [JsonProperty("messageType")]
        public string MessageType { get; }

        [JsonConstructor]
        protected GameServerOutgoingMessage(string messageType)
        {
            this.MessageType = messageType;
        }
    }
}