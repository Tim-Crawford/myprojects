using Newtonsoft.Json;

namespace Gsnll.Models.Matchmaking.Outgoing
{
    internal sealed class MatchmakingConnectOutgoingMessage : MatchmakingOutgoingMessage<MatchmakingConnectOutgoingMessage.ConnectionData>
    {
        [JsonProperty("data")]
        public override ConnectionData Data { get; }

        [JsonConstructor]
        public MatchmakingConnectOutgoingMessage(ConnectionData data)
        {
            this.Data = data;
        }

        public sealed class ConnectionData
        {
            [JsonProperty("game")]
            public string Game { get; }

            [JsonProperty("clientType")]
            public string ClientType => "client";

            [JsonProperty("configuration")]
            public ClientConfiguration Configuration { get; }

            [JsonConstructor]
            public ConnectionData(string game, ClientConfiguration configuration)
            {
                this.Game = game;
                this.Configuration = configuration;
            }
        }

        public sealed class ClientConfiguration
        {
            [JsonProperty("id")]
            public string Id { get; }

            [JsonConstructor]
            public ClientConfiguration(string id)
            {
                this.Id = id;
            }
        }
    }
}
