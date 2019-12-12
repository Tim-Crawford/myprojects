using System;
using Gsnll.Models.Matchmaking.Incoming;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Gsnll.Models.Matchmaking.JsonConverters
{
    internal sealed class MatchmakingIncomingMessageConverter : IncomingMessageConverter<IMatchmakingIncomingMessage>
    {
        protected override IMatchmakingIncomingMessage ReadMessage(JObject obj, string messageType)
        {
            if (!this.TryGetObjectToken(obj, "data", out JObject data))
            {
                throw new Exception("Invalid JSON: #/data must be an object.");
            }

            if (!this.TryGetValue(data, "message", out string message))
            {
                throw new Exception("Invalid JSON: #/data/message must be a string.");
            }

            switch (messageType)
            {
                case "response":
                {
                    return new MatchmakingIncomingResponseMessage(message);
                }

                case "connect":
                {
                    return new MatchmakingIncomingConnectMessage(message);
                }

                case "kick":
                {
                    return new MatchmakingIncomingKickMessage(message);
                }

                case "error":
                {
                    if (!this.TryGetValue(data, "errorType", out string errorType))
                    {
                        throw new Exception("Invalid JSON: #/data/errorType must be a string.");
                    }

                    return new MatchmakingIncomingErrorMessage(message, errorType);
                }

                default:
                {
                    throw new Exception($"Unknown message type: ${messageType}");
                }
            }
        }
    }
}
