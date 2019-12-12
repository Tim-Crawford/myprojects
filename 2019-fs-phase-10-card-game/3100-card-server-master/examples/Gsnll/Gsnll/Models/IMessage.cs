using Newtonsoft.Json;

namespace Gsnll.Models {
    internal interface IMessage {
        [JsonProperty("messageType")]
        string MessageType { get; }
    }
}