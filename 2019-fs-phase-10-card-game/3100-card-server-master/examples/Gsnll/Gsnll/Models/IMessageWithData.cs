using Newtonsoft.Json;

namespace Gsnll.Models
{
    internal interface IMessageWithData<out TData> : IMessage {
        [JsonProperty("data")]
        TData Data { get; }
    }
}
