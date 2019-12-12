using Gsnll.Models.Matchmaking.JsonConverters;
using Newtonsoft.Json;

namespace Gsnll.Models.Matchmaking.Incoming
{
    [JsonConverter(typeof(MatchmakingIncomingMessageConverter))]
    internal interface IMatchmakingIncomingMessage : IMessage { }
}