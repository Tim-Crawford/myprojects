using Newtonsoft.Json;

namespace Gsnll.Models.Matchmaking.Outgoing
{
    internal abstract class MatchmakingOutgoingMessage<TData> : IMessageWithData<TData>
    {
        [JsonProperty("messageType")]
        public string MessageType => "connect";

        [JsonProperty("data")]
        public abstract TData Data { get; }
    }
}
